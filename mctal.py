class mctal:
	
	def __init__(self, filepath=None, verbose=False, tex=False):
		### mctal header data
		self.kod 		= '' 		# the name of the code, MCNPX.
		self.ver 		= '' 		# the version, 2.7.0.
		self.probid 	= '' 		# the date and time when the problem was run and, if it is available, the designator of the machine that was used.
		self.knod 		= 0  		# the dump number.
		self.nps 		= 0  		# the number of histories that were run.
		self.rnr 		= 0  		# the number of pseudorandom numbers that were used.
		self.title 		= '' 		# the input title card
		self.ntal 		= 0  		# number of tallies
		self.tally_n 	= [] 		# list of tally name numbers
		self.npert 		= 0  		# number of perturbations
		self.tallies 	= {} 		# dictionary of tally objects
		self.verbose 	= verbose 	# flag if prints are done
		self.tex		= tex 		# flag is TeX is used to render plot text
		self.filepath 	= filepath  # path the mctal file
		self.picklepath = None 		# path for pickling
		if self.filepath: 				# read in file if specified at instantiation
			self.read_mctal(self.filepath)
	
	def read_mctal(self,filepath):

		import MCNPtools.tally
		import re, numpy

		meshtal_flag = False

		def read_array(lines,obj,n,mode='float',limit=1e99):
			small=re.compile('([0-9].[0-9]+)([+-]+[0-9]+)')
			n_start=n
			while len(lines[n])>0 and lines[n][0]==' ' and (n-n_start)<limit:
				for m in lines[n].split():
					if mode == 'int':
						obj.append(int(m))
					elif mode == 'float':
						check = small.match(m)
						if check:
							obj.append(float(check.group(1)) * numpy.power(10.0,float(check.group(2))))   #  workaround for mcnp omitting 'E' for exponents with 3 digits
						else:
							obj.append(float(m))
				n = n+1
			return n

		# open and read in entirely
		fobj    = open(filepath)
		fstr    = fobj.read()

		# split into lines for convenience
		lines 	= fstr.split('\n')

		# split first line into its six parts
		line1   		= lines[0].split()
		self.kod 		= line1[0] 
		self.ver 		= line1[1] 
		self.probid 	= line1[2]+' '+line1[3] 
		self.knod 		= int(line1[4]) 
		self.nps 		= int(line1[5]) 
		self.rnr 		= int(line1[6])

		# next line is the title
		self.title = lines[1]

		# next is number of tallies
		self.ntal = int(lines[2].split()[1])

		# next is list of tally numbers
		n = 3
		n = read_array(lines,self.tally_n,n,mode='int')
		
		# go through tally data
		for k in self.tally_n:
			if self.verbose:
				print "... reading tally "+str(k)
			# init tally object
			self.tallies[k] = MCNPtools.tally.tally(verbose=self.verbose,tex=self.tex)
			# get header data, assert things
			t1 = lines[n].split()
			n = n+1
			self.tallies[k].name 			= int(t1[1])
			self.tallies[k].particle_type 	= int(t1[2])
			self.tallies[k].detector_type 	= int(t1[3])
			assert(t1[0]=='tally')
			assert(self.tallies[k].name==k)
			### get list of numbers if flagged
			if self.tallies[k].particle_type < 0:
				t1 = lines[n].split()
				n = n+1
				for p in t1:
					self.tallies[k].particle_list.append(int(p)) 
			for i in range(0,5):
				if lines[n][0] != 'f':
					self.tallies[k].comment 		= lines[n]
					n = n+1
				else:
					break
			# read the object numbers (surfaces, cells), keep all values so can decide what to do with them
			t1 = lines[n].split()
			self.tallies[k].object_bins 			= int(t1[1])
			n = n+1
			if (self.tallies[k].name % 10) == 5:   # point detector objects are not listed, so skip
				n = n
				self.tallies[k].objects = range(0,self.tallies[k].object_bins)
			elif len(lines[n-1].split())>2:
				if len(lines[n-1].split())!=6:
					if self.verbose:
						print "...... rejected.  number of object entries not consistent with a mesh tally."
					else:
						print "Tally %d rejected.  Number of object entries not consistent with a mesh tally."%k
					## find the start of the next tally (if any)
					while len(lines[n])>0:
						if lines[n].split()[0]=='tally':
							break
						else:
							n=n+1
					continue
				else:
					meshtal_flag = True
					self.tallies[k].objects = [[],[],[],[]]
					# read in binning parameters
					self.tallies[k].object_bins = int(t1[1])
					nbins_et	= int(t1[2])
					nbins_x		= int(t1[3])
					nbins_y		= int(t1[4])
					nbins_z		= int(t1[5])
					# read in binning data
					if nbins_et>0:
						n = read_array(lines,self.tallies[k].objects[0],n,mode='float',limit=(nbins_et/6+1))
						self.tallies[k].energies = self.tallies[k].objects[0]
					if nbins_x>0:
						n = read_array(lines,self.tallies[k].objects[1],n,mode='float',limit=(nbins_x/6+1))
					if nbins_y>0:
						n = read_array(lines,self.tallies[k].objects[2],n,mode='float',limit=(nbins_y/6+1))
					if nbins_z>0:
						n = read_array(lines,self.tallies[k].objects[3],n,mode='float',limit=(nbins_z/6+1))
			else:
				n = read_array(lines,self.tallies[k].objects,n,mode='int')
			# read single numbers bins
			self.tallies[k].totalvsdirect_bins 		= int(lines[n+0].split()[1])
			self.tallies[k].user_bins 				= int(lines[n+1].split()[1])
			# read segments
			self.tallies[k].segment_bins 			= int(lines[n+2].split()[1])
			n = n+3
			if self.tallies[k].segment_bins == 0: # make 1-indexing, since if there is 1 bin, this number is 0, and if there are two, this number is 2!
				self.tallies[k].segment_bins = 1
			elif (self.tallies[k].name % 10) == 5:   # point detector objects can only be segmented in radiography tallies, will be floats, otherwise there is no list
				n = read_array(lines,self.tallies[k].segments,n,mode='float')
			# read multipliers
			self.tallies[k].multiplier_bins 		= int(lines[n].split()[1])
			n = n+1
			if self.tallies[k].multiplier_bins == 0: # make 1-indexing, but flag to keep information that this tally is NOT multiplied
				self.tallies[k].multiplier_bins = 1
				self.tallies[k].multiplier_flag = False
			#  read cosine bins
			self.tallies[k].cosine_bins 			= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].cosines,n)
			if self.tallies[k].cosine_bins == 0:
				self.tallies[k].cosine_bins = 1
				self.tallies[k].cosines     = [-1.0,1.0]
			#  read energy bins
			self.tallies[k].energy_bins 			= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].energies,n)
			if self.tallies[k].energy_bins == 0:
				self.tallies[k].energy_bins = 1
			#  read time bins
			self.tallies[k].time_bins 				= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].times,n)
			if self.tallies[k].time_bins == 0:
				self.tallies[k].time_bins = 1
			#  read tally data
			n = n+1 #vals has no numbers following it
			n = read_array(lines,self.tallies[k].vals,n)
			self.tallies[k]._process_vals()  # parse tally data
			#  read tfc data
			if meshtal_flag:
				continue
			else:
				for d in lines[n].split()[1:] :
					self.tallies[k].tfc.append(int(d))
				n = n+1
				n = read_array(lines,self.tallies[k].tfc_data,n)

		if self.verbose:
			print "... done."

	def save(self,filepath=None):
		import cPickle, os

		if filepath:
			self.picklepath = filepath
		elif self.picklepath:
			filepath = self.picklepath
		else:
			print "NOPE.  Filepath for pickle IO not specified"
			return 

		if filepath.lstrip()[0]!='/':   #assume relative path if first non-white character isn't /
			filepath = os.getcwd()+'/'+filepath 
			self.picklepath = filepath

		if self.verbose:
			print "Saving mctal object to: '"+filepath+"'"
		file_out = open(filepath,'wb')
		cPickle.dump(self,file_out)
		file_out.close()

	def load(self,filepath=None,force=False):
		import cPickle, os

		if filepath:
			self.picklepath = filepath
		elif self.picklepath:
			filepath = self.picklepath
		else:
			print "NOPE.  Filepath for pickle IO  not specified"
			return

		if filepath.lstrip()[0]!='/':   #assume relative path if first non-white character isn't /
			filepath = os.getcwd()+'/'+filepath 
			self.picklepath = filepath

		file_in = open(filepath,'rb') 

		if force:
			a = cPickle.load(file_in)
			self.__dict__.update(a.__dict__)
		else:
			print "Are you sure you want to overwrite this mctal object with that in '"+filepath+"'?"
			response = raw_input()
			if response[0] == 'y' or response[0] == 'Y':
				print "Overwriting."
				a = cPickle.load(file_in)  ### is a autonatically cleared since there are no references to it when this function returns?
				self.__dict__.update(a.__dict__)
			else:
				print "Load aborted."

		file_in.close()

	def write_csv(self,filename,ax=None,tal=False,obj=False,cos=False,seg=False,mul=False,t_or_d=False,options=False,ylim=False):

		### options
		if not options:
			plot_options=['lin']
		else:
			plot_options=options[:]

		### deal with a non-specified tally
		if not tal:
			tal = [self.tally_n[0]]

		### non-spec total/direct
		if not t_or_d:
			t_or_d = [0]

		### input logic and plotting
		if not obj and not cos and not seg and not mul:
			for t in tal:
				self.tallies[t].plot(filename,all=True,options=plot_options)
		else:
			if not obj:
				obj = [0]
			if not cos:
				cos = [0]
			if not seg:
				seg = [0]
			if not mul:
				mul = [0]
			for t in tal:
				self.tallies[t].write_csv(filename,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options,prepend_label='{com:s}\n Tally {a:4d} :'.format(com=self.tallies[t].comment,a=t))



	def plot(self,ax=None,tal=False,obj=False,cos=False,seg=False,mul=False,t_or_d=False,options=False,ylim=False,renorm_to_sum=False,color=None,norm=1.0):
		### general plotting
		import numpy, pylab
		import matplotlib.pyplot as plt

		### TeX flag
		if self.tex:
			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')
			plt.rc('font', size=16)

		### init axes if not passed one
		if ax:
			show = False
		else:
			show = True
			fig = plt.figure(figsize=(10,6))
			ax  = fig.add_subplot(1,1,1)

		### options
		if not options:
			plot_options=['lin','wavelength','err']
		else:
			plot_options=options[:]

		if 'wavelength' in plot_options:
			leg_loc = 1
		else:
			leg_loc = 1

		### init axes if not passed one
		if ax:
			pass
		else:
			fig = plt.figure(figsize=(10,6))
			ax = fig.add_subplot(1,1,1)

		### deal with a non-specified tally
		if not tal:
			tal = [self.tally_n[0]]

		### non-spec total/direct
		if not t_or_d:
			t_or_d = [0]

		### input logic and plotting
		if not obj and not cos and not seg and not mul:
			for t in tal:
				self.tallies[t].plot(ax=ax,all=True,options=plot_options)
		else:
			if not obj:
				obj = [0]
			if not cos:
				cos = [0]
			if not seg:
				seg = [0]
			if not mul:
				mul = [0]
			for t in tal:
				self.tallies[t].plot(ax=ax,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options,prepend_label='{com:s}\n Tally {a:4d} :'.format(com=self.tallies[t].comment,a=t),ylim=ylim,renorm_to_sum=renorm_to_sum,color=color,norm=norm)

		### show
		ax.set_title(self.title.strip())
		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
		ax.grid(True)

		if show:
			fig.show()



	def write_weight_windows_from_meshtal(self,tals=False,erg=False,output='wwout',norms=False):
		import numpy, datetime
		import matplotlib.pyplot as plt
		from matplotlib.colors import LogNorm

		def compress_range(array,weight_range):
			flat_array = array.flatten()
			this_min = numpy.min(flat_array)
			this_max = numpy.max(flat_array)
			for i in range(0,len(flat_array)):
				if flat_array[i] > 0.0:
					flat_array[i] = ( (flat_array[i] - this_min ) / (this_max-this_min)  ) * (weight_range[1]-weight_range[0]) + weight_range[0]
			return numpy.reshape(flat_array, array.shape)

		def make_dimension_string(a0,array0):
			# interleave the stupid ones
			array = numpy.array(array0)
			new_array = numpy.empty((array.size*3), dtype=array.dtype)
			new_array[0::3] = numpy.ones((array.size), dtype=array.dtype)
			new_array[1::3] = array
			new_array[2::3] = numpy.ones((array.size), dtype=array.dtype)
			# prepend a0
			new_array = numpy.hstack((a0,new_array))
			# do it
			total_string=""
			fstring = "  {0: 6.{1}f}    "
			for i in range(0,int(len(new_array)/6)):
				string = ""
				string = string + fstring.format( new_array[6*i+0], 4-int(numpy.log10(max(1,abs(new_array[6*i+0])))))
				string = string + fstring.format( new_array[6*i+1], 4-int(numpy.log10(max(1,abs(new_array[6*i+1])))))
				string = string + fstring.format( new_array[6*i+2], 4-int(numpy.log10(max(1,abs(new_array[6*i+2])))))
				string = string + fstring.format( new_array[6*i+3], 4-int(numpy.log10(max(1,abs(new_array[6*i+3])))))
				string = string + fstring.format( new_array[6*i+4], 4-int(numpy.log10(max(1,abs(new_array[6*i+4])))))
				string = string + fstring.format( new_array[6*i+5], 4-int(numpy.log10(max(1,abs(new_array[6*i+5])))))
				string = string + "\n"
				total_string= total_string + string
			if len(new_array)%6:
				string = ""
				remaining = len(new_array)%6
				last_index = int(len(new_array)/6)*6
				for i in range(0,remaining):
					string = string + fstring.format(new_array[last_index+i], 4-int(numpy.log10(max(1,abs(new_array[last_index+i])))))
				string = string + "\n"
				total_string= total_string + string
			return total_string

		def make_value_string(array):
			total_string=""
			fstring = "{0: 6.5E} "
			for i in range(0,int(len(array)/6)):
				string = ""
				string = string + fstring.format( array[6*i+0])
				string = string + fstring.format( array[6*i+1])
				string = string + fstring.format( array[6*i+2])
				string = string + fstring.format( array[6*i+3])
				string = string + fstring.format( array[6*i+4])
				string = string + fstring.format( array[6*i+5])
				string = string + "\n"
				total_string= total_string + string
			if len(array)%6:
				print len(array), len(array)%6
				string = ""
				remaining = len(array)%6
				last_index = (i+1)*6
				for i in range(0,remaining):
					string = string + fstring.format(array[last_index+i])
				string = string + "\n"
				total_string= total_string + string
			return total_string


		try:
			null = iter(tals)
		except TypeError, te:
			print "Input '",tals,"'is not iterable.  A list of tally ID numbers is required."
		#try:
		#	null = iter(erg)
		#except TypeError, te:
		#	print "Input '",erg,"'is not iterable.  A list of energy boundaries is required."
		#
		#  Make list of data
		#
		print "writing to '%s'..."%output
		# make a vector of particle symbols
		particle_dict = self.tallies[self.tallies.keys()[0]].particles
		particle_symbols = []
		for i in particle_dict:
			particle_symbols.append(particle_dict[i][1])
		# check to make sure is meshtally and meshes are the same
		check_num = tals[0]
		for i in range(0,len(tals)):
			tal_num = tals[i]
			if tal_num in particle_symbols:
				print tal_num+" values are zeros"
			else:
				if not self.tallies[tal_num].is_meshtal:
					"Tally %d is not a mesh tally.  Aborting."
					return 
				if self.tallies[check_num].objects[1]!=self.tallies[tal_num].objects[1] or self.tallies[check_num].objects[2]!=self.tallies[tal_num].objects[2] or self.tallies[check_num].objects[3]!=self.tallies[tal_num].objects[3]:
					print "Mesh structure of specified tallies do not mactch!  Aborting."
					return
				if norms:
					this_norm = norms[i]
				else:
					this_norm = 0.5
				print self.tallies[tal_num].what_particles('symbol')+" values from tally %d, normed to %4.3E"%(tal_num,this_norm)
		x_bins   =     self.tallies[check_num].objects[1]
		y_bins   =     self.tallies[check_num].objects[2]
		z_bins   =     self.tallies[check_num].objects[3]
		n_x_bins = len(self.tallies[check_num].objects[1])-1
		n_y_bins = len(self.tallies[check_num].objects[2])-1
		n_z_bins = len(self.tallies[check_num].objects[3])-1
		n_particles = len(tals)
		e_bins = [7000.]  # only upper
		n_e_bins = 1
		#
		ww_arrays = {}
		for i in range(0,n_particles):
			tal_num = tals[i]
			if tal_num in particle_symbols:
				twoD_values=numpy.zeros((n_y_bins,n_x_bins))
				this_particle = tal_num
			else:
				# read in value
				this_particle = self.tallies[tal_num].what_particles('symbol')
				combined_values = numpy.zeros((n_e_bins,n_z_bins,n_y_bins,n_x_bins))
				e_dex=0
				for z_dex in range(0,n_z_bins):
					combined_values[e_dex,z_dex,:,:] = combined_values[e_dex,z_dex,:,:,] + self.tallies[tal_num].vals[0][z_dex]['data']
				# sum energies if asked to combine
				threeD_values=numpy.zeros((n_z_bins,n_y_bins,n_x_bins))
				for e_dex in range(0,n_e_bins):
					threeD_values[:,:,:]=threeD_values[:,:,:]+combined_values[e_dex,:,:,:]
				# sum z values?
				twoD_values=numpy.zeros((n_y_bins,n_x_bins))
				for z_dex in range(0,n_z_bins):
					twoD_values[:,:]=threeD_values[z_dex,:,:]+twoD_values[:,:]
				# invert the values? no! want to flatten population! just rescale so maximum is 1
				#  replace Inf with zeros
				twoD_values[          twoD_values == numpy.inf] = 0.0
				# reform to specified norm
				if norms:
					twoD_values = twoD_values* norms[i] / numpy.max(twoD_values.flatten())
				else:
					# renorm so maximum (most likely the source) is 0.5
					twoD_values = twoD_values* 0.5      / numpy.max(twoD_values.flatten())
				# apply weight cutoff
				weight_cutoff 	= 1e-9
				weight_to 		= 10.0
				print this_particle+" : applying weight cutoff %2.1E -> %2.1E"%(weight_cutoff,weight_to)
				# compress the range
				weight_range = [1e-9,norms[i]]
				print this_particle+" : applying weight compression into range %2.1E -> %2.1E"%(weight_range[0],weight_range[1])
				twoD_values = compress_range(twoD_values,weight_range)
			# have to pad the damn origin
			twoD_values = numpy.hstack( (numpy.zeros((twoD_values.shape[0],1)),twoD_values) ) 
			twoD_values = numpy.vstack( (numpy.zeros((1,twoD_values.shape[1])),twoD_values) )
			twoD_values = [numpy.zeros(twoD_values.shape),twoD_values]
			# add to dict 
			ww_arrays[this_particle] = twoD_values
			# plot
			#this_plot = ww_arrays[this_particle][1]
			#this_plot[this_plot<=0.0] = 1e-11
			#plt.imshow(this_plot,interpolation='nearest',norm=LogNorm(),cmap=plt.get_cmap('spectral'),origin='lower')
			#plt.colorbar()
			#plt.show()
		#
		#
		#
		#
		#
		#
		#
		#  write the array into wwout format
 		#
		f = open(output,'w')
		#
		# write header
		now=datetime.datetime.now()
		string = "  % 8d  % 8d  % 8d  % 8d        "%(1,1,max(particle_dict.keys()),10)+"             "+now.strftime("%d/%m/%y %H:%M:%S")+"\n"
		f.write(string)
		#
		# create masked particle vector
		particle_mask = []
		for i in range(0,len(particle_symbols)):
			if particle_symbols[i] in ww_arrays.keys():
				particle_mask.append(1)
			elif particle_symbols[i]>0:  # eliminate anti particles?
				particle_mask.append(0)
		string = " "
		for i in range(1,len(particle_mask)+1):
			string = string + "  % 7d "%(particle_mask[i-1])
			if i%7==0:
				f.write(string+"\n")
				string = " "
		if len(string)>2:
			f.write(string+"\n")
		#
		# write spatial vector header information
		nfx	= n_x_bins+1
		nfy	= n_y_bins+1
		nfz	= 2
		x0	= x_bins[ 0]-1.0
		y0	= y_bins[ 0]-1.0
		z0	= z_bins[ 0]-1.0
		ncx	= n_x_bins+1
		ncy	= n_y_bins+1
		ncz	= 2
		nwg	=1  # cart superimposed mesh
		string =         "  {0: 6.{1}f}    ".format(nfx, 5-(int(numpy.log10(abs(nfx)))+1))
		string = string +"  {0: 6.{1}f}    ".format(nfy, 5-(int(numpy.log10(abs(nfy)))+1))
		string = string +"  {0: 6.{1}f}    ".format(nfz, 5-(int(numpy.log10(abs(nfz)))+1))
		string = string +"  {0: 6.{1}f}    ".format( x0, 5-(int(numpy.log10(abs( x0)))+1))
		string = string +"  {0: 6.{1}f}    ".format( y0, 5-(int(numpy.log10(abs( y0)))+1))
		string = string +"  {0: 6.{1}f}    ".format( z0, 5-(int(numpy.log10(abs( z0)))+1))
		f.write(string+"\n")
		string =         "  {0: 6.{1}f}    ".format(ncx, 5-(int(numpy.log10(abs(ncx)))+1))
		string = string +"  {0: 6.{1}f}    ".format(ncy, 5-(int(numpy.log10(abs(ncy)))+1))
		string = string +"  {0: 6.{1}f}    ".format(ncz, 5-(int(numpy.log10(abs(ncz)))+1))
		string = string +"  {0: 6.{1}f}    ".format(nwg, 5-(int(numpy.log10(abs(nwg)))+1))
		f.write(string+"\n")
		string = make_dimension_string( x0, x_bins )
		f.write(string)
		string = make_dimension_string( y0, y_bins )
		f.write(string)
		string = make_dimension_string( z0, [z_bins[0],z_bins[-1]] )
		f.write(string)
		#
		# write values for all particles
		for i in range(0,len(particle_mask)):  # to ensure order is same as vector
			sym = particle_symbols[i]  
			if sym in ww_arrays.keys():
				dist_list = ww_arrays[sym]
				string = "{0: 6.5E} \n".format(e_bins[0])
				dist = numpy.hstack((dist_list[0].flatten(),dist_list[1].flatten()))
				string = string + make_value_string(dist)  
				f.write(string)
		# f.write("\n")
		#
		#
		#
		f.close()
		print 'done.'

