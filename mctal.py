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

		def read_array(lines,obj,n,mode='float'):
			small=re.compile('([0-9].[0-9]+)([+-]+[0-9]+)')
			while len(lines[n])>0 and lines[n][0]==' ':
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
			# read the object numbers (surfaces, cells)
			self.tallies[k].object_bins 			= int(lines[n].split()[1])
			n = n+1
			if (self.tallies[k].name % 10) == 5:   # point detector objects are not listed, so skip
				n = n
				self.tallies[k].objects = range(0,self.tallies[k].object_bins)
			elif len(lines[n-1].split())>2:
				if self.verbose:
					print "...... rejected.  Multiple entries on object line assumed to indicate mesh tally."
				else:
					print "Tally %d rejected.  Multiple entries on object line assumed to indicate mesh tally."%k
				self.tallies[k].totalvsdirect_bins	= 0
				self.tallies[k].user_bins			= 0
				self.tallies[k].segment_bins		= 0
				self.tallies[k].multiplier_bins		= 0
				self.tallies[k].cosine_bins			= 0
				self.tallies[k].energy_bins			= 0
				self.tallies[k].time_bins			= 0
				## find the start of the next tally (if any)
				while len(lines[n])>0:
					if lines[n].split()[0]=='tally':
						break
					else:
						n=n+1
				continue
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

	def plot(self,ax=None,tal=False,obj=False,cos=False,seg=False,mul=False,t_or_d=False,options=False,ylim=False):
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
				self.tallies[t].plot(ax=ax,obj=obj,seg=seg,mul=mul,cos=cos,options=plot_options,prepend_label='{com:s}\n Tally {a:4d} :'.format(com=self.tallies[t].comment,a=t),ylim=ylim)

		### show
		ax.set_title(self.title.strip())
		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
		ax.grid(True)
		fig.show()
