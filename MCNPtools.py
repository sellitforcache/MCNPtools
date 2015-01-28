### Python module to help slay the MCNP dragon 
### Ryan M. Bergmann, Jan 2015
### ryanmbergmann@gmail.com

class tally:
	### static mappings, shared by all
	###  MCNPX particle encodings
	particles={
		 1  : ['neutron'				, 'n' ],
		-1  : ['anti-neutron'			, '-n'],
		 2  : ['photon'					, 'p' ],
		 3  : ['electron'				, 'e' ],
		-3  : ['positron'				, '-e'],
		 4  : ['muon-' 					, '|' ],
		-4  : ['anti-muon-'				, '-|'],
		 5  : ['tau'					, '*' ],
		 6  : ['electron neutrino'		, 'u' ],
		-6  : ['anti-electron neutrino'	, '-u'],
		 7  : ['muon neutrino'			, 'v' ],
		 8  : ['tau neutrino'			, 'w' ],
		 9  : ['proton'					, 'h' ],
		-9  : ['anti-proton'			, '-h'],
		 10 : ['lambda0'				, 'l' ],
		 11 : ['sigma+'					, '+' ],
		 12 : ['sigma-'					, '-' ],
		 13 : ['cascade+'				, 'x' ],
		 14 : ['caccade-'				, 'y' ],
		 15 : ['omega-'					, 'o' ],
		 16 : ['lambda_c+'				, 'c' ],
		 17 : ['cascade_c+'				, '!' ],
		 18 : ['cascade_c0'				, '?' ],
		 19 : ['lambda_b0'				, '<' ],
		 20 : ['pion+'					, '/' ],
		-20 : ['pion-'					, '-/'],
		 21 : ['pion0'					, 'z' ],
		 22 : ['kaon+'					, 'k' ],
		-22 : ['kaon-'					, '-k'],
		 23 : ['K0 short'				, '%' ],
		 24 : ['K0 long'				, '^' ],
		 25 : ['D+'						, 'g' ],
		 26 : ['D0'						, '@' ],
		 27 : ['D_s+'					, 'f' ],
		 28 : ['B+'						, '>' ],
		 29 : ['B0'						, 'b' ],
		 30 : ['B_s0'					, 'q' ],
		 31 : ['deuteron'				, 'd' ],
		 32 : ['triton'					, 't' ],
		 33 : ['helium-3'				, 's' ],
		 34 : ['helium-4'				, 'a' ],
		 35 : ['heavy ions'				, '#' ]}
	particles_shorthand={
		  1 : ['neutron'					,'n ' ],
		  2 : ['photon'						,'p ' ],
		  3 : ['neutron, photon'			,'np' ], 
		  4 : ['electron'					,'e'  ],
		  5 : ['neutron, electron'			,'ne' ],
		  6 : ['photon, electron'			,'pe' ],
		  7 : ['neutron, photon, electron'	,'npe']}

	def __init__(self,verbose=False,tex=False):
		self.name 				= 0    # tally name number
		self.particle_type 		= 0    # i>0 particle type, i<0 i=number of particle type, list following
		self.detector_type		= 0    # j=type of detector tally (0=none)
		self.particle_list 		= []   # list of included particles
		self.comment 			= ''  
		self.object_bins 		= 0
		self.objects     		= []
		self.totalvsdirect_bins = 0
		self.user_bins 			= 0
		self.segment_bins 		= 0
		self.multiplier_bins 	= 0 
		self.multiplier_flag 	= True
		self.cosine_bins 		= 0
		self.cosines 			= []
		self.energy_bins 		= 0
		self.energies 			= []
		self.time_bins 			= 0
		self.times 				= []
		self.total_bins 		= 0
		self.vals 				= []
		self.tfc 				= [0,0,0,0,0,0,0,0,0]
		self.tfc_data 			= []
		self.verbose 			= verbose
		self.tex				= tex

	def what_particles(self):
		ret_string=''
		### decode particle data to human-readable
		if self.particle_type>0:
			### shorthand list, can return directly
			ret_string = self.particles_shorthand[self.particle_type][0]
		else:
			### explicit list, collect results
			for x in range(len(self.particle_list)):
				if self.particle_list[x] != 0:
					ret_string = ret_string + self.particles[(x+1)*self.particle_list[x]][0]   ### the multiplication is ti switch the sign if anti-particle and then the dictionary will know!
		return  ret_string


	def _hash(self,obj=0,user=0,seg=0,mul=0,cos=0):
		# update once multiplier and user are understood
		assert(obj  < self.object_bins)
		assert(seg  < self.segment_bins)
		assert(cos  < self.cosine_bins)
		assert(mul  < self.multiplier_bins)
		dex = obj*(self.segment_bins*self.cosine_bins*self.multiplier_bins)+ seg*(self.cosine_bins*self.multiplier_bins)+ mul*(self.cosine_bins) + cos
		return dex


	def _make_steps(self,ax,bins_in,avg_in,values_in,err_in,options=['log'],label=''):
		import numpy
		assert(len(bins_in)==len(values_in)+1)

		### make copies
		bins=bins_in[:]
		values=values_in[:]
		avg=avg_in[:]
		err=err_in[:]

		### convert energy edges to wavelength
		if 'wavelength' in options:
			bins=numpy.divide(0.286014369,numpy.sqrt(numpy.array(bins)*1.0e6))
			avg=numpy.divide(numpy.array(bins[:-1])+numpy.array(bins[1:]),2.0)

		x=[]
		y=[]
		x.append(bins[0])
		y.append(0.0)
		for n in range(len(values)):
			x.append(bins[n])
			x.append(bins[n+1])
			y.append(values[n])
			y.append(values[n])
		x.append(bins[len(values)])
		y.append(0.0)

		### plot with correct scale
		if 'lin' in options:
			ax.plot(x,y,label=label)
		else:   #default to log if lin not present
			ax.semilogx(x,y,label=label)
		
		### plot errorbars
		if 'err' in options:
			ax.errorbar(avg,values,yerr=numpy.multiply(numpy.array(err),numpy.array(values)),alpha=0.0,color='r')

		### labels
		if 'wavelength' in options:
			if self.tex:
				ax.set_xlabel(r'Wavelength (\AA)')
			else:
				ax.set_xlabel('Wavelength (A)')
		else:
			if self.tex:
				ax.set_xlabel(r'Energy (MeV)')
			else:
				ax.set_xlabel('Energy (MeV)')


	def plot(self,all=False,ax=None,obj=[0],cos=[0],seg=[0],mul=[0],options=[],prepend_label=False):
		import numpy as np
		import pylab as pl
		import matplotlib.pyplot as plt

		### I don't care the I'm overriding the built-in 'all' within this method

		### make consistency checks
		if 'lethargy' in options:
			if 'normed' in options:
				pass
			else:
				options.append('normed')

		if 'wavelength' in options:
			leg_loc = 2
		else:
			leg_loc = 1
		
		### set TeX
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

		### deal with data to be plotted
		if all:
			plot_objects	= range(self.object_bins)
			plot_segments	= range(self.segment_bins)
			plot_cosines	= range(self.cosine_bins)
			plot_multipliers= range(self.multiplier_bins)
		else:
			plot_objects	= obj
			plot_segments	= seg
			plot_cosines	= cos
			plot_multipliers= mul

		### go through selected objets and plot them
		for o in plot_objects:
			for s in plot_segments:
				for m in plot_multipliers:
					for c in plot_cosines:
						dex  		= self._hash(obj=o,cos=c,seg=s,mul=m)
						tally 		= self.vals[dex]['data'][:-1]  # clip off totals from ends
						err 		= self.vals[dex]['err'][:-1]
						cosine_bin	= self.vals[dex]['cosine_bin']
						name		= self.vals[dex]['object']
						if len(tally) < 2:
							print "tally has length <=1, aborting."
							if show:
								pl.close(fig)
							return
						bins 		= self.energies[:-1]
						widths 	 	= np.diff(bins)
						avg 		= np.divide(np.array(bins[:-1])+np.array(bins[1:]),2.0)
						if 'normed' in options:
							tally_norm  = np.divide(tally,widths)
							if 'lethargy' in options:
								tally_norm=np.multiply(tally_norm,avg)
						else:
							tally_norm = tally

						if prepend_label:
							label = prepend_label+r' obj %2d (%4d) seg %d cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1])
						else:
							label = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1])
						if 'ratio_mctal' in options:
							total 		= self.vals[dex]['data'][-1]
							total_err 	= self.vals[dex]['err'][-1]
							label = label + '\n Total = {total:5.4f} +- {err:5.4f}'.format(total=total,err=total_err)
						if 'ratio_cos' in options:
							if c == plot_cosines[0]:
								a     = tally_norm[:]
								a_err = err[:]
								a_bin = cosine_bin[:]
							else:
								label = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] / cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
								self._make_steps(ax,bins,avg,np.divide(tally_norm,a),np.add(err,a_err),options=options,label=label)
						else:
							self._make_steps(ax,bins,avg,tally_norm,err,options=options,label=label)

		### labeling
		if 'normed' in options:
			ax.set_ylabel(r'Tally / bin width')
			if 'lethargy' in options:
				ax.set_ylabel(r'Tally / unit lethargy')
		else:
			ax.set_ylabel(r'Tally')

		### title legend grid, show if self-made
		if show:
			ax.set_title(r'Tally %d: %s'% (self.name,self.what_particles())+'\n'+r'%s'%self.comment)
			handles, labels = ax.get_legend_handles_labels()
			ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
			ax.grid(True)
			pl.show()


	def _process_vals(self):
		# calculate based on binning
		total_bins = self.object_bins*(self.multiplier_bins*self.segment_bins*self.cosine_bins)  ## update for user/multiplier

		# check based on e vec length
		total_bins_e = len(self.vals)/(2*(len(self.energies)+1))
		
		# check consistency (should be thick by now)
		assert(total_bins == total_bins_e)
		self.total_bins = total_bins
		if self.verbose:
			print "...... %d non-energy bins in tally" % (self.total_bins)

		# make full vector of cosine edges
		if self.cosine_bins==1:
			self.cosines=[-1.0,1.0]
		else:
			self.cosines.insert(0,-1.0)

		# make ful vector of energy edges
		self.energies.insert(0,0.0)
		self.energies.append('total')
		
		# bag and tag em
		# indexing only for segment and cosine bins now, add others once I understand what they mean
		new_vals = []
		n = 0
		num_seg=self.segment_bins	
		num_cos=self.cosine_bins
		num_obj=self.object_bins
		num_mul=self.multiplier_bins

		for o in range(num_obj):
			for s in range(num_seg):
				for m in range(num_mul):
					for c in range(num_cos):
						if self.verbose:
							if self.multiplier_flag:
								print "...... parsing object %2d (%4d) segment %2d multiplier %2d cosine bin %2d " % (o,self.objects[o],s,m,c)
							else:
								print "...... parsing object %2d (%4d) segment %2d cosine bin %2d " % (o,self.objects[o],s,c)
						these_vals 					= {}
						subset 						= self.vals[n*(self.energy_bins*2):(n+1)*(self.energy_bins*2)]
						these_vals['object']		= self.objects[o]
						if self.multiplier_flag:
							these_vals['multiplier']= m
						else:
							these_vals['multiplier']= False
						these_vals['segment'] 		= s
						these_vals['cosine_bin']	= [self.cosines[c],self.cosines[c+1]]
						these_vals['user_bin'] 		= self.user_bins       # replace once understood
						these_vals['data'] 			= subset[0::2]
						these_vals['err'] 			= subset[1::2]
						new_vals.append(these_vals)
						n = n+1
		self.vals = new_vals 


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

		def read_array(lines,obj,n,mode='float'):
			while len(lines[n])>0 and lines[n][0]==' ':
				for m in lines[n].split():
					if mode == 'int':
						obj.append(int(m))
					elif mode == 'float':
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
			self.tallies[k] = tally(verbose=self.verbose,tex=self.tex)
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
			if lines[n][0] != 'f':
				print "here"
				self.tallies[k].comment 		= lines[n]
				n = n+1
			# read the object numbers (surfaces, cells)
			self.tallies[k].object_bins 			= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].objects,n,mode='int')
			# read single numbers bins
			self.tallies[k].totalvsdirect_bins 		= int(lines[n+0].split()[1])
			self.tallies[k].user_bins 				= int(lines[n+1].split()[1])
			self.tallies[k].segment_bins 			= int(lines[n+2].split()[1])
			self.tallies[k].multiplier_bins 		= int(lines[n+3].split()[1])
			n = n+4
			if self.tallies[k].multiplier_bins == 0: # make 1-indexing, but flag to keep information that this tally is NOT multiplied
				self.tallies[k].multiplier_bins = 1
				self.tallies[k].multiplier_flag = False
			if self.tallies[k].segment_bins == 0: # make 1-indexing, since if there is 1 bin, this number is 0, and if there are two, this number is 2!
				self.tallies[k].segment_bins = 1
			#  read cosine dbins
			self.tallies[k].cosine_bins 			= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].cosines,n)
			if self.tallies[k].cosine_bins == 0:
				self.tallies[k].cosine_bins = 1
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

	def plot(self,ax=None,tal=False,obj=False,cos=False,seg=False,mul=False,options=False):
		### general plotting
		import numpy, pylab
		import matplotlib.pyplot as plt

		### TeX flag
		if self.tex:
			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')
			plt.rc('font', size=16)

		### options
		if not options:
			plot_options=['lin','wavelength','err']
		else:
			plot_options=options[:]

		if 'wavelength' in plot_options:
			leg_loc = 2
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
				self.tallies[t].plot(ax=ax,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options,prepend_label='{com:s}\n Tally {a:4d} :'.format(com=self.tallies[t].comment,a=t))

		### show
		ax.set_title(self.title.strip())
		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
		ax.grid(True)
		fig.show()


def load_mctal_obj(filepath):
	import cPickle, os

	if filepath.lstrip()[0]!='/':   #assume relative path if first non-white character isn't /
		filepath = os.getcwd()+'/'+filepath 

	file_in = open(filepath,'rb') 
	a = cPickle.load(file_in)
	a.picklepath = filepath
	file_in.close()

	print "Loaded mctal object from '"+filepath+"'"

	return a

def save_mctal_obj(obj,filepath):
	import cPickle, os

	if filepath.lstrip()[0]!='/':   #assume relative path if first non-white character isn't /
		filepath = os.getcwd()+'/'+filepath 

	### type check
	if isinstance(obj,mctal):
		file_out = open(filepath,'wb') 
		obj.picklepath = filepath
		cPickle.dump(obj,file_out)
		file_out.close()

	print "Saved mctal object with the title '"+obj.title+"'' to: '"+filepath+"'"

def _do_ratio(objects,ax=False,tal=False,obj=False,seg=False,mul=False,cos=False,options=False):
	### internal function to make a new mctal object with ratio values and plot it on ax
	import numpy

	### input check
	if not ax or not tal or not obj or not seg or not mul or not cos or not options:
		print "INPUT ERROR IN _do_ratio()!"
		return
	if 'normed' in options:
		print "Norming is invalid for ratios, ignored."
		options.remove('normed')

	### set first title string
	title = 'a = {a:s}'.format(a=objects[0].title.strip())
	letter=['a','b','c','d','e','f','g']


	### do the ratios
	for o_in in range(len(objects)-1):

		### make mctal object
		dummy 			= mctal(tex=objects[0].tex)
		dummy.title  	= objects[o_in+1].title
		#assert( set(objects[0].tally_n)	== set(objects[1].tally_n))
		dummy.ntal 		= len(tal)
	
		### insert new vector into empty mctal, copy necessary values
		for t in tal:
			### make tally for ratios
			#dummy.tally_n.append(objects[0].tally_n[t])
			dummy.tallies[t]  					= tally(tex=dummy.tex)
			dummy.tallies[t].comment 			= objects[0].tallies[t].comment
			dummy.tallies[t].object_bins		= len(obj)
			dummy.tallies[t].segment_bins		= len(seg)
			dummy.tallies[t].cosine_bins		= len(cos)
			dummy.tallies[t].multiplier_bins	= len(mul)
			### check lengths for consistency:
			assert( set(objects[0].tallies[t].objects)  	== set(objects[o_in+1].tallies[t].objects))
			assert( set(objects[0].tallies[t].cosines) 		== set(objects[o_in+1].tallies[t].cosines))	
			assert( set(objects[0].tallies[t].energies) 	== set(objects[o_in+1].tallies[t].energies))
			### and copy energies now
			dummy.tallies[t].energies = objects[0].tallies[t].energies[:]
			### add to name vectors
			# print o0,o,objects[0].tallies[t].objects,dummy.tallies[t].objects
			# dummy.tallies[t].objects.append(objects[0].tallies[t].objects[o])
			# dummy.tallies[t].cosines.append(objects[0].tallies[t].cosines[c])
	
	
			o0 = 0
			for o in obj:
				s0 = 0
				for s in seg:
					m0 = 0
					for m in mul:
						c0 = 0
						for c in cos:
							### check indexing, that order is consistent new tally object
							dex0 = dummy.tallies[t]._hash(obj=o0,seg=s0,mul=m0,cos=c0)
							assert(dex0 == len(dummy.tallies[t].vals)) 
	
							### get values ratio
							dex 	= objects[0].tallies[t]._hash(obj=o,seg=s,mul=m,cos=c)
							a 		= objects[0].tallies[t].vals[dex]['data'][:]
							b 		= objects[o_in+1].tallies[t].vals[dex]['data'][:]
							a_err	= objects[0].tallies[t].vals[dex]['err'][:]
							b_err	= objects[o_in+1].tallies[t].vals[dex]['err'][:]
	
							### copy in data
							these_vals = {}
							if 'rel' in options:
								these_vals['data'] 		= numpy.subtract(numpy.divide(numpy.array(b),numpy.array(a)),1.0)
							else:
								these_vals['data'] 		= numpy.divide(numpy.array(b),numpy.array(a))
							these_vals['err'] 			= numpy.add(numpy.array(a_err),numpy.array(b_err))  # rel err of quotient is just the sum or errors?!
							these_vals['object']		= objects[0].tallies[t].vals[dex]['object']
							these_vals['multiplier']	= objects[0].tallies[t].vals[dex]['multiplier']
							these_vals['segment'] 		= objects[0].tallies[t].vals[dex]['segment']
							these_vals['cosine_bin']	= objects[0].tallies[t].vals[dex]['cosine_bin'][:]
							these_vals['user_bin'] 		= objects[0].tallies[t].vals[dex]['user_bin']
							dummy.tallies[t].vals.append(these_vals)
							c0 = c0 + 1
						m0 = m0 +1
					s0 = s0 + 1
				o0 = o0 + 1
	
		### finally plot the sucker
		for t in tal:
			labelstr = '{a1:s} : {com:s}\n Tally {t:4d} :'.format(a1=letter[o_in+1],com=dummy.tallies[t].comment,t=t)
			dummy.tallies[t].plot(all=True,ax=ax,options=options,prepend_label=labelstr)

		### append to title string
		title = title + '\n {a:s} = {b:s}'.format(a=letter[o_in+1],b=objects[o_in+1].title.strip())

	### slight differences
	if 'rel' in options:
		ax.set_ylabel('Rel. Diff. ( ([x]-a)/a) ')
	else:
		ax.set_ylabel('Ratio ([x]/a)')
	ax.set_title(title)

def plot(objects,ax=None,tal=False,obj=False,cos=False,seg=False,mul=False,options=False):
	### plotting routines for inter-mctal plots
	import numpy, pylab
	import matplotlib.pyplot as plt

	### type check
	for o in objects:
		if isinstance(o,mctal):
			pass
		else:
			print "Objects in list are not MCNPtools.mctal instances!  Aborting."
			return

	### TeX flag of first object
	if objects[0].tex:
		plt.rc('text', usetex=True)
		plt.rc('font', family='serif')
		plt.rc('font', size=16)

	### options
	if not options:
		plot_options=['lin','wavelength','err']
	else:
		plot_options=options[:]
		if 'ratio' in options:
			plot_options.remove('ratio')
			plot_options.append('ratio_mctal')
		if 'rel' in plot_options:
			if 'ratio_mctal' not in plot_options:
				plot_options.append('ratio_mctal')
	if 'wavelength' in options:
		leg_loc = 2
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
		tal = [objects[0].tally_n[0]]

	### input logic and plotting, using methods
	if not obj and not cos and not seg and not mul:
		if 'ratio_mctal' in plot_options:
			obj = range(objects[0].tallies[tal[0]].object_bins)
			seg = range(objects[0].tallies[tal[0]].segment_bins)
			cos = range(objects[0].tallies[tal[0]].cosine_bins)
			mul = range(objects[0].tallies[tal[0]].multiplier_bins)
			_do_ratio(objects,ax=ax,tal=tal,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options)
		else:
			for this_mctal in objects:
				for t in tal:
					this_mctal.tallies[t].plot(ax=ax,all=True,options=plot_options)
	else:
		if not obj:
			obj = [0]
		if not cos:
			cos = [0]
		if not seg:
			seg = [0]
		if not mul:
			mul = [0]
		if 'ratio_mctal' in plot_options:
			_do_ratio(objects,ax=ax,tal=tal,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options)
		else:
			for this_mctal in objects:
				for t in tal:
					this_mctal.tallies[t].plot(ax=ax,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options,prepend_label='{title:s}\n{com:s}\n Tally {a:4d} :'.format(title=this_mctal.title.strip(),com=this_mctal.tallies[t].comment,a=t))

	### show
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
	ax.grid(True)
	fig.show()