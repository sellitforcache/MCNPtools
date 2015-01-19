### Python module to help slay the MCNP dragon 
### Ryan M. Bergmann, Jan 2015
### ryanmbergmann@gmail.com

class tally:
	def __init__(self,verbose=0):
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

	def _make_steps(self,ax,bins_in,values_in,options=['log'],label=''):
		import numpy
		assert(len(bins_in)==len(values_in)+1)

		bins=bins_in[:]
		values=values_in[:]
		if 'wavelength' in options:
			bins=numpy.divide(0.286014369,numpy.sqrt(numpy.array(bins)*1.0e6))
			if 'log' in options:
				options.remove('log')
				options.append('lin')
			elif 'lin' in options:
				pass
			else:
				options.append('lin')

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

		if 'lin' in options:
			ax.plot(x,y,label=label)
			ax.set_xlabel('Wavelength (A)')
		else:   #default to log if lin not present
			ax.semilogx(x,y,label=label)
			ax.set_xlabel('Energy (MeV)')


	def _hash(self,obj=0,user=0,seg=0,mult=0,cos=0):
		# update once multiplier and user are understood
		assert(obj  < self.object_bins)
		if self.segment_bins==0 and self.cosine_bins==0:
			assert(seg  == self.segment_bins)
			assert(cos  == self.cosine_bins)
		else:
			assert(seg  < self.segment_bins)
			assert(cos  < self.cosine_bins)
		dex = obj* (self.segment_bins*self.cosine_bins)+seg* (self.cosine_bins)+cos
		return dex


	def _process_vals(self):
		# calculate based on binning
		total_bins = self.object_bins*(self.segment_bins*self.cosine_bins)  ## update for user/multiplier
		if self.segment_bins==0 and self.cosine_bins==0:
			total_bins = self.object_bins

		# check based on e vec length
		total_bins_e = len(self.vals)/(2*(len(self.energies)+1))
		
		# check consistency (should be thick by now)
		assert(total_bins == total_bins_e)
		self.total_bins = total_bins
		if self.verbose:
			print "...... %d non-energy bins in tally" % (self.total_bins)

		# make full vector of cosine edges
		if self.cosine_bins==0:
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
		if self.segment_bins==0 and self.cosine_bins==0:
			num_seg=1
			num_cos=1
		else:
			num_seg=self.segment_bins
			num_cos=self.cosine_bins
		for s in range(num_seg):
			for c in range(num_cos):
				if self.verbose:
					print "...... parsing segment %d cosine bin %d " % (s,c)
				these_vals 					= {}
				subset 						= self.vals[n*(self.energy_bins*2):(n+1)*(self.energy_bins*2)]
				these_vals['segment'] 		= s
				these_vals['cosine_bin']	= [self.cosines[c],self.cosines[c+1]]
				these_vals['multiplier_bin']= self.multiplier_bins # replace once understood
				these_vals['user_bin'] 		= self.user_bins       # replace once understood
				these_vals['data'] 			= subset[0::2]
				these_vals['err'] 			= subset[1::2]
				new_vals.append(these_vals)
				n = n+1
		self.vals = new_vals 


	def plot(self,ax_in=None,obj=[0],cos=[0],seg=[0],options=[]):
		import numpy as np
		import pylab as pl

		### init axes if not passed one
		if ax_in:
			ax=ax_in
		else:
			fig = pl.figure(figsize=(10,6))
			ax = fig.add_subplot(1,1,1)

		### deal with data to be plotted
		if 'all' in options:
			plot_objects	= range(self.object_bins)
			if self.segment_bins==0 and self.cosine_bins==0:
				plot_segments 	= [0]
				plot_cosines 	= [0]
			else:
				plot_segments	= range(self.segment_bins)
				plot_cosines	= range(self.cosine_bins)
		else:
			plot_objects	= obj
			plot_segments	= seg
			plot_cosines	= cos

		### deal with options
		if 'wavelength' in options:
			plot_options=['wavelength']
		else:
			plot_options=[]

		### go through selected objets and plot them
		for o in plot_objects:
			for s in plot_segments:
				for c in plot_cosines:
					dex  		= self._hash(obj=o,cos=c,seg=s)
					tally 		= self.vals[dex]['data'][:-1]
					err 		= self.vals[dex]['err'][:-1]
					bins 		= self.energies[:-1]
					widths 	 	= np.diff(bins)
					avg 		= np.divide(np.array(bins[:-1])+np.array(bins[1:]),2.0)
					if 'normed' in options:
						tally_norm  = np.divide(tally,widths)
						if 'lethargy' in options:
							tally_norm=np.multiply(tally_norm,avg)
					else:
						tally_norm = tally
					self._make_steps(ax,bins,tally_norm,options=plot_options,label='Obj %d seg %d cos %4.2E - %4.2E' % (o,s,self.cosines[c],self.cosines[c+1]))

		### labeling
		if 'normed' in options:
			ax.set_ylabel('tally / bin width')
			if 'lethargy' in options:
				ax.set_ylabel('tally / bin width / unit lethargy')
		else:
			ax.set_ylabel('tally')

		### title and legend
		ax.set_title('Tally %d'%self.name)
		handles, labels = ax.get_legend_handles_labels()
		print handles,labels
		ax.legend(handles,labels,loc=1)

		### show
		ax.grid(True)
		pl.show()


class mctal:
	### static mappings, shared by all
	particles={
		 1 	: ['neutron' 				, 'n' ],
		-1 	: ['anti-neutron' 			, '-n'],
		 2 	: ['photon' 				, 'p' ],
		 3	: ['electron' 				, 'e' ],
		-3	: ['positron' 				, '-e'],
		 4	: ['muon-' 					, '|' ],
		-4 	: ['anti-muon-' 			, '-|'],
		 5 	: ['tau'					, '*' ],
		 6 	: ['electron neutrino'		, 'u' ],
		-6 	: ['anti-electron neutrino'	, '-u'],
		 7 	: ['muon neutrino'			, 'v' ],
		 8 	: ['tau neutrino'			, 'w' ],
		 9 	: ['proton' 				, 'h' ],
		-9 	: ['anti-proton' 			, '-h'],
		 10	: ['lambda0' 				, 'l' ],
		 11	: ['sigma+'					, '+' ],
		 12	: ['sigma-'					, '-' ],
		 13	: ['cascade+'				, 'x' ],
		 14	: ['caccade-'				, 'y' ],
		 15	: ['omega-' 				, 'o' ],
		 16	: ['lambda_c+'				, 'c' ],
		 17	: ['cascade_c+'				, '!' ],
		 18	: ['cascade_c0'				, '?' ],
		 19	: ['lambda_b0'				, '<' ],
		 20	: ['pion+' 					, '/' ],
		-20 : ['pion-' 					, '-/'],
		 21 : ['pion0'					, 'z' ],
		 22 : ['kaon+'					, 'k' ],
		-22 : ['kaon-'					, '-k'],
		 23 : ['K0 short'				, '%' ],
		 24 : ['K0 long'				, '^' ],
		 25 : ['D+'						, 'g' ],
		 26 : ['D0'						, '@' ],
		 27 : ['D_s+'					, 'f' ],
		 28 : ['B+'						, '>' ],
		 29	: ['B0' 					, 'b' ],
		 30	: ['B_s0' 					, 'q' ],
		 31	: ['deuteron' 				, 'd' ],
		 32	: ['triton' 				, 't' ],
		 33	: ['helium-3' 				, 's' ],
		 34	: ['helium-4' 				, 'a' ],
		 35	: ['heavy ions' 			, '#' ]}
	
	def __init__(self, filepath=None):
		### mctal header data
		self.kod 		= '' # the name of the code, MCNPX.
		self.ver 		= '' # the version, 2.7.0.
		self.probid 	= '' # the date and time when the problem was run and, if it is available, the designator of the machine that was used.
		self.knod 		= 0  # the dump number.
		self.nps 		= 0  # the number of histories that were run.
		self.rnr 		= 0  # the number of pseudorandom numbers that were used.
		self.title 		= '' # the input title card
		self.ntal 		= 0  # number of tallies
		self.tally_n 	= [] # list of tally name numbers
		self.npert 		= 0  # number of perturbations
		self.tallies 	= {} # dictionary of tally objects
		self.verbose 	= 0  # flag if prints are done
		if filepath:
			self.read_mctal_file(filepath)
	
	def read_mctal_file(self,filepath):

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
			self.tallies[k] = tally(verbose=self.verbose)
			# get header data, assert things
			t1 = lines[n].split()
			n = n+1
			self.tallies[k].name 			= int(t1[1])
			self.tallies[k].particle_type 	= int(t1[2])
			self.tallies[k].detector_type 	= int(t1[3])
			assert(t1[0]=='tally')
			assert(self.tallies[k].name==k)
			t1 = lines[n].split()
			n = n+1
			for p in t1:
				self.tallies[k].particle_list.append(int(p)) 
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
			#  read cosine dbins
			self.tallies[k].cosine_bins 			= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].cosines,n)
			#  read energy bins
			self.tallies[k].energy_bins 			= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].energies,n)
			#  read time bins
			self.tallies[k].time_bins 				= int(lines[n].split()[1])
			n = n+1
			n = read_array(lines,self.tallies[k].times,n)
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