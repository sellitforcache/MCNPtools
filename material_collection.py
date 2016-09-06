# Stainless Steel 316
ss316=calculate_materials.material('SS316',7.95)
#ss316.add_element_mass( 'P'  ,    210.00)
ss316.add_element_mass( 'Mo' ,   1990.00)
#ss316.add_element_mass( 'Zn' ,     12.00)
#ss316.add_element_mass( 'Pb' ,     40.00)
ss316.add_element_mass( 'Co' ,   1330.00)
ss316.add_element_mass( 'Ni' ,  87600.00)
ss316.add_element_mass( 'Si' ,   4010.00)
ss316.add_element_mass( 'Mn' ,  13600.00)
ss316.add_element_mass( 'Fe' , 715109.00)
ss316.add_element_mass( 'Cr' , 172000.00)
#ss316.add_element_mass( 'Mg' ,      3.10)
ss316.add_element_mass( 'V'  ,    800.00)
ss316.add_element_mass( 'Cu' ,   1240.00)
#ss316.add_element_mass( 'Ag' ,      6.00)
#ss316.add_element_mass( 'Ti' ,    128.00)
#ss316.add_element_mass( 'Ca' ,      4.40)
#ss316.add_element_mass( 'Al' ,     35.00)
#ss316.add_element_mass( 'Sr' ,      0.30)
#ss316.add_element_mass( 'K'  ,      2.10)
#ss316.add_element_mass( 'Cs' ,     13.00)
#ss316.add_element_mass( 'Rb' ,      5.00)
ss316.add_element_mass( 'W'  ,   1350.00)
#ss316.add_element_mass( 'Ga' ,    123.00)
#ss316.add_element_mass( 'C'  ,    390.00)
ss316.finalize()

# pure aluminum
al_pure=calculate_materials.material('Al',2.70)
al_pure.add_element_atom( 'Al'  , 1.00)
al_pure.finalize()

#
#  pure tungsten
#
tungsten = calculate_materials.material('W',19.25)
tungsten.add_element_atom( 'W'  , 1.00)
tungsten.finalize()

#
#  pure tantalum
#
tantalum = calculate_materials.material('Ta',16.4)
tantalum.add_element_atom( 'Ta'  , 1.00)
tantalum.finalize()

#
#  pure titanium
#
titanium = calculate_materials.material('Ti',4.43)
titanium.add_element_atom( 'Ti'  , 1.00)
titanium.finalize()

#
#  pure helium
#
helium = calculate_materials.material('He',0.164)
helium.add_element_atom( 'He'  , 1.00)
helium.finalize()

#
#  pure lead
#
lead = calculate_materials.material('Pb',11.32)
lead.add_element_atom( 'Pb'  , 1.00)
lead.finalize()

#
#  pure copper
#
lead = calculate_materials.material('Cu',8.96)
lead.add_element_atom( 'Cu'  , 1.00)
lead.finalize()

#
#  pure iron
#
lead = calculate_materials.material('Fe', 7.874)
lead.add_element_atom( 'Fe'  , 1.00)
lead.finalize()

#
#  Neodymium permanent magnets
#
lead = calculate_materials.material('NeoMag', 7.4)
lead.add_element_atom( 'Nd'  ,  2.00)
lead.add_element_atom( 'Fe'  , 14.00)
lead.add_element_atom( 'B'   ,  1.00)
lead.finalize()

#
#  zircaloy-2
#
lead = calculate_materials.material('Zircaloy-II',11.32)
lead.add_element_mass( 'Zr',980700.0)
lead.add_element_mass( 'Sn', 14600.0)
lead.add_element_mass( 'Fe',  1500.0)
lead.add_element_mass( 'Cr',  2500.0)
lead.add_element_mass( 'Ni',   500.0)
lead.add_element_mass( 'Hf',   200.0)
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

#
# B4C
#
b4c = calculate_materials.material('B4C',2.52)
b4c.add_element_atom( 'B',  4.0   )
b4c.add_element_atom( 'C',  1.0    )
b4c.finalize()

#
# high density polyethylene
#
hdpe = calculate_materials.material('HDPE',0.95)
hdpe.add_element_atom( 'H',  4.0   )
hdpe.add_element_atom( 'C',  2.0    )
hdpe.finalize()

#
# Borated concrete
#
concrete_borated = calculate_materials.material('Borated Concrete',3.10)
concrete_borated.add_element_mass( 'H ', 0.005600)
concrete_borated.add_element_mass( 'B ', 0.010400)
concrete_borated.add_element_mass( 'O ', 0.338000)
concrete_borated.add_element_mass( 'F ', 0.002300)
concrete_borated.add_element_mass( 'Na', 0.012100)
concrete_borated.add_element_mass( 'Mg', 0.002300)
concrete_borated.add_element_mass( 'Al', 0.006400)
concrete_borated.add_element_mass( 'Si', 0.033100)
concrete_borated.add_element_mass( 'S ', 0.091500)
concrete_borated.add_element_mass( 'K ', 0.001000)
concrete_borated.add_element_mass( 'Ca', 0.062600)
concrete_borated.add_element_mass( 'Mn', 0.000200)
concrete_borated.add_element_mass( 'Fe', 0.021900)
concrete_borated.add_element_mass( 'Zn', 0.006600)
concrete_borated.add_element_mass( 'Ba', 0.401300)
concrete_borated.finalize()

#
# borosilicate glass
#
glass_borosilicate = calculate_materials.material('Borosilicate Glass',2.23)
glass_borosilicate.add_element_mass( 'B ', 0.040066)
glass_borosilicate.add_element_mass( 'O ', 0.539559)
glass_borosilicate.add_element_mass( 'Na', 0.028191)
glass_borosilicate.add_element_mass( 'Al', 0.011644)
glass_borosilicate.add_element_mass( 'Si', 0.377220)
glass_borosilicate.add_element_mass( 'K ', 0.003321)
glass_borosilicate.finalize()

#
# plate glass
#
glass_plate = calculate_materials.material('Plate Glass',2.40)
glass_plate.add_element_mass(  'O ', 0.459800) 
glass_plate.add_element_mass(  'Na', 0.096441) 
glass_plate.add_element_mass(  'Si', 0.336553) 
glass_plate.add_element_mass(  'Ca', 0.107205)
glass_plate.finalize()


#
# Schrottbeton/heavy concrete/heavy mortar
# Assay number   10 : Representative Schrottbeton
#
schrottbeton = calculate_materials.material('Schrottbeton',5.7)
schrottbeton.add_element_mass( 'H ',   3000.00 )
#schrottbeton.add_element_mass( 'Li',      0.10 )
#schrottbeton.add_element_mass( 'Be',      0.09 )
#schrottbeton.add_element_mass( 'B ',     63.0  )
schrottbeton.add_element_mass( 'C ',   3000.00 )
#schrottbeton.add_element_mass( 'N ',     70.00 )
schrottbeton.add_element_mass( 'O ',  80000.00 )
#schrottbeton.add_element_mass( 'Na',     87.00 )
schrottbeton.add_element_mass( 'Mg',    837.00 )
schrottbeton.add_element_mass( 'Al',   3270.00 )
schrottbeton.add_element_mass( 'Si',  17600.00 )
schrottbeton.add_element_mass( 'P ',   5770.00 )
schrottbeton.add_element_mass( 'S ',   2560.00 )
#schrottbeton.add_element_mass( 'Cl',     30.00 )
schrottbeton.add_element_mass( 'K ',    260.00 )
schrottbeton.add_element_mass( 'Ca',    280.00 )
schrottbeton.add_element_mass( 'Ti',    555.00 )
schrottbeton.add_element_mass( 'V ',    510.00 )
schrottbeton.add_element_mass( 'Cr',    710.00 )
schrottbeton.add_element_mass( 'Mn',   4300.00 )
schrottbeton.add_element_mass( 'Fe', 861000.00 )
schrottbeton.add_element_mass( 'Co',    120.00 )
schrottbeton.add_element_mass( 'Ni',    615.00 )
schrottbeton.add_element_mass( 'Cu',   1700.00 )
#schrottbeton.add_element_mass( 'Zn',     77.00 )
#schrottbeton.add_element_mass( 'Ga',     10.00 )
schrottbeton.add_element_mass( 'As',    238.00 )
#schrottbeton.add_element_mass( 'Rb',      3.00 )
schrottbeton.add_element_mass( 'Sr',    140.00 )
#schrottbeton.add_element_mass( 'Y ',      1.00 )
#schrottbeton.add_element_mass( 'Zr',     10.00 )
#schrottbeton.add_element_mass( 'Nb',      1.00 )
#schrottbeton.add_element_mass( 'Mo',     50.00 )
#schrottbeton.add_element_mass( 'Ag',      0.70 )
#schrottbeton.add_element_mass( 'Sn',      5.00 )
#schrottbeton.add_element_mass( 'Sb',     70.00 )
schrottbeton.add_element_mass( 'Te',    100.00 )
#schrottbeton.add_element_mass( 'Cs',      6.00 )
#schrottbeton.add_element_mass( 'Ba',     55.00 )
#schrottbeton.add_element_mass( 'La',      5.00 )
#schrottbeton.add_element_mass( 'Ce',      1.00 )
#schrottbeton.add_element_mass( 'Sm',      1.00 )
#schrottbeton.add_element_mass( 'Eu',      0.10 )
#schrottbeton.add_element_mass( 'Gd',      0.50 )
#schrottbeton.add_element_mass( 'Dy',      0.30 )
#schrottbeton.add_element_mass( 'Ho',      0.50 )
#schrottbeton.add_element_mass( 'Yb',      0.10 )
#schrottbeton.add_element_mass( 'Lu',     20.00 )
schrottbeton.add_element_mass( 'W ',    380.00 )
#schrottbeton.add_element_mass( 'Tl',      2.00 ) 
#schrottbeton.add_element_mass( 'Pb',      6.00 )
#schrottbeton.add_element_mass( 'Bi',      1.00 )
#schrottbeton.add_element_mass( 'Th',      0.50 )
#schrottbeton.add_element_mass( 'U ',      1.00 )
schrottbeton.finalize()

#
#  
# schrottbeton from some old mcnp definition
#
schrottbeton2 = calculate_materials.material('Schrottbeton-PSI',4.783)
schrottbeton2.add_element_mass( 'H ',   0.004395  )
schrottbeton2.add_element_mass( 'O ',   0.184241  ) 
schrottbeton2.add_element_mass( 'Fe',   0.765413  )
schrottbeton2.add_element_mass( 'Ca',   0.002704  )
schrottbeton2.add_element_mass( 'Si',   0.020705  )
schrottbeton2.add_element_mass( 'Al',   0.002077  )
schrottbeton2.finalize()



#
# Bundeseisen
#
bundeseisen = calculate_materials.material('Bundeseisen',7.80488)  # calculated from drawing 0-10009.22.026
bundeseisen.add_element_mass( 'C' 	,	2689.	)
#bundeseisen.add_element_mass( 'Na' 	,	2.		)
#bundeseisen.add_element_mass( 'Mg' 	,	5.		)
bundeseisen.add_element_mass( 'Al' 	,	100.	)
bundeseisen.add_element_mass( 'Si' 	,	7451.	)
bundeseisen.add_element_mass( 'P' 	,	344.	)
bundeseisen.add_element_mass( 'S' 	,	303.	)
#bundeseisen.add_element_mass( 'K' 	,	17.		)
#bundeseisen.add_element_mass( 'Ca' 	,	13.		)
#bundeseisen.add_element_mass( 'Ti' 	,	12.		)
bundeseisen.add_element_mass( 'V' 	,	310.	)
bundeseisen.add_element_mass( 'Cr' 	,	728.	)
bundeseisen.add_element_mass( 'Mn' 	,	9699.	)
bundeseisen.add_element_mass( 'Fe' 	,	971278.	)
bundeseisen.add_element_mass( 'Co' 	,	153.	)
bundeseisen.add_element_mass( 'Ni' 	,	1796.	)
bundeseisen.add_element_mass( 'Cu' 	,	3701.	)
#bundeseisen.add_element_mass( 'Zn' 	,	70.		)
bundeseisen.add_element_mass( 'As' 	,	245.	)
#bundeseisen.add_element_mass( 'Rb' 	,	19.		)
bundeseisen.add_element_mass( 'Mo' 	,	95.		)
bundeseisen.add_element_mass( 'Sn' 	,	769.	)
bundeseisen.add_element_mass( 'Cs' 	,	93.		)
#bundeseisen.add_element_mass( 'Yb' 	,	1.		)
#bundeseisen.add_element_mass( 'W' 	,	3.		)
#bundeseisen.add_element_mass( 'Pb' 	,	84.		)
bundeseisen.finalize()

#
#  Granatsand, Australien
#  4.1 g/cc solid, 2.4 bulk, from http://www.abritec.ch/index.php?nav=5,32
granatsand1 = calculate_materials.material('Granatsand 1',2.40)
granatsand1.add_element_mass( 'P' 	,240.	)
granatsand1.add_element_mass( 'S' 	,270.	)
#granatsand1.add_element_mass( 'As' 	,20.	)
#granatsand1.add_element_mass( 'Sn' 	,20.	)
#granatsand1.add_element_mass( 'Hg' 	,5.		)
#granatsand1.add_element_mass( 'Mo' 	,3.		)
granatsand1.add_element_mass( 'Cr' 	,142.	)
#granatsand1.add_element_mass( 'Zn' 	,43.4	)
#granatsand1.add_element_mass( 'Pb' 	,46.	)
#granatsand1.add_element_mass( 'Co' 	,34.	)
#granatsand1.add_element_mass( 'Cd' 	,1.0	)
#granatsand1.add_element_mass( 'Ni' 	,20.	)
#granatsand1.add_element_mass( 'B' 	,7.		)
granatsand1.add_element_mass( 'Si' 	,17.6e4	)
granatsand1.add_element_mass( 'Mn' 	,0.72e4	)
granatsand1.add_element_mass( 'Fe' 	,22.9e4	)
granatsand1.add_element_mass( 'Mg' 	,3.57e4	)
granatsand1.add_element_mass( 'V' 	,140.	)
#granatsand1.add_element_mass( 'Be' 	,0.5	)
#granatsand1.add_element_mass( 'Cu' 	,2.		)
#granatsand1.add_element_mass( 'Ag' 	,2.		)
#granatsand1.add_element_mass( 'Ti' 	,89.5	)
#granatsand1.add_element_mass( 'Zr' 	,33.	)
granatsand1.add_element_mass( 'Ca' 	,1.03e4	)
granatsand1.add_element_mass( 'Al' 	,10.6e4	)
#granatsand1.add_element_mass( 'Sr' 	,11.8	)
#granatsand1.add_element_mass( 'Ba' 	,64.4	)
#granatsand1.add_element_mass( 'Na' 	,72.	)
#granatsand1.add_element_mass( 'Li' 	,8.		)
#granatsand1.add_element_mass( 'K' 	,85.	)
#granatsand1.add_element_mass( 'Rb' 	,1.		)
#granatsand1.add_element_mass( 'Cs' 	,10.	)
#granatsand1.add_element_mass( 'Se' 	,20.	)
#granatsand1.add_element_mass( 'W' 	,10.	)
granatsand1.add_element_mass( 'Te' 	,108.	)
#granatsand1.add_element_mass( 'Sb' 	,10.	)
#granatsand1.add_element_mass( 'Re' 	,5.		)
#granatsand1.add_element_mass( 'Bi' 	,15.	)
#granatsand1.add_element_mass( 'Ir' 	,10.	)
#granatsand1.add_element_mass( 'Os' 	,20.	)
#granatsand1.add_element_mass( 'In' 	,20.	)
#granatsand1.add_element_mass( 'Ru' 	,10.	)
#granatsand1.add_element_mass( 'Au' 	,5.		)
#granatsand1.add_element_mass( 'Ge' 	,10.	)
#granatsand1.add_element_mass( 'Ta' 	,10.	)
#granatsand1.add_element_mass( 'Ga' 	,23.	)
#granatsand1.add_element_mass( 'Pr' 	,50.	)
#granatsand1.add_element_mass( 'Nb' 	,2.		)
#granatsand1.add_element_mass( 'Hf' 	,10.	)
#granatsand1.add_element_mass( 'Pd' 	,10.	)
#granatsand1.add_element_mass( 'Rh' 	,5.		)
#granatsand1.add_element_mass( 'Tl' 	,26.	)
#granatsand1.add_element_mass( 'U' 	,10.	)
#granatsand1.add_element_mass( 'Th' 	,5.		)
#granatsand1.add_element_mass( 'Lu' 	,17.2	)
#granatsand1.add_element_mass( 'Yb' 	,46.9	)
granatsand1.add_element_mass( 'Gd' 	,98.	)
#granatsand1.add_element_mass( 'Ho' 	,8.		)
#granatsand1.add_element_mass( 'Tm' 	,5.		)
#granatsand1.add_element_mass( 'Dy' 	,30.	)
#granatsand1.add_element_mass( 'Sm' 	,10.	)
granatsand1.add_element_mass( 'Sc' 	,1333.	)
#granatsand1.add_element_mass( 'Tb' 	,5.		)
granatsand1.add_element_mass( 'Y' 	,322.	)
#granatsand1.add_element_mass( 'La' 	,15.	)
#granatsand1.add_element_mass( 'Eu' 	,0.5	)
#ranatsand1.add_element_mass( 'Er' 	,35.	)
#ranatsand1.add_element_mass( 'Pr' 	,3.		)
#granatsand1.add_element_mass( 'Ce' 	,25.	)
#granatsand1.add_element_mass( 'Nd' 	,11. 	)
granatsand1.add_element_mass( 'O' 	,432070.8)  # balance
granatsand1.finalize()


#
#  Granatsand, "Neuer Abschirmsand"
#  4.1 g/cc solid, 2.4 bulk, from http://www.abritec.ch/index.php?nav=5,32
granatsand2 = calculate_materials.material('Granatsand 2',2.40)
#granatsand2.add_element_mass(  'Lu'	,	15.3		)
#granatsand2.add_element_mass(  'Yb'	,	18.4		)
granatsand2.add_element_mass(  'Gd'	,	103.		)
#granatsand2.add_element_mass(  'Ho'	,	1.			)
#granatsand2.add_element_mass(  'Tm'	,	2.			)
#granatsand2.add_element_mass(  'Dy'	,	1.			)
#granatsand2.add_element_mass(  'Sm'	,	5.			)
granatsand2.add_element_mass(  'Sc'	,	119.		)
#granatsand2.add_element_mass(  'Tb'	,	10.			)
granatsand2.add_element_mass(  'Y'	,	133.		)
#granatsand2.add_element_mass(  'La'	,	12.			)
#granatsand2.add_element_mass(  'Eu'	,	1.			)
#granatsand2.add_element_mass(  'Er'	,	13.			)
#granatsand2.add_element_mass(  'Pr'	,	10.			)
#granatsand2.add_element_mass(  'Ce'	,	10.			)
#granatsand2.add_element_mass(  'Nd'	,	10.			)
granatsand2.add_element_mass(  'P'	,	450.		)
granatsand2.add_element_mass(  'S'	,	370.		)
#granatsand2.add_element_mass(  'As'	,	20.			)
#granatsand2.add_element_mass(  'Sn'	,	20.			)
#granatsand2.add_element_mass(  'Hg'	,	20.			)
#granatsand2.add_element_mass(  'Mo'	,	5.			)
#granatsand2.add_element_mass(  'Zn'	,	79.			)
#granatsand2.add_element_mass(  'Pb'	,	20.			)
#granatsand2.add_element_mass(  'Co'	,	30.			)
#granatsand2.add_element_mass(  'Cd'	,	1.			)
#granatsand2.add_element_mass(  'Ni'	,	3.			)
#granatsand2.add_element_mass(  'B'	,	10.			)
granatsand2.add_element_mass(  'Si'	,	206000.		)
granatsand2.add_element_mass(  'Mn'	,	5550.		)
granatsand2.add_element_mass(  'Fe'	,	301000.		)
#granatsand2.add_element_mass(  'Cr'	,	49.			)
granatsand2.add_element_mass(  'Mg'	,	28100.		)
#granatsand2.add_element_mass(  'V'	,	74.			)
#granatsand2.add_element_mass(  'Be'	,	0.5			)
#granatsand2.add_element_mass(  'Cu'	,	26.			)
#granatsand2.add_element_mass(  'Ag'	,	9.			)
granatsand2.add_element_mass(  'Ti'	,	1790.		)
#granatsand2.add_element_mass(  'Zr'	,	84.			)
granatsand2.add_element_mass(  'Ca'	,	14900.		)
granatsand2.add_element_mass(  'Al'	,	127000.		)
#granatsand2.add_element_mass(  'Sr'	,	9.86		)
granatsand2.add_element_mass(  'Ba'	,	225.		)
granatsand2.add_element_mass(  'Na'	,	837.		)
#granatsand2.add_element_mass(  'Li'	,	5.			)
granatsand2.add_element_mass(  'K'	,	1050.		)
#granatsand2.add_element_mass(  'Cs'	,	3.			)
#granatsand2.add_element_mass(  'Rb'	,	18.			)
#granatsand2.add_element_mass(  'Se'	,	20.			)
#granatsand2.add_element_mass(  'W'	,	10.			)
#granatsand2.add_element_mass(  'Te'	,	50.			)
#granatsand2.add_element_mass(  'Sb'	,	20.			)
#granatsand2.add_element_mass(  'Re'	,	5.			)
#granatsand2.add_element_mass(  'Bi'	,	10.			)
#granatsand2.add_element_mass(  'Ir'	,	10.			)
#granatsand2.add_element_mass(  'Os'	,	20.			)
#granatsand2.add_element_mass(  'In'	,	50.			)
#granatsand2.add_element_mass(  'Ru'	,	10.			)
#ranatsand2.add_element_mass(  'Au'	,	10.			)
#granatsand2.add_element_mass(  'Ge'	,	10.			)
#granatsand2.add_element_mass(  'Ta'	,	10.			)
#granatsand2.add_element_mass(  'Ga'	,	28.			)
#granatsand2.add_element_mass(  'Pt'	,	50.			)
#granatsand2.add_element_mass(  'Nb'	,	5.			)
#granatsand2.add_element_mass(  'Hf'	,	10.			)
#granatsand2.add_element_mass(  'Pd'	,	10.			)
#granatsand2.add_element_mass(  'Rh'	,	10.			)
#granatsand2.add_element_mass(  'Tl'	,	50.			)
#granatsand2.add_element_mass(  'U'	,	10.			)
#granatsand2.add_element_mass(  'Th'	,	5.			)
granatsand2.add_element_mass(  'O'	,	311364.94  	) # balance
granatsand2.finalize()





#
# soil, from PNNL-15870 Rev. 1
#
soil = calculate_materials.material('soil',1.52)
soil.add_element_atom(  'H ', 0.316855) 
soil.add_element_atom(  'O ', 0.501581) 
soil.add_element_atom(  'Al', 0.039951) 
soil.add_element_atom(  'Si', 0.141613)
soil.finalize()

#
# asphalt/bitumen full density from PNNL-15870 Rev. 1
#
asphalt = calculate_materials.material('asphalt',1.3)
asphalt.add_element_atom(  'H ', 0.586755) 
asphalt.add_element_atom(  'C ', 0.402588) 
asphalt.add_element_atom(  'N ', 0.002463) 
asphalt.add_element_atom(  'O ', 0.001443)
asphalt.add_element_atom(  'S ', 0.006704) 
asphalt.add_element_atom(  'V ', 0.000044) 
asphalt.add_element_atom(  'Ni', 0.000003)
asphalt.finalize()

#
# polyurethane foam insulation, from PNNL-15870 Rev. 1, swisspor PUR premium
#
pur = calculate_materials.material('pur',0.03)
pur.add_element_atom(  'H ', 0.360023) 
pur.add_element_atom(  'C ', 0.400878) 
pur.add_element_atom(  'N ', 0.076459) 
pur.add_element_atom(  'O ', 0.162639)
pur.finalize()


#
#  swisspor Drain WS20, 20mm polypropylene stuff, mostly air
#
ws20 = calculate_materials.material('ws20',0.0325)
ws20.add_element_atom(  'H ', 0.666653) 
ws20.add_element_atom(  'C ', 0.333347) 
ws20.finalize()

































