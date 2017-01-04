#! /home/l_bergmann/anaconda/bin/python -W ignore
#  top level script for calculating the STIP-VI volume-averaged materials 
#  Ryan M. Bergmann, June 2016 
#  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

from MCNPtools import calculate_materials
import copy

calculate_materials.verbose=0

execfile("natural_abundances.py")
execfile("compounds.py")
execfile("material_collection.py")

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
 

for mat in calculate_materials.material._materials.keys():
	calculate_materials.material._materials[mat].print_material_card()

print "c |=========================================|"
print "c |                                         |" 
print "c |                                         |"  
print "c | VOLUME AVERAGED MATERIALS FOR STIP RODS |"
print "c |                                         |" 
print "c |                                         |" 
print "c |=========================================|"

r1=calculate_materials.mixture('STIP-VII Rod 1')
r1.add_material_vol('W',          46.83)
r1.add_material_vol('SS316',      15.36)
r1.add_material_vol('Ta',         15.36)
r1.add_material_vol('He',          7.10)
r1.add_material_vol('Zircaloy-II',15.36)
r1.finalize()
r1.print_material_card()


r2=calculate_materials.mixture('STIP-VII Rod 2')
r2.add_material_vol('SIMP',		7.61)
r2.add_material_vol('SS316',	19.29)
r2.add_material_vol('T91',   	15.75)
r2.add_material_vol('CLAM',  	44.94)
r2.add_material_vol('Al',    	5.76)
r2.add_material_vol('He',    	6.65)
r2.finalize()
r2.print_material_card()


r3=calculate_materials.mixture('STIP-VII Rod 3')
r3.add_material_vol('SIMP',		29.88)
r3.add_material_vol('CLAM',		29.88)
r3.add_material_vol('SS316',	12.78)
r3.add_material_vol('T91',		4.30)
r3.add_material_vol('He',		23.16)
r3.finalize()
r3.print_material_card()


r4=calculate_materials.mixture('STIP-VII Rod 4')
r4.add_material_vol('SIMP',		4.70)
r4.add_material_vol('Al6061',	18.81)
r4.add_material_vol('CLAM',		1.48)
r4.add_material_vol('SS316',	39.17)
r4.add_material_vol('T91',		1.27)
r4.add_material_vol('Ti6Al4V',	4.91)
r4.add_material_vol('Ti3AlC2',	1.69)
r4.add_material_vol('Ti3SiC2',	4.11)
r4.add_material_vol('Ti2AlC',	3.22)
r4.add_material_vol('W',		1.61)
r4.add_material_vol('He',		19.03)
r4.finalize()
r4.print_material_card()


r5=calculate_materials.mixture('STIP-VII Rod 5')
r5.add_material_vol('SIMP',		4.25)
r5.add_material_vol('Al6061',	21.42)
r5.add_material_vol('CLAM',		7.09)
r5.add_material_vol('SS316',	46.07)
r5.add_material_vol('T91',		1.43)
r5.add_material_vol('Ti6Al4V',	1.93)
r5.add_material_vol('Ti',		6.83)
r5.add_material_vol('He',		10.97)
r5.finalize()
r5.print_material_card()


r6=calculate_materials.mixture('STIP-VII Rod 6')
r6.add_material_vol('W',	99.57)
r6.add_material_vol('He',	 0.43)
r6.finalize()
r6.print_material_card()


r7=calculate_materials.mixture('STIP-VII Rod 7')
r7.add_material_vol('W',	92.58)
r7.add_material_vol('Pb',	 7.42)
r7.finalize()
r7.print_material_card()


r8=calculate_materials.mixture('STIP-VII Rod 8')
r8.add_material_vol('W',	71.55)
r8.add_material_vol('Ta',	23.34)
r8.add_material_vol('He',	 5.11)
r8.finalize()
r8.print_material_card()


r9=calculate_materials.mixture('STIP-VII Rod 9')
r9.add_material_vol('SIMP',		16.49)
r9.add_material_vol('SS316',	31.30)
r9.add_material_vol('Ti6Al4V',	12.68)
r9.add_material_vol('W',		19.02)
r9.add_material_vol('Al6061',	12.20)
r9.add_material_vol('He',		 8.31)
r9.finalize()
r9.print_material_card()


r10=calculate_materials.mixture('STIP-VII Rod 10')
r10.add_material_vol('CLAM',	59.76)
r10.add_material_vol('SS316',	12.78)
r10.add_material_vol('T91',		 4.30)
r10.add_material_vol('Al6061',	 4.52)
r10.add_material_vol('Ti',		 0.87)
r10.add_material_vol('He',		17.77)
r10.finalize()
r10.print_material_card()


r11=calculate_materials.mixture('STIP-VII Rod 11')
r11.add_material_vol('SIMP',	59.76)
r11.add_material_vol('T91',		 4.30)
r11.add_material_vol('W',		 1.01)
r11.add_material_vol('He',		34.93)
r11.finalize()
r11.print_material_card()


r12=calculate_materials.mixture('STIP-VII Rod 12')
r12.add_material_vol('SIMP',	12.68)
r12.add_material_vol('SS316',	33.77)
r12.add_material_vol('CLAM',	12.68)
r12.add_material_vol('Ti3AlC2',	 7.61)
r12.add_material_vol('Ti3SiC2',	 7.61)
r12.add_material_vol('Ti6Al4V',	 2.54)
r12.add_material_vol('Al6061',	 4.34)
r12.add_material_vol('He',		18.77)
r12.finalize()
r12.print_material_card()


r13=calculate_materials.mixture('STIP-VII Rod 13')
r13.add_material_vol('9Cr-ODS',		 4.11)
r13.add_material_vol('14Cr-ODS',	 5.06)
r13.add_material_vol('SS316',		32.85)
r13.add_material_vol('Ti3SiC2',		 5.43)
r13.add_material_vol('Ti2AlC',		 4.52)
r13.add_material_vol('Al6061',		 2.48)
r13.add_material_vol('He',			49.65)
r13.finalize()
r13.print_material_card()


r14=calculate_materials.mixture('STIP-VII Rod 14')
r14.add_material_vol('9Cr-ODS',	36.56)
r14.add_material_vol('T91',		36.56)
r14.add_material_vol('SiC',		 8.60)
r14.add_material_vol('He',		18.28)
r14.finalize()
r14.print_material_card()


r15=calculate_materials.mixture('STIP-VII Rod 15')
r15.add_material_vol('9Cr-ODS',	36.56)
r15.add_material_vol('T91',		36.56)
r15.add_material_vol('SiC',		 8.60)
r15.add_material_vol('He',		18.28)
r15.finalize()
r15.print_material_card()


r16=calculate_materials.mixture('STIP-VII Rod 16')
r16.add_material_vol('T91',		 8.14)
r16.add_material_vol('FeCr',	21.70)
r16.add_material_vol('SS316',	22.79)
r16.add_material_vol('Al6061',	10.49)
r16.add_material_vol('He  ',		45.02)
r16.finalize()
r16.print_material_card()


borated_water=calculate_materials.mixture('borated_water')
borated_water.add_material_vol('light_water', 3000.00)
borated_water.add_material_vol('borax',        173.41)
borated_water.add_material_vol('boric_acid',   139.38)
borated_water.finalize()
borated_water.print_material_card()

borated_concrete_SIEMENS=calculate_materials.mixture('borated concrete, SIEMENS, 1wt% B4C')
borated_concrete_SIEMENS.add_material_vol('concrete, SIEMENS', 100.0)
borated_concrete_SIEMENS.add_material_vol('B4C',                1.0)
borated_concrete_SIEMENS.finalize()
borated_concrete_SIEMENS.print_material_card()

#rt=calculate_materials.mixture('Test Rod 1')
#rt.add_material_vol('SS316',      1.0)
#rt.finalize()
#rt.print_material_card()
#
#
#
#b4c=calculate_materials.mixture('B4C rod')
#b4c.add_material_vol('B4C',		 1.0)
#b4c.finalize()
#b4c.print_material_card()