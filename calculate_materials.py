class mixture(object):

	_mixtures = {}

	def __new__(cls,name):
		if not isinstance(name,int):
			if isinstance(name,str):
				name = name.strip()
		else:
			print "name must be a string.  rejected."
			return None
		# else return a new instance
		return super(mixture,cls).__new__(cls)

	def __init__(self,name):
		import copy
		if isinstance(name,str):
			name = name.strip()
			self.name		= copy.deepcopy(name)
		else:
			print "name must be a string.  rejected."
			return None
		self.mode				= 'none'
		self.avg_amu			= 0.0
		self.mass_density		= 0.0
		self.mixtures_list		= []
		self.atom_fractions		= {}
		self.mass_fractions		= {}
		self.volume_fractions	= {}

	def make_isotope_lists_from_mixture_list(self):
		# SUMMED ISOTOPE LIST
		#
		# calculate the list of isotope atom fractions from the sum of the mixtures
		for i in range(0,len(self.mixtures_list)):
			for isotope in self.mixtures_list[i][0].atom_fractions.keys():
				if isotope in self.atom_fractions.keys():
					self.atom_fractions[isotope] = self.atom_fractions[isotope] + self.mixtures_list[i][0].atom_fractions[isotope] * self.mixtures_list[i][1]
				else:
					self.atom_fractions[isotope] =                                self.mixtures_list[i][0].atom_fractions[isotope] * self.mixtures_list[i][1]
		# calculate averge amu from the atom fractions
		self.avg_amu = 0.0 
		for isotope in self.atom_fractions.keys():
			self.avg_amu = self.avg_amu + amu[isotope] * self.atom_fractions[isotope]
		# calculate the mass factions
		for isotope in self.atom_fractions.keys():
			self.mass_fractions[isotope] = amu[isotope] * self.atom_fractions[isotope] / self.avg_amu

	def add_mixture(self,name_in,frac,mode='mass'):
		# strip off whitespace from name
		name=name_in.strip()
		#
		if not isinstance(name,str):
			print "first input (name) is not a string.  rejected."
			return
		if not name in mixture._mixtures.keys():
			print "'"+name+"' not found in mixtures dictionary.  rejected."
			return
		if not isinstance(frac,float):
			print "second input is not a float atomic fraction.  rejected."
			return
		if not isinstance(mode,str):
			print "mode keyword input is not a string.  rejected."
			return
		if self.mode not in [mode,'none']:
			if verbose: print "element object is in %s mode.  delete and start over."%self.mode
		#
		self.mode = mode
		if mode == 'atom':
			self.mixtures_list.append([mixture._mixtures[name],frac,0.,0.])
		elif mode == 'mass':
			self.mixtures_list.append([mixture._mixtures[name],0.,frac,0.])
		elif mode == 'volume':
			self.mixtures_list.append([mixture._mixtures[name],0.,0.,frac])
		if verbose: print "added mixture '%s' with amu %12.8f and %s fraction %15.8f into mixture '%s'"%(name,mixture._mixtures[name].avg_amu,self.mode,frac,self.name)

	def delete(self):
		element._elements.pop(self.name, None)
		self.__init__(self.name)
		if verbose: print "removed element %s from the class dictionary and re-initialized all data.  the instance has not necessarily been deleted from the python namespace yet!"%self.name

	def finalize(self):
		import numpy

		if self.mode == 'atom':
			# check that there is a mass density present (mass densities of input mixtures is not used)
			if self.mass_density==0.0:
				print "mass density needs to be input to finalize, aborting."
				return
			# check that there is a nonzero list of mixtures
			if len(self.mixtures_list)==0:
				print "no mixtures in list while in %s mode, aborting."%self.mode
				return
			#
			# MIXTURES
			#
			# sum the fractions, renormalize
			frac_total = 0.0
			for i in range(0,len(self.mixtures_list)):
				frac_total = frac_total + self.mixtures_list[i][1]
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][1] = self.mixtures_list[i][1] / frac_total
			# calculate average amu from atom fractions
			mix_avg_amu = 0.0 
			for i in range(0,len(self.mixtures_list)):
				mix_avg_amu = mix_avg_amu + self.mixtures_list[i][0].avg_amu * self.mixtures_list[i][1]
			# calculate the mixture mass factions
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][2] = self.mixtures_list[i][0].avg_amu * self.mixtures_list[i][1] / mix_avg_amu
			# calculate the mixture volume, if the densities are conserved
			mix_vol = 0.0
			for i in range(0,len(self.mixtures_list)):
				mix_vol = mix_vol + self.mixtures_list[i][2]/self.mixtures_list[i][0].mass_density
			# calculate the mixture volume factions
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][3] = self.mixtures_list[i][2]/self.mixtures_list[i][0].mass_density / mix_vol
			# make full isotope list
			self.make_isotope_lists_from_mixture_list()

		elif self.mode == 'mass':
			# check that there is a mass density present (mass densities of input mixtures is not used)
			if self.mass_density==0.0:
				print "mass density needs to be input to finalize, aborting."
				return
			# check that there is a nonzero list of mixtures
			if len(self.mixtures_list)==0:
				if verbose: print "no mixtures in list while in %s mode, aborting."%self.mode
				return
			#
			# MIXTURES
			#
			# sum the mass fractions, renormalize
			frac_total = 0.0
			for i in range(0,len(self.mixtures_list)):
				frac_total = frac_total + self.mixtures_list[i][2]
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][2] = self.mixtures_list[i][2] / frac_total
			# calculate average amu from mass fractions
			mix_avg_amu = 0.0 
			for i in range(0,len(self.mixtures_list)):
				mix_avg_amu = mix_avg_amu + self.mixtures_list[i][2] / self.mixtures_list[i][0].avg_amu
			mix_avg_amu = 1.0 / mix_avg_amu
			# calculate the mixture atom factions
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][1] = mix_avg_amu * self.mixtures_list[i][2] / self.mixtures_list[i][0].avg_amu
			# calculate the mixture volume, if the densities are conserved
			mix_vol = 0.0
			for i in range(0,len(self.mixtures_list)):
				mix_vol = mix_vol + self.mixtures_list[i][2]/self.mixtures_list[i][0].mass_density
			# calculate the mixture volume factions
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][3] = self.mixtures_list[i][2]/self.mixtures_list[i][0].mass_density / mix_vol
			# make full isotope list
			self.make_isotope_lists_from_mixture_list()

		elif self.mode == 'volume':
			# a density must NOT be set, since it will be overwritten, reject to avoid silent errors or unepected behavior
			# must check that every input mixture has densities set
			# check that there is a nonzero list of mixtures
			if len(self.mixtures_list)==0:
				if verbose: print "no mixtures in list while in %s mode, aborting."%self.mode
				return
			# check that there is a nonzero list of mixtures
			if len(self.mixtures_list)==0:
				print "no mixtures in list while in %s mode, aborting."%self.mode
				return
			#
			# MIXTURES
			#
			# sum the fractions, renormalize
			frac_total = 0.0
			for i in range(0,len(self.mixtures_list)):
				frac_total = frac_total + self.mixtures_list[i][3]
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][3] = self.mixtures_list[i][3] / frac_total
			# calculate average density
			self.mass_density = 0.0
			for i in range(0,len(self.mixtures_list)):
				self.mass_density = self.mass_density + self.mixtures_list[i][3] * self.mixtures_list[i][0].mass_density
			# calculate the mixture mass factions
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][2] = self.mixtures_list[i][3] * self.mixtures_list[i][0].mass_density / self.mass_density
			# calculate average amu from mass fractions
			mix_avg_amu = 0.0 
			for i in range(0,len(self.mixtures_list)):
				mix_avg_amu = mix_avg_amu + self.mixtures_list[i][2] / self.mixtures_list[i][0].avg_amu
			mix_avg_amu = 1.0 / mix_avg_amu
			# calculate the mixture atom factions
			for i in range(0,len(self.mixtures_list)):
				self.mixtures_list[i][1] = mix_avg_amu * self.mixtures_list[i][2] / self.mixtures_list[i][0].avg_amu
			# make full isotope list
			self.make_isotope_lists_from_mixture_list()

		elif self.mode == 'none':
			# check that there is a mass density present
			if self.mass_density==0.0:
				print "mass density needs to be input to finalize, aborting."
				return
			# check that there is a zero list of mixtures
			if len(self.mixtures_list)!=0:
				print "mixtures present in list while in %s mode, aborting."%self.mode
				return
			# check that only atom fractions exist (mass not supported as of yet...)
			if len(self.mass_fractions)>0 and len(self.atom_fractions)>0:
				print "mass AND volume fractions present while in %s mode, aborting."%self.mode
				return
			if len(self.mass_fractions)<=0 and len(self.atom_fractions)<=0:
				print "no atom OR mass fractions present while in %s mode, aborting."%self.mode
				return
			if len(self.atom_fractions)>0:
				# sum the fractions, renormalize
				frac_total = 0.0
				for isotope in self.atom_fractions.keys():
					frac_total = frac_total + self.atom_fractions[isotope]
				for isotope in self.atom_fractions.keys():
					self.atom_fractions[isotope] = self.atom_fractions[isotope] / frac_total
				# calculate averge amu from the atom fractions
				self.avg_amu = 0.0 
				for isotope in self.atom_fractions.keys():
					self.avg_amu = self.avg_amu + amu[isotope] * self.atom_fractions[isotope]
				# calculate the mass factions
				for isotope in self.atom_fractions.keys():
					self.mass_fractions[isotope] = amu[isotope] * self.atom_fractions[isotope] / self.avg_amu

			else:
				# sum the mass fractions, renormalize
				frac_total = 0.0
				for isotope in self.mass_fractions.keys():
					frac_total = frac_total + self.mass_fractions[isotope]
				for isotope in self.mass_fractions.keys():
					self.mass_fractions[isotope] = self.mass_fractions[isotope] / frac_total
				# calculate average amu from mass fractions
				self.avg_amu = 0.0 
				for i in range(0,len(self.mixtures_list)):
					self.avg_amu = self.avg_amu + self.mass_fractions[isotope] / amu[isotope]
				self.avg_amu = 1.0 / self.avg_amu
				# calculate atom fractions
				for i in range(0,len(self.mixtures_list)):
					self.atom_fractions[isotope] = self.avg_amu * self.mass_fractions[isotope] / amu[isotope]

		elif self.mode == 'finalized':
			print "already finalized."
			return
		else:
			print "uninitialized!  cannot finalize."
			return

		if verbose: print "added mixture '%s' to the class dictionary."%self.name
		self.mode = 'finalized'
		mixture._mixtures[self.name] = self

	def print_material_card(self,comment=False):

		# set types
		if print_type == 'atom':
			isotope_list_total   = self.atom_fractions.keys()
			isotope_values_total = self.atom_fractions
			multiplier = 1.0
		elif print_type == 'mass':
			isotope_list_total   = self.mass_fractions.keys()
			isotope_values_total = self.mass_fractions
			multiplier = -1.0
		else:
			print 'print_type %s is not recognized!'%print_type
			return

		# sort for neatness
		isotope_list_total.sort()

		print "c"
		print "c         '%s'"%self.name
		print "c"
		print "c         average amu     = %12.8f"%self.avg_amu
		print "c         density         =  %11.8f"%self.mass_density
		if len(self.mixtures_list)>0:
			print "c"
			print "c         mixture     avg. amu     atom fraction    mass fraction    volume fraction"
			print "c         --------    --------     -------------    -------------    ---------------"
			for m in self.mixtures_list:
				print "c  %15s    %8.4f     %10.8f       %10.8f       %10.8f"%(m[0].name,m[0].avg_amu,m[1],m[2],m[3])
			print "c"
			if verbose:
				for m in self.mixtures_list:
					m[0].print_material_card(comment=True)
		elif comment==False:
			print "c"
			print "c         mixture     amu          atom fraction    mass fraction"
			print "c         --------    --------     -------------    -------------"
			for isotope in isotope_list_total:
				print "c  %15s    %8.4f     %10.8f       %10.8f"%(isotope,amu[isotope],self.atom_fractions[isotope],self.mass_fractions[isotope])
			print "c"
		print "c"
		if comment:
			for isotope in isotope_list_total:
				print "c    %6d   %8.10E"%(isotope,multiplier*isotope_values_total[isotope])
		else:
			print "c"
			print "c ISOTOPES FOR '%s'"%self.name
			print "c"
			print "mXXX"
			for isotope in isotope_list_total:
				print "     %6d   %8.10E"%(isotope,multiplier*isotope_values_total[isotope])
		print "c"

#
# global settings variables
#
verbose = 0
print_type = 'atom'

#
# proton numbers, indexed by element symbol string
#
z_number = {}
z_number['H']	=   1000
z_number['He']	=   2000
z_number['Li']	=   3000
z_number['Be']	=   4000
z_number['B']	=   5000
z_number['C']	=   6000
z_number['N']	=   7000
z_number['O']	=   8000
z_number['F']	=   9000
z_number['Ne']	=  10000 	
z_number['Na']	=  11000 	
z_number['Mg']	=  12000 	
z_number['Al']	=  13000 	
z_number['Si']	=  14000 	
z_number['P']	=  15000 	
z_number['S']	=  16000 	
z_number['Cl']	=  17000 	
z_number['Ar']	=  18000 	
z_number['K']	=  19000 	
z_number['Ca']	=  20000 	
z_number['Sc']	=  21000 	
z_number['Ti']	=  22000 	
z_number['V']	=  23000 	
z_number['Cr']	=  24000 	
z_number['Mn']	=  25000 	
z_number['Fe']	=  26000 	
z_number['Co']	=  27000 	
z_number['Ni']	=  28000 	
z_number['Cu']	=  29000 	
z_number['Zn']	=  30000 	
z_number['Ga']	=  31000 	
z_number['Ge']	=  32000 	
z_number['As']	=  33000 	
z_number['Se']	=  34000 	
z_number['Br']	=  35000 	
z_number['Kr']	=  36000 	
z_number['Rb']	=  37000 	
z_number['Sr']	=  38000 	
z_number['Y']	=  39000 	
z_number['Zr']	=  40000 	
z_number['Nb']	=  41000 	
z_number['Mo']	=  42000 	
z_number['Tc']	=  43000 	
z_number['Ru']	=  44000 	
z_number['Rh']	=  45000 	
z_number['Pd']	=  46000 	
z_number['Ag']	=  47000 	
z_number['Cd']	=  48000 	
z_number['In']	=  49000 	
z_number['Sn']	=  50000 	
z_number['Sb']	=  51000 	
z_number['Te']	=  52000 	
z_number['I']	=  53000 	
z_number['Xe']	=  54000 	
z_number['Cs']	=  55000 	
z_number['Ba']	=  56000 	
z_number['La']	=  57000 	
z_number['Ce']	=  58000 	
z_number['Pr']	=  59000 	
z_number['Nd']	=  60000 	
z_number['Pm']	=  61000 	
z_number['Sm']	=  62000 	
z_number['Eu']	=  63000 	
z_number['Gd']	=  64000 	
z_number['Tb']	=  65000 	
z_number['Dy']	=  66000 	
z_number['Ho']	=  67000 	
z_number['Er']	=  68000 	
z_number['Tm']	=  69000 	
z_number['Yb']	=  70000 	
z_number['Lu']	=  71000 	
z_number['Hf']	=  72000 	
z_number['Ta']	=  73000 	
z_number['W']	=  74000 	
z_number['Re']	=  75000 	
z_number['Os']	=  76000 	
z_number['Ir']	=  77000 	
z_number['Pt']	=  78000 	
z_number['Au']	=  79000 	
z_number['Hg']	=  80000 	
z_number['Tl']	=  81000 	
z_number['Pb']	=  82000 	
z_number['Bi']	=  83000 	
z_number['Po']	=  84000 	
z_number['At']	=  85000 	
z_number['Rn']	=  86000 	
z_number['Fr']	=  87000 	
z_number['Ra']	=  88000 	
z_number['Ac']	=  89000 	
z_number['Th']	=  90000 	
z_number['Pa']	=  91000 	
z_number['U']	=  92000 	
z_number['Np']	=  93000 	
z_number['Pu']	=  94000 	
z_number['Am']	=  95000 	
z_number['Cm']	=  96000 	
z_number['Bk']	=  97000 	
z_number['Cf']	=  98000 	
z_number['Es']	=  99000 	
z_number['Fm']	= 100000
z_number['Md']	= 101000
z_number['No']	= 102000
z_number['Lr']	= 103000
z_number['Rf']	= 104000
z_number['Db']	= 105000
z_number['Sg']	= 106000
z_number['Bh']	= 107000
z_number['Hs']	= 108000
z_number['Mt']	= 109000
z_number['Ds']	= 110000
z_number['Rg']	= 111000
z_number['Uub']	= 112000
z_number['Uut']	= 113000
z_number['Uuq']	= 114000
z_number['Uup']	= 115000
z_number['Uuh']	= 116000
z_number['Uus']	= 117000
z_number['Uuo']	= 118000

# 
# isotopic mass values, indexed by ZAID
# https://www.ncsu.edu/chemistry/msf/pdf/IsotopicMass_NaturalAbundance.pdf
#
amu = {}
amu[ 1001]= 1.007825032239
amu[ 1002]= 2.014101778121
amu[ 2003]= 3.016029
amu[ 2004]= 4.002603
amu[ 3006]= 6.015122
amu[ 3007]= 7.016004
amu[ 4009]= 9.012182
amu[ 5010]=10.012937
amu[ 5011]=11.009305
amu[ 6012]=12.000000
amu[ 6013]=13.003355
amu[ 7014]=14.003074
amu[ 7015]=15.000109
amu[ 8016]=15.994915
amu[ 8017]=16.999132
amu[ 8018]=17.999160
amu[ 9019]=18.998403
amu[10020]=19.992440
amu[10021]=20.993847
amu[10022]=21.991386
amu[11023]=22.989770
amu[12024]=23.985042
amu[12025]=24.985837
amu[12026]=25.982593
amu[13027]=26.981538
amu[14028]=27.976927
amu[14029]=28.976495
amu[14030]=29.973770
amu[15031]=30.973762
amu[16032]=31.972071
amu[16033]=32.971458
amu[16034]=33.967867
amu[16036]=35.967081
amu[17035]=34.968853
amu[17037]=36.965903
amu[18036]=35.967546
amu[18038]=37.962732
amu[18040]=39.962383
amu[19039]=38.963707
amu[19040]=39.963999
amu[19041]=40.961826
amu[20040]=39.962591
amu[20042]=41.958618
amu[20043]=42.958767
amu[20044]=43.955481
amu[20046]=45.953693
amu[20048]=47.952534
amu[21045]=44.955910
amu[22046]=45.952629
amu[22047]=46.951764
amu[22048]=47.947947
amu[22049]=48.947871
amu[22050]=49.944792
amu[23050]=49.947163
amu[23051]=50.943964
amu[24050]=49.946050
amu[24052]=51.940512
amu[24053]=52.940654
amu[24054]=53.938885
amu[25055]=54.938050
amu[26054]=53.939615
amu[26056]=55.934942
amu[26057]=56.935399
amu[26058]=57.933280
amu[27059]=58.933200
amu[28058]=57.935348
amu[28060]=59.930791
amu[28061]=60.931060
amu[28062]=61.928349
amu[28064]=63.927970
amu[29063]=62.929601
amu[29065]=64.927794
amu[30064]=63.929147
amu[30066]=65.926037
amu[30067]=66.927131
amu[30068]=67.924848
amu[30070]=69.925325
amu[31069]=68.925581
amu[31071]=70.924705
amu[32070]=69.924250
amu[32072]=71.922076
amu[32073]=72.923459
amu[32074]=73.921178
amu[32076]=75.921403
amu[33075]=74.921596
amu[34074]=73.922477
amu[34076]=75.919214
amu[34077]=76.919915
amu[34078]=77.917310
amu[34080]=79.916522
amu[34082]=81.916700
amu[35079]=78.918338
amu[35081]=80.916291
amu[36078]=77.920386
amu[36080]=79.916378
amu[36082]=81.913485
amu[36083]=82.914136
amu[36084]=83.911507
amu[36086]=85.910610
amu[37085]=84.911789
amu[37087]=86.909183
amu[38084]=83.913425
amu[38086]=85.909262
amu[38087]=86.908879
amu[38088]=87.905614
amu[39089]=88.905848
amu[40090]=89.904704
amu[40091]=90.905645
amu[40092]=91.905040
amu[40094]=93.906316
amu[40096]=95.908276
amu[41093]=92.906378
amu[42092]=91.906810
amu[42094]=93.905088
amu[42095]=94.905841
amu[42096]=95.904679
amu[42097]=96.906021
amu[42098]=97.905408
amu[42100]=99.907477
amu[43098]=97.907216
amu[44096]=95.907598
amu[44098]=97.905287
amu[44099]=98.905939
amu[44100]=99.904220
amu[44101]=100.905582
amu[44102]=101.904350
amu[44104]=103.905430
amu[45103]=102.905504
amu[46102]=101.905608
amu[46104]=103.904035
amu[46105]=104.905084
amu[46106]=105.903483
amu[46108]=107.903894
amu[46110]=109.905152
amu[47107]=106.905093
amu[47109]=108.904756
amu[48106]=105.906458
amu[48108]=107.904183
amu[48110]=109.903006
amu[48111]=110.904182
amu[48112]=111.902757
amu[48113]=112.904401
amu[48114]=113.903358
amu[48116]=115.904755
amu[49113]=112.904061
amu[49115]=114.903878
amu[50112]=111.904821
amu[50114]=113.902782
amu[50115]=114.903346
amu[50116]=115.901744
amu[50117]=116.902954
amu[50118]=117.901606
amu[50119]=118.903309
amu[50120]=119.902197
amu[50122]=121.903440
amu[50124]=123.905275
amu[51121]=120.903818
amu[51123]=122.904216
amu[52120]=119.904020
amu[52122]=121.903047
amu[52123]=122.904273
amu[52124]=123.902819
amu[52125]=124.904425
amu[52126]=125.903306
amu[52128]=127.904461
amu[52130]=129.906223
amu[53127]=126.904468
amu[54124]=123.905896
amu[54126]=125.904269
amu[54128]=127.903530
amu[54129]=128.904779
amu[54130]=129.903508
amu[54131]=130.905082
amu[54132]=131.904154
amu[54134]=133.905395
amu[54136]=135.907220
amu[55133]=132.905447
amu[56130]=129.906310
amu[56132]=131.905056
amu[56134]=133.904503
amu[56135]=134.905683
amu[56136]=135.904570
amu[56137]=136.905821
amu[56138]=137.905241
amu[57138]=137.907107
amu[57139]=138.906348
amu[58136]=135.907144
amu[58138]=137.905986
amu[58140]=139.905434
amu[58142]=141.909240
amu[59141]=140.907648
amu[60142]=141.907719
amu[60143]=142.909810
amu[60144]=143.910083
amu[60145]=144.912569
amu[60146]=145.913112
amu[60148]=147.916889
amu[60150]=149.920887
amu[61145]=144.912744
amu[62144]=143.911995
amu[62147]=146.914893
amu[62148]=147.914818
amu[62149]=148.917180
amu[62150]=149.917271
amu[62152]=151.919728
amu[62154]=153.922205
amu[63151]=150.919846
amu[63153]=152.921226
amu[64152]=151.919788
amu[64154]=153.920862
amu[64155]=154.922619
amu[64156]=155.922120
amu[64157]=156.923957
amu[64158]=157.924101
amu[64160]=159.927051
amu[65159]=158.925343
amu[66156]=155.924278
amu[66158]=157.924405
amu[66160]=159.925194
amu[66161]=160.926930
amu[66162]=161.926795
amu[66163]=162.928728
amu[66164]=163.929171
amu[67165]=164.930319
amu[68162]=161.928775
amu[68164]=163.929197
amu[68166]=165.930290
amu[68167]=166.932045
amu[68168]=167.932368
amu[68170]=169.935460
amu[69169]=168.934211
amu[70168]=167.933894
amu[70170]=169.934759
amu[70171]=170.936322
amu[70172]=171.936378
amu[70173]=172.938207
amu[70174]=173.938858
amu[70176]=175.942568
amu[71175]=174.940768
amu[71176]=175.942682
amu[72174]=173.940040
amu[72176]=175.941402
amu[72177]=176.943220
amu[72178]=177.943698
amu[72179]=178.945815
amu[72180]=179.946549
amu[73180]=179.947466
amu[73181]=180.947996
amu[74180]=179.946706
amu[74182]=181.948206
amu[74183]=182.950224
amu[74184]=183.950933
amu[74186]=185.954362
amu[75185]=184.952956
amu[75187]=186.955751
amu[76184]=183.952491
amu[76186]=185.953838
amu[76187]=186.955748
amu[76188]=187.955836
amu[76189]=188.958145
amu[76190]=189.958445
amu[76192]=191.961479
amu[77191]=190.960591
amu[77193]=192.962924
amu[78190]=189.959930
amu[78192]=191.961035
amu[78194]=193.962664
amu[78195]=194.964774
amu[78196]=195.964935
amu[78198]=197.967876
amu[79197]=196.966552
amu[80196]=195.965815
amu[80198]=197.966752
amu[80199]=198.968262
amu[80200]=199.968309
amu[80201]=200.970285
amu[80202]=201.970626
amu[80204]=203.973476
amu[81203]=202.972329
amu[81205]=204.974412
amu[82204]=203.973029
amu[82206]=205.974449
amu[82207]=206.975881
amu[82208]=207.976636
amu[83209]=208.980383
amu[90232]=232.038050
amu[91232]=231.035879
amu[92234]=234.040946
amu[92235]=235.043923
amu[92238]=238.050783

#
# natural compositions of a few elements, indexed by ZAID
# ratios: https://www.ncsu.edu/chemistry/msf/pdf/IsotopicMass_NaturalAbundance.pdf
# densities: http://www.angstromsciences.com/density-elements-chart
#
# hydrogen
H=mixture('H')
H.atom_fractions[1001]=99.9885
H.atom_fractions[1002]= 0.0115
H.mass_density=0.00008988
H.finalize()

# helium
He=mixture('He')
He.atom_fractions[2003]=0.00000137
He.atom_fractions[2004]=0.99999863
He.mass_density=0.00018
He.finalize()


# helium
He3=mixture('He3')
He3.atom_fractions[2003]=1
He3.mass_density=0.0001248
He3.finalize()

# lithium
Li=mixture('Li')
Li.atom_fractions[3006]=7.59
Li.atom_fractions[3007]=92.41
Li.mass_density=0.53
Li.finalize()

# beryllium
Be=mixture('Be')
Be.atom_fractions[4009]=1.0
Be.mass_density=1.85
Be.finalize()

# boron
B=mixture('B')
B.atom_fractions[5010]=19.9
B.atom_fractions[5011]=80.1
B.mass_density=2.34
B.finalize()

# carbon
C=mixture('C')
C.atom_fractions[6012]=98.93
C.atom_fractions[6013]=1.07
C.mass_density=2.26
C.finalize()

# nitrogen
N=mixture('N')
N.atom_fractions[7014]=99.632
N.atom_fractions[7015]=0.368
N.mass_density=0.00125
N.finalize()

# oxygen
O=mixture('O')
O.atom_fractions[8016]=99.757
O.atom_fractions[8017]=0.038
O.atom_fractions[8018]=0.205
O.mass_density=0.00143
O.finalize()

# fluorine
F=mixture('F')
F.atom_fractions[9019]=1.0
F.mass_density=0.00170
F.finalize()

# neon
Ne=mixture('Ne')
Ne.atom_fractions[10020]=90.48
Ne.atom_fractions[10021]=0.27
Ne.atom_fractions[10022]=9.25
Ne.mass_density=0.0009
Ne.finalize()

# sodium
Na=mixture('Na')
Na.atom_fractions[11023]=1.0
Na.mass_density=0.971
Na.finalize()

# magnesium
Mg=mixture('Mg')
Mg.atom_fractions[12024]=78.99
Mg.atom_fractions[12025]=10.00
Mg.atom_fractions[12026]=11.01
Mg.mass_density=1.738
Mg.finalize()

# aluminum
Al=mixture('Al')
Al.atom_fractions[13027]=1.0
Al.mass_density=2.702
Al.finalize()

# silicon
Si=mixture('Si')
Si.atom_fractions[14028]=92.2297
Si.atom_fractions[14029]=4.6832 
Si.atom_fractions[14030]=3.0872 
Si.mass_density=2.33
Si.finalize()

# phosphorous
P=mixture('P')
P.atom_fractions[15031]=1.0
P.mass_density=1.82
P.finalize()

# sulphur
S=mixture('S')
S.atom_fractions[16032]=94.93
S.atom_fractions[16033]=0.76
S.atom_fractions[16034]=4.29
S.atom_fractions[16036]=0.02
S.mass_density=2.07
S.finalize()

# chlorine
Cl=mixture('Cl')
Cl.atom_fractions[17035]=75.78
Cl.atom_fractions[17037]=24.22
Cl.mass_density=0.003214
Cl.finalize()

# argon
Ar=mixture('Ar')
Ar.atom_fractions[18036]=0.3365 
Ar.atom_fractions[18038]=0.0632 
Ar.atom_fractions[18040]=99.6003 
Ar.mass_density=0.0017824
Ar.finalize()

# potassium
K=mixture('K')
K.atom_fractions[19039]=93.2581 
K.atom_fractions[19040]=0.0117  
K.atom_fractions[19041]=6.7302  
K.mass_density=0.862
K.finalize()

# calcium
Ca=mixture('Ca')
Ca.atom_fractions[20040]=96.941
Ca.atom_fractions[20042]=0.647 
Ca.atom_fractions[20043]=0.135 
Ca.atom_fractions[20044]=2.086 
Ca.atom_fractions[20046]=0.004 
Ca.atom_fractions[20048]=0.187 
Ca.mass_density=1.55
Ca.finalize()

# scandium
Sc=mixture('Sc')
Sc.atom_fractions[21045]=1.0
Sc.mass_density=2.99
Sc.finalize()

# titanium
Ti=mixture('Ti')
Ti.atom_fractions[22046]=8.25 
Ti.atom_fractions[22047]=7.44 
Ti.atom_fractions[22048]=73.72
Ti.atom_fractions[22049]=5.41 
Ti.atom_fractions[22050]=5.18 
Ti.mass_density=4.54
Ti.finalize()

# vanadium
V=mixture('V')
V.atom_fractions[23050]=0.250 
V.atom_fractions[23051]=99.750
V.mass_density=6.11
V.finalize()

# chromium
Cr=mixture('Cr')
Cr.atom_fractions[24050]=4.345 
Cr.atom_fractions[24052]=83.789
Cr.atom_fractions[24053]=9.501 
Cr.atom_fractions[24054]=2.365 
Cr.mass_density=7.19
Cr.finalize()

# manganese
Mn=mixture('Mn')
Mn.atom_fractions[25055]=1.0
Mn.mass_density=7.43
Mn.finalize()

# iron
Fe=mixture('Fe')
Fe.atom_fractions[26054]=5.845 
Fe.atom_fractions[26056]=91.754
Fe.atom_fractions[26057]=2.119 
Fe.atom_fractions[26058]=0.282 
Fe.mass_density=7.874
Fe.finalize()

# cobalt
Co=mixture('Co')
Co.atom_fractions[27059]=1.0
Co.mass_density=8.9
Co.finalize()

# nickel
Ni=mixture('Ni')
Ni.atom_fractions[28058]=68.0769
Ni.atom_fractions[28060]=26.2231
Ni.atom_fractions[28061]=1.1399 
Ni.atom_fractions[28062]=3.6345 
Ni.atom_fractions[28064]=0.9256 
Ni.mass_density=8.9
Ni.finalize()

# copper
Cu=mixture('Cu')
Cu.atom_fractions[29063]=69.17
Cu.atom_fractions[29065]=30.83
Cu.mass_density=8.96
Cu.finalize()

# zinc
Zn=mixture('Zn')
Zn.atom_fractions[30064]=48.63
Zn.atom_fractions[30066]=27.90
Zn.atom_fractions[30067]=4.10 
Zn.atom_fractions[30068]=18.75
Zn.atom_fractions[30070]=0.62 
Zn.mass_density=7.13
Zn.finalize()

# gallium
Ga=mixture('Ga')
Ga.atom_fractions[31069]=60.108
Ga.atom_fractions[31071]=39.892
Ga.mass_density=5.907
Ga.finalize()

# germanium
Ge=mixture('Ge')
Ge.atom_fractions[32070]=20.84
Ge.atom_fractions[32072]=27.54
Ge.atom_fractions[32073]=7.73 
Ge.atom_fractions[32074]=36.28
Ge.atom_fractions[32076]=7.61 
Ge.mass_density=5.323
Ge.finalize()

# arsenic
As=mixture('As')
As.atom_fractions[33075]=1.0
As.mass_density=5.72
As.finalize()

# selenium
Se=mixture('Se')
Se.atom_fractions[34074]=0.89 
Se.atom_fractions[34076]=9.37 
Se.atom_fractions[34077]=7.63 
Se.atom_fractions[34078]=23.77
Se.atom_fractions[34080]=49.61
Se.atom_fractions[34082]=8.73 
Se.mass_density=4.79
Se.finalize()

# bromine
Br=mixture('Br')
Br.atom_fractions[35079]=50.69
Br.atom_fractions[35081]=49.31
Br.mass_density=3.119
Br.finalize()

# krypton
Kr=mixture('Kr')
Kr.atom_fractions[36078]=0.35
Kr.atom_fractions[36080]=2.28
Kr.atom_fractions[36082]=11.58
Kr.atom_fractions[36083]=11.49
Kr.atom_fractions[36084]=57.00
Kr.atom_fractions[36086]=17.30
Kr.mass_density=0.00375
Kr.finalize()

# rubidium
Rb=mixture('Rb')
Rb.atom_fractions[37085]=72.17
Rb.atom_fractions[37087]=27.83
Rb.mass_density=1.63
Rb.finalize()

# strontium
Sr=mixture('Sr')
Sr.atom_fractions[38084]=0.56
Sr.atom_fractions[38086]=9.86
Sr.atom_fractions[38087]=7.00
Sr.atom_fractions[38088]=82.58
Sr.mass_density=2.54
Sr.finalize()

# yttrium
Y=mixture('Y')
Y.atom_fractions[39089]=1.0
Y.mass_density=4.47
Y.finalize()

# zirconium
Zr=mixture('Zr')
Zr.atom_fractions[40090]=51.45
Zr.atom_fractions[40091]=11.22
Zr.atom_fractions[40092]=17.15
Zr.atom_fractions[40094]=17.38
Zr.atom_fractions[40096]=2.80
Zr.mass_density=6.51
Zr.finalize()

# niobium
Nb=mixture('Nb')
Nb.atom_fractions[41093]=1.0
Nb.mass_density=8.57
Nb.finalize()

# molybdenum
Mo=mixture('Mo')
Mo.atom_fractions[42092]=14.84
Mo.atom_fractions[42094]=9.25
Mo.atom_fractions[42095]=15.92
Mo.atom_fractions[42096]=16.68
Mo.atom_fractions[42097]=9.55
Mo.atom_fractions[42098]=24.13
Mo.atom_fractions[42100]=9.63
Mo.mass_density=10.22
Mo.finalize()

# technetium
Tc=mixture('Tc')
Tc.atom_fractions[43098]=1.0
Tc.mass_density=11.5
Tc.finalize()

# Ruthenium
Ru=mixture('Ru')
Ru.atom_fractions[44096]=5.54
Ru.atom_fractions[44098]=1.87
Ru.atom_fractions[44099]=12.76
Ru.atom_fractions[44100]=12.60
Ru.atom_fractions[44101]=17.06
Ru.atom_fractions[44102]=31.55
Ru.atom_fractions[44104]=18.62
Ru.mass_density=12.37
Ru.finalize()

# Rhodium
Rh=mixture('Rh')
Rh.atom_fractions[45103]=1.0
Rh.mass_density=12.41
Rh.finalize()

# Palladium
Pd=mixture('Pd')
Pd.atom_fractions[46102]=1.02
Pd.atom_fractions[46104]=11.14
Pd.atom_fractions[46105]=22.33
Pd.atom_fractions[46106]=27.33
Pd.atom_fractions[46108]=26.46
Pd.atom_fractions[46110]=11.72
Pd.mass_density=12.02
Pd.finalize()

# Silver
Ag=mixture('Ag')
Ag.atom_fractions[47107]=51.839
Ag.atom_fractions[47109]=48.161
Ag.mass_density=10.5
Ag.finalize()

# Cadmium
Cd=mixture('Cd')
Cd.atom_fractions[48106]=1.25
Cd.atom_fractions[48108]=0.89
Cd.atom_fractions[48110]=12.49
Cd.atom_fractions[48111]=12.80
Cd.atom_fractions[48112]=24.13
Cd.atom_fractions[48113]=12.22
Cd.atom_fractions[48114]=28.73
Cd.atom_fractions[48116]=7.49
Cd.mass_density=8.65
Cd.finalize()

# Indium
In=mixture('In')
In.atom_fractions[49113]=4.29
In.atom_fractions[49115]=95.71
In.mass_density=7.31
In.finalize()

# Tin
Sn=mixture('Sn')
Sn.atom_fractions[50112]=0.97
Sn.atom_fractions[50114]=0.66
Sn.atom_fractions[50115]=0.34
Sn.atom_fractions[50116]=14.54
Sn.atom_fractions[50117]=7.68
Sn.atom_fractions[50118]=24.22
Sn.atom_fractions[50119]=8.59
Sn.atom_fractions[50120]=32.58
Sn.atom_fractions[50122]=4.63
Sn.atom_fractions[50124]=5.79
Sn.mass_density=7.31
Sn.finalize()

# Antimony
Sb=mixture('Sb')
Sb.atom_fractions[51121]=57.21
Sb.atom_fractions[51123]=42.79
Sb.mass_density=6.684
Sb.finalize()

# Tellurium
Te=mixture('Te')
Te.atom_fractions[52120]=0.09
Te.atom_fractions[52122]=2.55
Te.atom_fractions[52123]=0.89
Te.atom_fractions[52124]=4.74
Te.atom_fractions[52125]=7.07
Te.atom_fractions[52126]=18.84
Te.atom_fractions[52128]=31.74
Te.atom_fractions[52130]=34.08
Te.mass_density=6.25
Te.finalize()

# Iodine
I=mixture('I')
I.atom_fractions[53127]=1.0
I.mass_density=4.93
I.finalize()

# Xenon
Xe=mixture('Xe')
Xe.atom_fractions[54124]=0.09
Xe.atom_fractions[54126]=0.09
Xe.atom_fractions[54128]=1.92
Xe.atom_fractions[54129]=26.44
Xe.atom_fractions[54130]=4.08
Xe.atom_fractions[54131]=21.18
Xe.atom_fractions[54132]=26.89
Xe.atom_fractions[54134]=10.44
Xe.atom_fractions[54136]=8.87
Xe.mass_density=0.0059
Xe.finalize()

# Cesium
Cs=mixture('Cs')
Cs.atom_fractions[55133]=1.0
Cs.mass_density=1.873
Cs.finalize()

# Barium
Ba=mixture('Ba')
Ba.atom_fractions[56130]=0.106
Ba.atom_fractions[56132]=0.101
Ba.atom_fractions[56134]=2.417
Ba.atom_fractions[56135]=6.592
Ba.atom_fractions[56136]=7.854
Ba.atom_fractions[56137]=11.232
Ba.atom_fractions[56138]=71.698
Ba.mass_density=3.59
Ba.finalize()

# Lanthanum
La=mixture('La')
La.atom_fractions[57138]=0.090
La.atom_fractions[57139]=99.910
La.mass_density=6.15
La.finalize()

# Cerium
Ce=mixture('Ce')
Ce.atom_fractions[58136]=0.185
Ce.atom_fractions[58138]=0.251
Ce.atom_fractions[58140]=88.450
Ce.atom_fractions[58142]=11.114
Ce.mass_density=6.77
Ce.finalize()

# Praseodymium
Pr=mixture('Pr')
Pr.atom_fractions[59141]=1.0
Pr.mass_density=6.77
Pr.finalize()

# Neodymium
Nd=mixture('Nd')
Nd.atom_fractions[60142]=27.2
Nd.atom_fractions[60143]=12.2
Nd.atom_fractions[60144]=23.8
Nd.atom_fractions[60145]=8.3
Nd.atom_fractions[60146]=17.2
Nd.atom_fractions[60148]=5.7
Nd.atom_fractions[60150]=5.6
Nd.mass_density=7.01
Nd.finalize()

# Promethium
Pm=mixture('Pm')
Pm.atom_fractions[61145]=1.0
Pm.mass_density=7.3
Pm.finalize()

# Samarium
Sm=mixture('Sm')
Sm.atom_fractions[62144]=3.07
Sm.atom_fractions[62147]=14.99
Sm.atom_fractions[62148]=11.24
Sm.atom_fractions[62149]=13.82
Sm.atom_fractions[62150]=7.38
Sm.atom_fractions[62152]=26.75
Sm.atom_fractions[62154]=22.75
Sm.mass_density=7.52
Sm.finalize()

# Europium
Eu=mixture('Eu')
Eu.atom_fractions[63151]=47.81
Eu.atom_fractions[63153]=52.19
Eu.mass_density=5.24
Eu.finalize()

# Gadolinium
Gd=mixture('Gd')
Gd.atom_fractions[64152]=0.20
Gd.atom_fractions[64154]=2.18
Gd.atom_fractions[64155]=14.80
Gd.atom_fractions[64156]=20.47
Gd.atom_fractions[64157]=15.65
Gd.atom_fractions[64158]=24.84
Gd.atom_fractions[64160]=21.86
Gd.mass_density=7.895
Gd.finalize()

# Terbium
Tb=mixture('Tb')
Tb.atom_fractions[65159]=1.0
Tb.mass_density=8.23
Tb.finalize()

# Dysprosium
Dy=mixture('Dy')
Dy.atom_fractions[66156]=0.06
Dy.atom_fractions[66158]=0.10
Dy.atom_fractions[66160]=2.34
Dy.atom_fractions[66161]=18.91
Dy.atom_fractions[66162]=25.51
Dy.atom_fractions[66163]=24.90
Dy.atom_fractions[66164]=28.18
Dy.mass_density=8.55
Dy.finalize()

# Holmium
Ho=mixture('Ho')
Ho.atom_fractions[67165]=1.0
Ho.mass_density=8.8
Ho.finalize()

# Erbium
Er=mixture('Er')
Er.atom_fractions[68162]=0.14
Er.atom_fractions[68164]=1.61
Er.atom_fractions[68166]=33.61
Er.atom_fractions[68167]=22.93
Er.atom_fractions[68168]=26.78
Er.atom_fractions[68170]=14.93
Er.mass_density=9.07
Er.finalize()

# Thulium
Tm=mixture('Tm')
Tm.atom_fractions[69169]=1.0
Tm.mass_density=9.32
Tm.finalize()

# Ytterbium
Yb=mixture('Yb')
Yb.atom_fractions[70168]=0.13
Yb.atom_fractions[70170]=3.04
Yb.atom_fractions[70171]=14.28
Yb.atom_fractions[70172]=21.83
Yb.atom_fractions[70173]=16.13
Yb.atom_fractions[70174]=31.83
Yb.atom_fractions[70176]=12.76
Yb.mass_density=6.9
Yb.finalize()

# Lutetium
Lu=mixture('Lu')
Lu.atom_fractions[71175]=97.41
Lu.atom_fractions[71176]=2.59
Lu.mass_density=9.84
Lu.finalize()

# Hafnium
Hf=mixture('Hf')
Hf.atom_fractions[72174]=0.16
Hf.atom_fractions[72176]=5.26
Hf.atom_fractions[72177]=18.60
Hf.atom_fractions[72178]=27.28
Hf.atom_fractions[72179]=13.62
Hf.atom_fractions[72180]=35.08
Hf.mass_density=13.31
Hf.finalize()

# Tantalum
Ta=mixture('Ta')
Ta.atom_fractions[73180]=0.012
Ta.atom_fractions[73181]=99.988
Ta.mass_density=16.65
Ta.finalize()

# Tungsten
W=mixture('W')
W.atom_fractions[74180]=0.12
W.atom_fractions[74182]=26.50
W.atom_fractions[74183]=14.31
W.atom_fractions[74184]=30.64
W.atom_fractions[74186]=28.43
W.mass_density=19.35
W.finalize()

# Rhenium
Re=mixture('Re')
Re.atom_fractions[75185]=37.40
Re.atom_fractions[75187]=62.60
Re.mass_density=21.04
Re.finalize()

# Osmium
Os=mixture('Os')
Os.atom_fractions[76184]=0.02
Os.atom_fractions[76186]=1.59
Os.atom_fractions[76187]=1.96
Os.atom_fractions[76188]=13.24
Os.atom_fractions[76189]=16.15
Os.atom_fractions[76190]=26.26
Os.atom_fractions[76192]=40.78
Os.mass_density=22.6
Os.finalize()

# Iridium
Ir=mixture('Ir')
Ir.atom_fractions[77191]=37.3
Ir.atom_fractions[77193]=62.7
Ir.mass_density=22.4
Ir.finalize()

# Platinum
Pt=mixture('Pt')
Pt.atom_fractions[78190]=0.014
Pt.atom_fractions[78192]=0.782
Pt.atom_fractions[78194]=32.967
Pt.atom_fractions[78195]=33.832
Pt.atom_fractions[78196]=25.242
Pt.atom_fractions[78198]=7.163
Pt.mass_density=21.45
Pt.finalize()

# Gold
Au=mixture('Au')
Au.atom_fractions[79197]=1.0
Au.mass_density=19.32
Au.finalize()

# Mercury
Hg=mixture('Hg')
Hg.atom_fractions[80196]=0.15
Hg.atom_fractions[80198]=9.97
Hg.atom_fractions[80199]=16.87
Hg.atom_fractions[80200]=23.10
Hg.atom_fractions[80201]=13.18
Hg.atom_fractions[80202]=29.86
Hg.atom_fractions[80204]=6.87
Hg.mass_density=13.546
Hg.finalize()

# Thallium
Tl=mixture('Tl')
Tl.atom_fractions[81203]=29.524
Tl.atom_fractions[81205]=70.476
Tl.mass_density=11.85
Tl.finalize()

# Lead
Pb=mixture('Pb')
Pb.atom_fractions[82204]=1.4
Pb.atom_fractions[82206]=24.1
Pb.atom_fractions[82207]=22.1
Pb.atom_fractions[82208]=52.4
Pb.mass_density=11.35
Pb.finalize()

# Bismuth
Bi=mixture('Bi')
Bi.atom_fractions[83209]=1.0
Bi.mass_density=9.75
Bi.finalize()

# Thorium
Th=mixture('Th')
Th.atom_fractions[90232]=1.0
Th.mass_density=11.724
Th.finalize()

# Protactinium
Pa=mixture('Pa')
Pa.atom_fractions[91232]=1.0
Pa.mass_density=15.4
Pa.finalize()

# Uranium
U=mixture('U')
U.atom_fractions[92234]=0.0055
U.atom_fractions[92235]=0.7200
U.atom_fractions[92238]=99.2745
U.mass_density=18.95
U.finalize()