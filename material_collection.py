# Stainless Steel 316
ss316=calculate_materials.material('SS316',7.85)
ss316.add_element_atom( 'P'  ,    210.00)
ss316.add_element_atom( 'Mo' ,   1990.00)
ss316.add_element_atom( 'Zn' ,     12.00)
ss316.add_element_atom( 'Pb' ,     40.00)
ss316.add_element_atom( 'Co' ,   1330.00)
ss316.add_element_atom( 'Ni' ,  87600.00)
ss316.add_element_atom( 'Si' ,   4010.00)
ss316.add_element_atom( 'Mn' ,  13600.00)
ss316.add_element_atom( 'Fe' , 715109.00)
ss316.add_element_atom( 'Cr' , 172000.00)
ss316.add_element_atom( 'Mg' ,      3.10)
ss316.add_element_atom( 'V'  ,    800.00)
ss316.add_element_atom( 'Cu' ,   1240.00)
ss316.add_element_atom( 'Ag' ,      6.00)
ss316.add_element_atom( 'Ti' ,    128.00)
ss316.add_element_atom( 'Ca' ,      4.40)
ss316.add_element_atom( 'Al' ,     35.00)
ss316.add_element_atom( 'Sr' ,      0.30)
ss316.add_element_atom( 'K'  ,      2.10)
ss316.add_element_atom( 'Cs' ,     13.00)
ss316.add_element_atom( 'Rb' ,      5.00)
ss316.add_element_atom( 'W'  ,   1350.00)
ss316.add_element_atom( 'Ga' ,    123.00)
ss316.add_element_atom( 'C'  ,    390.00)
ss316.finalize()

# pure aluminum
al_pure=calculate_materials.material('Al',2.70)
al_pure.add_element_atom( 'Al'  , 1000000.00)
al_pure.finalize()

#
#  pure tungsten
#
tungsten = calculate_materials.material('W',19.25)
tungsten.add_element_atom( 'W'  , 1000000.00)
tungsten.finalize()

#
#  pure tantalum
#
tantalum = calculate_materials.material('Ta',16.4)
tantalum.add_element_atom( 'Ta'  , 1000000.00)
tantalum.finalize()

#
#  pure titanium
#
titanium = calculate_materials.material('Ti',4.43)
titanium.add_element_atom( 'Ti'  , 1000000.00)
titanium.finalize()

#
#  pure helium
#
helium = calculate_materials.material('He',0.164)
helium.add_element_atom( 'He'  , 1000000.00)
helium.finalize()

#
#  pure lead
#
lead = calculate_materials.material('Pb',11.32)
lead.add_element_atom( 'Pb'  , 1000000.00)
lead.finalize()

#
#  zircaloy-2
#
lead = calculate_materials.material('Zircaloy-II',11.32)
lead.add_element_atom( 'Zr',980700.0)
lead.add_element_atom( 'Sn', 14600.0)
lead.add_element_atom( 'Fe',  1500.0)
lead.add_element_atom( 'Cr',  2500.0)
lead.add_element_atom( 'Ni',   500.0)
lead.add_element_atom( 'Hf',   200.0)
lead.finalize()

#
# T91 steel
# wt%, from http://pure.qub.ac.uk/portal/files/17599818/341_manuscript.pdf  
t91 = calculate_materials.material('T91',7.76)
t91.add_element_mass( 'Fe',  89.4)
t91.add_element_mass( 'C' ,  0.10)    
t91.add_element_mass( 'Si',  0.26)    
t91.add_element_mass( 'V' ,  0.2 )     
t91.add_element_mass( 'Cr',  8.45)   
t91.add_element_mass( 'Mn',  0.46)    
t91.add_element_mass( 'Ni',  0.17)    
t91.add_element_mass( 'Mo',  0.92)    
t91.add_element_mass( 'Nb',  0.04)    
t91.finalize()

#
# SIMP steel
# wt%, from http://pure.qub.ac.uk/portal/files/17599818/341_manuscript.pdf   
simp = calculate_materials.material('SIMP',7.8) # couldn't find reference for density...
simp.add_element_mass( 'Fe',   84.53)
simp.add_element_mass( 'C' ,   0.25)    
simp.add_element_mass( 'Si',   1.5 )    
simp.add_element_mass( 'V',    0.2 )    
simp.add_element_mass( 'Cr',   10.8)    
simp.add_element_mass( 'Mn',   0.5 )    
simp.add_element_mass( 'W',    1.2 )    
simp.add_element_mass( 'Mo',   0.9 )    
simp.add_element_mass( 'Nb',   0.01)    
simp.add_element_mass( 'Ta',   0.11) 
simp.finalize()

#
# CLAM steel
# http://www.sciencedirect.com/science/article/pii/S0261306914004774
clam = calculate_materials.material('CLAM',7.8) # couldn't find reference for density...
clam.add_element_mass( 'Fe', 88.709 )
clam.add_element_mass( 'C',  0.091)
clam.add_element_mass( 'Cr',  8.93 )
clam.add_element_mass( 'Mn',  0.49 )
clam.add_element_mass( 'W',  1.51)
clam.add_element_mass( 'V',  0.15 )
clam.add_element_mass( 'Ta', 0.15 )
clam.finalize()

#
# Al6061
# http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA6061t6
al_6061 = calculate_materials.material('Al6061',2.7)
al_6061.add_element_mass( 'Al',  97.2 )
al_6061.add_element_mass( 'Cr',  0.195)
al_6061.add_element_mass( 'Cu',  0.275)
al_6061.add_element_mass( 'Fe',  0.35 ) 
al_6061.add_element_mass( 'Mg',  1.0  )
al_6061.add_element_mass( 'Mn',  0.075)	 	 
al_6061.add_element_mass( 'Si',  0.6  )
al_6061.add_element_mass( 'Ti',  0.075)	 
al_6061.add_element_mass( 'Zn',  0.125)
al_6061.finalize()


#
# Ti6Al4V
#
ti6al4v = calculate_materials.material('Ti6Al4V',4.43)
ti6al4v.add_element_atom( 'Ti', 6.0 )
ti6al4v.add_element_atom( 'Al', 4.0 )
ti6al4v.add_element_atom( 'V' , 1.0 )
ti6al4v.finalize()

#
# Ti3AlC2
#
ti3alc2 = calculate_materials.material('Ti3AlC2',4.24)
ti3alc2.add_element_atom( 'Ti', 3.0 )
ti3alc2.add_element_atom( 'Al', 1.0 )
ti3alc2.add_element_atom( 'C' , 2.0 )
ti3alc2.finalize()

#
#Ti3SiC2
#
ti3sic2 = calculate_materials.material('Ti3SiC2',4.53)
ti3sic2.add_element_atom( 'Ti', 3.0 )
ti3sic2.add_element_atom( 'Si', 1.0 )
ti3sic2.add_element_atom( 'C' , 2.0 )
ti3sic2.finalize()

#
#Ti2AlC
#
ti3alc = calculate_materials.material('Ti2AlC',4.25)
ti3alc.add_element_atom( 'Ti', 3.0 )
ti3alc.add_element_atom( 'Al', 1.0 )
ti3alc.add_element_atom( 'C' , 1.0 )
ti3alc.finalize()


#
# 9Cr-ODS
#
cr9_ods = calculate_materials.material('9Cr-ODS',7.8)
cr9_ods.add_element_mass( 'Fe', 87.85   )
cr9_ods.add_element_mass( 'Cr',  9.0    )
cr9_ods.add_element_mass( 'W'    , 2.5  )
cr9_ods.add_element_mass( 'Ti'   , 0.4  ) 
cr9_ods.add_element_mass( 'Y2O3' , 0.25 )   
cr9_ods.finalize()

#
# 14Cr-ODS
#
cr14_ods = calculate_materials.material('14Cr-ODS',7.8)
cr14_ods.add_element_mass( 'Fe', 82.85   )
cr14_ods.add_element_mass( 'Cr', 14.0    )
cr14_ods.add_element_mass( 'W'    , 2.5  )
cr14_ods.add_element_mass( 'Ti'   , 0.4  ) 
cr14_ods.add_element_mass( 'Y2O3' , 0.25 )   
cr14_ods.finalize()

#
# Fe-Cr alloy
#
fecr = calculate_materials.material('FeCr',7.8)
fecr.add_element_mass( 'Fe', 88.0   )
fecr.add_element_mass( 'Cr', 12.0    )
fecr.finalize()

#
# SiC
#
sic = calculate_materials.material('SiC',3.21)
sic.add_element_atom( 'Si', 1.0   )
sic.add_element_atom( 'C',  1.0    )
sic.finalize()