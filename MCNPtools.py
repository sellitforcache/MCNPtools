class tally:
	def __init__(self):
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
		self.vals 				= []
		self.tfc 				= [0,0,0,0,0,0,0,0,0]
		self.tfc_data 			= []


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
			print "... reading tally "+str(k)
			# init tally object
			self.tallies[k] = tally()
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
			#  read tfc data
			for d in lines[n].split()[1:] :
				self.tallies[k].tfc.append(int(d))
			n = n+1
			n = read_array(lines,self.tallies[k].tfc_data,n)

		print "done."
