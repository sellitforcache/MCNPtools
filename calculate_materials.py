#! /home/l_bergmann/anaconda/bin/python -W ignore

from pyne import mcnp, ace
import math
import pylab, numpy, sys, cPickle, progressbar, copy
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
from MCNPtools.to_energy import to_energy
from MCNPtools.to_temperature import to_temperature
from MCNPtools.to_wavelength import to_wavelength
from MCNPtools.mctal import mctal
from MCNPtools.plot import plot
import scipy.special
import numpy.linalg

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=18)


#
# element class for materials
#
class element:

	_elements = {}

	def __init__(self,name):
		if !isinstance(name,int):
			print "input is not a integer.  rejected."
			return
		# must follow ZZZ000 naming?
		if name%1000:
			print "input of %d does not follow ZZZ000 naming for 'natural' isotopes"%name
		self.name 			= copy.deepcopy(name)
		self.n_isotopes		= 0
		self.mode 			= 'none'
		self.avg_amu 		= 0.0
		self.atom_fractions	= {}
		self.mass_fractions	= {}

	def add_isotope_atom(self,mass_num,amu,frac):
		if !isinstance(mass_num,int):
			print "first input is not an int mass number.  rejected."
			return
		if !isinstance(frac,float):
			print "second input is not a float atomic fraction.  rejected."
			return
		if !isinstance(amu,float):
			print "third input is not a float amu number.  rejected."
			return
		if mode not in ['atom','none']:
			print "element object is in %s mode.  delete and start over in atom mode."%self.mode
		self.mode 								= 'atom'
		self.atom_fractions[mass_num+self.name]	= [amu,frac]
		self.n_isotopes 						= self.n_isotopes + 1
		print "added isotope %d with amu %6.8f and atom fraction %6.8f in element %d"%(mass_num+self.name,amu,frac,self.name)


	def add_isotope_mass(self,mass_num,amu,frac):
		if !isinstance(mass_num,int):
			print "first input is not an int mass number.  rejected."
			return
		if !isinstance(frac,float):
			print "second input is not a float mass fraction.  rejected."
			return
		if !isinstance(amu,float):
			print "third input is not a float amu number.  rejected."
			return
		if mode not in ['mass','none']:
			print "element object is in %s mode.   delete and start over in mass mode."%self.mode
			return
		self.mode 								= 'mass'
		self.mass_fractions[mass_num+self.name]	= [amu,frac]
		self.n_isotopes 						= self.n_isotopes + 1
		print "added isotope %d with amu %6.8f and mass fraction %6.8f in element %d"%(mass_num+self.name,amu,frac,self.name)

	def finalize(self):
		if mode == 'atom':
			# sum the fractions, renormalize
			frac_total = 0.0
			for isotope in self.atom_fractions.keys():
				frac_total = frac_total + self.atom_fractions[isotope][1]
			for isotope in self.atom_fractions.keys():
				self.atom_fractions[isotope] = self.atom_fractions[isotope][1] / frac_total
			# calculate averge amu from atom fractions
			self.avg_amu = 0.0 
			for isotope in self.atom_fractions.keys():
				self.avg_amu = self.avg_amu + self.atom_fractions[isotope][0]*self.atom_fractions[isotope][1]
			# calculate the mass factions
			for isotope in self.atom_fractions.keys():
				mass_frac = self.atom_fractions[isotope][1] / self.avg_amu
				self.mass_fractions[isotope] = [self.atom_fractions[isotope][0],mass_frac]
		elif mode == 'mass':
			# sum the fractions, renormalize
			frac_total = 0.0
			for isotope in self.mass_fractions.keys():
				frac_total = frac_total + self.mass_fractions[isotope][1]
			for isotope in self.mass_fractions.keys():
				self.mass_fractions[isotope] = self.mass_fractions[isotope][1] / frac_total
			# calculate averge amu from mass fractions
			self.avg_amu = 0.0 
			for isotope in self.atom_fractions.keys():
				self.avg_amu = self.avg_amu + self.atom_fractions[isotope][1]/self.atom_fractions[isotope][0]
			self.avg_amu = 1.0 / self.avg_amu
			# calculate the atom factions
			for isotope in self.mass_fractions.keys():
				atom_frac = self.avg_amu * self.mass_fractions[isotope][1] / self.mass_fractions[isotope][0]
				self.mass_fractions[isotope] = [self.atom_fractions[isotope][0],mass_frac]
		else:
			print "uninitialized!  cannot finalize."
			return

		self.mode = 'finalized'

		_elements.append(self.name)



#
#  material class for a rod
#
class material:

	def __init__(self,name):
		if !isinstance(name,str):
			print "input is not a string.  rejected."
			return
		self.name 			= copy.deepcopy(name)
		self.n_isotopes		= 0
		self.density 		= 0.0
		self.isotopes 		= []
		self.atom_fractions	= []
		self.mass_fractions	= []

	def add_isotope_atom(self,name,frac):
		if !isinstance(name,str):
			print "first input is not a string.  rejected."
			return
		if !isinstance(name,float):
			print "second input is not a float.  rejected."
			return

	def add_isotope_mass(self,name,frac):
		if !isinstance(name,str):
			print "first input is not a string.  rejected."
			return
		if !isinstance(name,float):
			print "second input is not a float.  rejected."
			return

	def finalize_atom():
		if len(self.mass_fractions)>0:
			print "%d mass fractions overwritten to be consistent with the entered atom fractions."%len(self.mass_fractions)
		for:


	def finalize_mass():
		if len(self.atom_fractions)>0:
			print "%d mass fractions overwritten to be consistent with the entered atom fractions."%len(self.atom_fractions)


class rod:

	# global material dictionary
	_materials = {}

	def __init__(self,name):
		if !isinstance(name,str):
			print "input is not a string.  rejected."
			return
		self.name 				= copy.deepcopy(name)
		self.volume_fractions	= {}  # this dictionary must be material name keys with volume fraction values!
		self.average_density	= 0.0
		self.volume 			= 0.0
		self.isotope_list 		= {}

	def add_material(self,mat_in):
		# check if material object and a string
		if !isinstance(mat_in, material):
			print "second input is not a material object.  rejected."
			return

		# add it otherwise, copy to be sure that it isn't a reference
		print "adding material to class global dictionary"
		_materials[material.name]=copy.deepcopy(material)

	def add_frac(self,name,frac):
		# check if material object and a string
		if !isinstance(frac, float):
			print "second input is not a float.  rejected."
			return
		if !isinstance(name,str):
			print "first input is not a string.  rejected."
			return

		# otherwise add it to this rod's dictionary
		self.volume_fractions[name]=copy.deepcopy(frac)

	def calc_material_definition(self):


#
# init rod objects so we can add materials to it
#
rods=[]
rods.append(rod("STIP-VII Rod 1"))
rods.append(rod("STIP-VII Rod 2"))
rods.append(rod("STIP-VII Rod 3"))
rods.append(rod("STIP-VII Rod 4"))
rods.append(rod("STIP-VII Rod 5"))
rods.append(rod("STIP-VII Rod 6"))
rods.append(rod("STIP-VII Rod 7"))
rods.append(rod("STIP-VII Rod 8"))
rods.append(rod("STIP-VII Rod 9"))
rods.append(rod("STIP-VII Rod 10"))
rods.append(rod("STIP-VII Rod 11"))
rods.append(rod("STIP-VII Rod 12"))
rods.append(rod("STIP-VII Rod 13"))
rods.append(rod("STIP-VII Rod 14"))
rods.append(rod("STIP-VII Rod 15"))
rods.append(rod("STIP-VII Rod 16"))

#
#  materials
#
W
SS 316L
Ta
He
Zry-2
SIMP
T91
CLAM
Al
Al6061
Ti6Al4V
Ti3AlC2
Ti3SiC2
Ti6Al4V
Ti2AlC
Pb
Ta
9Cr-ODS
14Cr-ODS
Fe-Cr alloy
