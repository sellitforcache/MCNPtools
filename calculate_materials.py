verbose = 0

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


class element(object):

	_elements = {}

	def __new__(cls,name):
		if not isinstance(name,int):
			if isinstance(name,str):
				name = name.strip()
			if name in z_number:
				name = z_number[name]
			else:
				print "input is not a integer or in the element symbol dictionary.  rejected."
				return None
		if name in element._elements.keys():
			print "element %d already exists in the class list.  rejected."%name
			return None
		# must follow ZZZ000 naming?
		if name%1000:
			print "input of %d does not follow ZZZ000 naming for 'natural' isotopes"%name
			return None
		# else return a new instance
		return super(element,cls).__new__(cls)

	def __init__(self,name):
		import copy
		if isinstance(name,str):
			name = name.strip()
		if name in z_number:
			self.name 		= copy.deepcopy(z_number[name])
		else:
			self.name 		= copy.deepcopy(name)
		self.n_isotopes		= 0
		self.mode 			= 'none'
		self.avg_amu 		= 0.0
		self.atom_fractions	= {}
		self.mass_fractions	= {}

	def add_isotope_atom(self,mass_num,amu,frac):
		if not isinstance(mass_num,int):
			print "first input is not an int mass number.  rejected."
			return
		if not isinstance(frac,float):
			print "second input is not a float atomic fraction.  rejected."
			return
		if not isinstance(amu,float):
			print "third input is not a float amu number.  rejected."
			return
		if self.mode not in ['atom','none']:
			if verbose: print "element object is in %s mode.  delete and start over in atom mode."%self.mode
		self.mode 								= 'atom'
		self.atom_fractions[mass_num+self.name]	= [amu,frac]
		self.n_isotopes 						= self.n_isotopes + 1
		if verbose: print "added isotope %6d with amu %12.8f and atom fraction %15.8f into element %6d"%(mass_num+self.name,amu,frac,self.name)

	def add_isotope_mass(self,mass_num,amu,frac):
		if not isinstance(mass_num,int):
			print "first input is not an int mass number.  rejected."
			return
		if not isinstance(frac,float):
			print "second input is not a float mass fraction.  rejected."
			return
		if not isinstance(amu,float):
			print "third input is not a float amu number.  rejected."
			return
		if self.mode not in ['mass','none']:
			print "element object is in %s mode.   delete and start over in mass mode."%self.mode
			return
		self.mode 								= 'mass'
		self.mass_fractions[mass_num+self.name]	= [amu,frac]
		self.n_isotopes 						= self.n_isotopes + 1
		if verbose: print "added isotope %6d with amu %12.8f and mass fraction %15.8f into element %6d"%(mass_num+self.name,amu,frac,self.name)

	def delete(self):
		element._elements.pop(self.name, None)
		self.__init__(self.name)
		if verbose: print "removed element %s from the class dictionary and re-initialized all data.  the instance has not necessarily been deleted from the python namespace yet!"%self.name

	def finalize(self):
		import numpy
		if self.mode == 'atom':
			# sum the fractions, renormalize
			frac_total = 0.0
			for isotope in self.atom_fractions.keys():
				frac_total = frac_total + self.atom_fractions[isotope][1]
			for isotope in self.atom_fractions.keys():
				self.atom_fractions[isotope] = [self.atom_fractions[isotope][0] , self.atom_fractions[isotope][1] / frac_total]
			# calculate averge amu from atom fractions
			self.avg_amu = 0.0 
			for isotope in self.atom_fractions.keys():
				self.avg_amu = self.avg_amu + self.atom_fractions[isotope][0]*self.atom_fractions[isotope][1]
			# calculate the mass factions
			for isotope in self.atom_fractions.keys():
				mass_frac = self.atom_fractions[isotope][0] * self.atom_fractions[isotope][1] / self.avg_amu
				self.mass_fractions[isotope] = [self.atom_fractions[isotope][0] , mass_frac]
		elif self.mode == 'mass':
			# sum the fractions, renormalize
			frac_total = 0.0
			for isotope in self.mass_fractions.keys():
				frac_total = frac_total + self.mass_fractions[isotope][1]
			for isotope in self.mass_fractions.keys():
				self.mass_fractions[isotope] = [self.mass_fractions[isotope][0] , self.mass_fractions[isotope][1] / frac_total]
			# calculate averge amu from mass fractions
			self.avg_amu = 0.0 
			for isotope in self.atom_fractions.keys():
				self.avg_amu = self.avg_amu + self.mass_fractions[isotope][1]/self.mass_fractions[isotope][0]
			self.avg_amu = 1.0 / self.avg_amu
			# calculate the atom factions
			for isotope in self.mass_fractions.keys():
				atom_frac = self.avg_amu * self.mass_fractions[isotope][1] / self.mass_fractions[isotope][0]
				self.atom_fractions[isotope] = [self.mass_fractions[isotope][0] , atom_frac]
		elif self.mode == 'finalized':
			print "already finalized."
			return
		else:
			print "uninitialized!  cannot finalize."
			return

		if verbose: print "added element %6d to the class dictionary."%self.name
		self.mode = 'finalized'
		element._elements[self.name] = self



#
#  material class for a rod
#
class material(object):

	_materials = {}

	def __new__(cls,name,den):
		if not isinstance(name,str):
			print "first input is not a string.  rejected."
			return None
		if not isinstance(den,float):
			print "second input is not a float.  rejected."
			return None
		name = name.strip()
		if name in material._materials.keys():
			print "material %s already exists in the class list.  rejected."%name
			return None
		# else return a new instance
		return super(material,cls).__new__(cls)

	def __init__(self,name,den):
		import copy
		self.name 			= copy.deepcopy(name.strip())
		self.n_elements		= 0
		self.density 		= copy.deepcopy(den)
		self.avg_amu 		= 0.0
		self.mode 			= 'none'
		self.atom_fractions	= {}
		self.mass_fractions	= {}

	def add_element_atom(self,name,frac):
		if not isinstance(name,int):
			if isinstance(name,str):
				name = name.strip()
			if name in z_number:
				name = z_number[name]
			else:
				print "first input is not an int or in the element symbol dictionary.  rejected."
				return
		if not isinstance(frac,float):
			print "second input is not a float.  rejected."
			return
		if not name in element._elements.keys():
			print "element %d is not in the element class dictionary.  rejected."%name
			return
		if self.mode not in ['atom','none']:
			print "material object is in %s mode.   delete and start over in atom mode."%self.mode
			return
		self.mode = 'atom'
		self.atom_fractions[name]	= frac
		self.n_elements				= self.n_elements + 1
		if verbose: print "added element %6d with atom fraction %15.8f into material %s"%(name,frac,self.name)

	def add_element_mass(self,name,frac):
		if not isinstance(name,int):
			if isinstance(name,str):
				name = name.strip()
			if name in z_number:
				name = z_number[name]
			else:
				print "first input is not an int or in the element symbol dictionary.  rejected."
				return
		if not isinstance(frac,float):
			print "second input is not a float.  rejected."
			return
		if not name in element._elements.keys():
			print "element %d is not in the element class dictionary.  rejected."%name
			return
		if self.mode not in ['mass','none']:
			print "material object is in %s mode.   delete and start over in mass mode."%self.mode
			return
		self.mode = 'mass'
		self.mass_fractions[name]	= frac
		self.n_elements				= self.n_elements + 1
		if verbose: print "added element %6d with mass fraction %15.8f into material %s"%(name,frac,self.name)

	def delete(self):
		material._materials.pop(self.name, None)
		self.__init__(self.name)
		if verbose: print "removed material %s from the class dictionary and re-initialized all data.  the instance has not necessarily been deleted from the python namespace yet!"%self.name

	def finalize(self):
		import numpy
		if self.mode == 'atom':
			# sum the fractions, renormalize
			frac_total = 0.0
			for e in self.atom_fractions.keys():
				frac_total = frac_total + self.atom_fractions[e]
			for e in self.atom_fractions.keys():
				self.atom_fractions[e] = self.atom_fractions[e] / frac_total
			# calculate averge amu from atom fractions
			self.avg_amu = 0.0 
			for e in self.atom_fractions.keys():
				self.avg_amu = self.avg_amu + self.atom_fractions[e]*element._elements[e].avg_amu
			# calculate the mass factions
			for e in self.atom_fractions.keys():
				self.mass_fractions[e] = self.atom_fractions[e]*element._elements[e].avg_amu / self.avg_amu
		elif self.mode == 'mass':
			# sum the fractions, renormalize
			frac_total = 0.0
			for e in self.mass_fractions.keys():
				frac_total = frac_total + self.mass_fractions[e]
			for e in self.mass_fractions.keys():
				self.mass_fractions[e] = self.mass_fractions[e] / frac_total
			# calculate averge amu from mass fractions
			self.avg_amu = 0.0 
			for e in self.mass_fractions.keys():
				self.avg_amu = self.avg_amu + self.mass_fractions[e]/element._elements[e].avg_amu
			self.avg_amu = 1.0 / self.avg_amu
			# calculate the atom factions
			for e in self.mass_fractions.keys():
				self.atom_fractions[e] = self.avg_amu * self.mass_fractions[e] / element._elements[e].avg_amu
		elif self.mode == 'finalized':
			print "already finalized."
			return
		else:
			print "uninitialized!  cannot finalize."
			return

		if verbose: print "added material %s to the class dictionary."%self.name
		self.mode = 'finalized'
		material._materials[self.name] = self

	def print_material_card(self):

		atom_fractions_total = {}

		# init
		for e in self.atom_fractions.keys():
				for i in element._elements[e].atom_fractions.keys():
					atom_fractions_total[i] = 0.0
		# set
		for e in self.atom_fractions.keys():
				for i in element._elements[e].atom_fractions.keys():
					atom_fractions_total[i] = atom_fractions_total[i] + self.atom_fractions[e]*element._elements[e].atom_fractions[i][1]

		isotope_list_total = atom_fractions_total.keys()
		isotope_list_total.sort()

		print "c"
		print "c         %s"%self.name
		print "c"
		print "c         element     avg. amu     atom fraction    mass fraction"
		print "c         --------    --------     -------------    -------------"
		for e in self.atom_fractions.keys():
			print "c  %15s    %8.4f     %10.8f       %10.8f"%(e,element._elements[e].avg_amu,self.atom_fractions[e],self.mass_fractions[e])
		print "c"
		print "c         average amu     = %12.8f"%self.avg_amu
		print "c         density         =  %11.8f"%self.density
		print "c"
		for i in isotope_list_total:
			print "     %6d   %8.10E"%(i,atom_fractions_total[i])
		print "c"


class rod(object):

	_rods = {}

	def __new__(cls,name):
		if not isinstance(name,str):
			print "first input is not a string.  rejected."
			return None
		name = name.strip()
		if name in rod._rods.keys():
			print "rod %s already exists in the class list.  rejected."%name
			return None
		# else return a new instance
		return super(rod,cls).__new__(cls)

	def __init__(self,name):
		import copy
		self.name 			= copy.deepcopy(name.strip())
		self.n_materials	= 0
		self.avg_den 		= 0.0
		self.avg_amu 		= 0.0
		self.mass_total		= 0.0
		self.mode 			= 'none'
		self.vol_fractions	= {}
		self.atom_fractions	= {}
		self.mass_fractions	= {}

	def add_material_vol(self,name,frac):
		if not isinstance(name,str):
			print "first input is not an str.  rejected."
			return
		name = name.strip()
		if not isinstance(frac,float):
			print "second input is not a float.  rejected."
			return
		if not name in material._materials.keys():
			print "material %s is not in the material class dictionary.  rejected."%name
			return
		if self.mode not in ['volume','none']:
			print "material object is in %s mode.   delete and start over in atom mode."%self.mode
			return
		self.mode = 'volume'
		self.vol_fractions[name]	= frac
		self.n_materials			= self.n_materials + 1
		if verbose: print "added material %s with volume fraction %15.8f into rod %s"%(name,frac,self.name)

	def delete(self):
		rod._rods.pop(self.name, None)
		self.__init__(self.name)
		if verbose: print "removed rod %s from the class dictionary and re-initialized all data.  the instance has not necessarily been deleted from the python namespace yet!"%self.name

	def finalize(self):
		import numpy
		if self.mode == 'volume':
			# sum the fractions, renormalize
			frac_total = 0.0
			for m in self.vol_fractions.keys():
				frac_total = frac_total + self.vol_fractions[m]
			for m in self.vol_fractions.keys():
				self.vol_fractions[m] = self.vol_fractions[m] / frac_total
			# calculate averge density from volume fractions
			self.avg_den = 0.0 
			for m in self.vol_fractions.keys():
				self.avg_den = self.avg_den + self.vol_fractions[m]*material._materials[m].density
			# calculate the mass factions
			for m in self.vol_fractions.keys():
				self.mass_fractions[m] = self.vol_fractions[m]*material._materials[m].density / self.avg_den
			# calculate averge amu from mass fractions
			self.avg_amu = 0.0 
			for m in self.mass_fractions.keys():
				self.avg_amu = self.avg_amu + self.mass_fractions[m]/material._materials[m].avg_amu
			self.avg_amu = 1.0 / self.avg_amu
			# calculate the atom factions
			for m in self.mass_fractions.keys():
				self.atom_fractions[m] = self.mass_fractions[m] * self.avg_amu / material._materials[m].avg_amu
		elif self.mode == 'finalized':
			print "already finalized."
			return
		else:
			print "uninitialized!  cannot finalize."
			return

		if verbose: print "added rod %s to the class dictionary."%self.name
		self.mode = 'finalized'
		rod._rods[self.name] = self

	def print_material_card(self):

		atom_fractions_total = {}

		# init
		for m in self.atom_fractions.keys():
			for e in material._materials[m].atom_fractions.keys():
				for i in element._elements[e].atom_fractions.keys():
					atom_fractions_total[i] = 0.0
		# set
		for m in self.atom_fractions.keys():
			for e in material._materials[m].atom_fractions.keys():
				for i in element._elements[e].atom_fractions.keys():
					atom_fractions_total[i] = atom_fractions_total[i] + self.atom_fractions[m]*material._materials[m].atom_fractions[e]*element._elements[e].atom_fractions[i][1]

		isotope_list_total = atom_fractions_total.keys()
		isotope_list_total.sort()

		print "c"
		print "c         %s"%self.name
		print "c"
		print "c         material    density    avg. amu     volume fraction    atom fraction    mass fraction"
		print "c         --------    -------    --------     ---------------    -------------    -------------"
		for m in self.atom_fractions.keys():
			print "c  %15s    %7.4f   %8.4f      %10.8f         %10.8f       %10.8f"%(m,material._materials[m].density,material._materials[m].avg_amu,self.vol_fractions[m],self.atom_fractions[m],self.mass_fractions[m])
		print "c"
		print "c         average amu     = %12.8f"%self.avg_amu
		print "c         average density =  %11.8f"%self.avg_den
		print "c"
		for i in isotope_list_total:
			print "     %6d   %8.10E"%(i,atom_fractions_total[i])
		print "c"
