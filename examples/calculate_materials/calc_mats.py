#! /home/l_bergmann/anaconda/bin/python -W ignore
#  top level script for calculating the STIP-VI volume-averaged materials
#  Ryan M. Bergmann, June 2016
#  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

# import the main module
from MCNPtools import calculate_materials

# import some materials libraries, makes them present in the global material dictionary, NOT directly in this namespace
# this is done so things like SS316 already exist
from MCNPtools import material_collection

# more imports
import copy

# set the verbose flag so that all the details of mixing aren't printed
calculate_materials.verbose=0

# set the card printing flag
calculate_materials.print_type='atom'

total_width = len('                                         ')
name = 'Ryan M. Bergmann'

print "c |=========================================|"
print "c |                                         |"
print "c |    Calculated by ryan.bergmann@psi.ch   |"
print "c |              June 10, 2016              |"
print "c |                                         |"
print "c |                                         |"
print "c |=========================================|"
print "c "
print "c |=========================================|"
print "c |                                         |"
print "c |                                         |"
print "c |          INDIVIDUAL MATERIALS           |"
print "c |                                         |"
print "c |                                         |"
print "c |=========================================|"

# acessing the class global dictionary
for mix in calculate_materials.mixture._mixtures.keys():
	calculate_materials.mixture._mixtures[mix].print_material_card()

print "c |=========================================|"
print "c |                                         |"
print "c |                                         |"
print "c | VOLUME AVERAGED MATERIALS FOR STIP RODS |"
print "c |                                         |"
print "c |                                         |"
print "c |=========================================|"

r1=calculate_materials.mixture('STIP-VII Rod 1')
r1.add_mixture('W',          46.83, mode='volume')
r1.add_mixture('SS316',      15.36, mode='volume')
r1.add_mixture('Ta',         15.36, mode='volume')
r1.add_mixture('He',          7.10, mode='volume')
r1.add_mixture('Zircaloy-II',15.36, mode='volume')
r1.finalize()
r1.print_material_card()

#
#
#

print "c |=========================================|"
print "c |                                         |"
print "c |                                         |"
print "c |        SOME ADDITIONAL MATERIALS        |"
print "c |                                         |"
print "c |                                         |"
print "c |=========================================|"

hydrogen_peroxide = calculate_materials.mixture('H2O2')
hydrogen_peroxide.add_mixture('H' ,  2., mode='atom')
hydrogen_peroxide.add_mixture('O' ,  2., mode='atom')
hydrogen_peroxide.mass_density=1.45
hydrogen_peroxide.finalize()

peroxide_solution=calculate_materials.mixture('peroxide solution 6wt%')
peroxide_solution.add_mixture('light water', 94.0, mode='mass')
peroxide_solution.add_mixture('H2O2',         6.0, mode='mass')
peroxide_solution.mass_density=1.01
peroxide_solution.finalize()
peroxide_solution.print_material_card()

borated_water=calculate_materials.mixture('borated water')
borated_water.add_mixture('light water', 3000.00, mode='mass')
borated_water.add_mixture('borax',        173.41, mode='mass')
borated_water.add_mixture('boric_acid',   139.38, mode='mass')
borated_water.mass_density=1.05
borated_water.finalize()
borated_water.print_material_card()

borated_concrete_SIEMENS=calculate_materials.mixture('borated concrete, SIEMENS, 1wt% B4C')
borated_concrete_SIEMENS.add_mixture('concrete, SIEMENS', 100.0, mode='volume')
borated_concrete_SIEMENS.add_mixture('B4C',                 1.0, mode='volume')
borated_concrete_SIEMENS.finalize()
borated_concrete_SIEMENS.print_material_card()
