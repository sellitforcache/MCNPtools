#
# Stainless Steel 316
#
ss316=calculate_materials.mixture('SS316')
ss316.mass_density=7.95
ss316.add_mixture( 'P'  ,    210.00, mode='mass')
ss316.add_mixture( 'Mo' ,   1990.00, mode='mass')
ss316.add_mixture( 'Zn' ,     12.00, mode='mass')
ss316.add_mixture( 'Pb' ,     40.00, mode='mass')
ss316.add_mixture( 'Co' ,   1330.00, mode='mass')
ss316.add_mixture( 'Ni' ,  87600.00, mode='mass')
ss316.add_mixture( 'Si' ,   4010.00, mode='mass')
ss316.add_mixture( 'Mn' ,  13600.00, mode='mass')
ss316.add_mixture( 'Fe' , 715109.00, mode='mass')
ss316.add_mixture( 'Cr' , 172000.00, mode='mass')
ss316.add_mixture( 'Mg' ,      3.10, mode='mass')
ss316.add_mixture( 'V'  ,    800.00, mode='mass')
ss316.add_mixture( 'Cu' ,   1240.00, mode='mass')
ss316.add_mixture( 'Ag' ,      6.00, mode='mass')
ss316.add_mixture( 'Ti' ,    128.00, mode='mass')
ss316.add_mixture( 'Ca' ,      4.40, mode='mass')
ss316.add_mixture( 'Al' ,     35.00, mode='mass')
ss316.add_mixture( 'Sr' ,      0.30, mode='mass')
ss316.add_mixture( 'K'  ,      2.10, mode='mass')
ss316.add_mixture( 'Cs' ,     13.00, mode='mass')
ss316.add_mixture( 'Rb' ,      5.00, mode='mass')
ss316.add_mixture( 'W'  ,   1350.00, mode='mass')
ss316.add_mixture( 'Ga' ,    123.00, mode='mass')
ss316.add_mixture( 'C'  ,    390.00, mode='mass')
ss316.finalize()

#
#  Neodymium permanent magnets
#
neomag = calculate_materials.mixture('NeoMag')
neomag.mass_density=7.4
neomag.add_mixture( 'Nd'  ,  2.00, mode='atom')
neomag.add_mixture( 'Fe'  , 14.00, mode='atom')
neomag.add_mixture( 'B'   ,  1.00, mode='atom')
neomag.finalize()

#
#  zircaloy-2
#
zircII = calculate_materials.mixture('Zircaloy-II')
zircII.mass_density=11.32
zircII.add_mixture( 'Zr',980700.0,mode='mass')
zircII.add_mixture( 'Sn', 14600.0,mode='mass')
zircII.add_mixture( 'Fe',  1500.0,mode='mass')
zircII.add_mixture( 'Cr',  2500.0,mode='mass')
zircII.add_mixture( 'Ni',   500.0,mode='mass')
zircII.add_mixture( 'Hf',   200.0,mode='mass')
zircII.finalize()

#
# T91 steel
# wt%, from http://pure.qub.ac.uk/portal/files/17599818/341_manuscript.pdf  
t91 = calculate_materials.mixture('T91')
t91.mass_density=7.76
t91.add_mixture( 'Fe',  89.4, mode='mass')
t91.add_mixture( 'C' ,  0.10, mode='mass')    
t91.add_mixture( 'Si',  0.26, mode='mass')    
t91.add_mixture( 'V' ,  0.2 , mode='mass')     
t91.add_mixture( 'Cr',  8.45, mode='mass')   
t91.add_mixture( 'Mn',  0.46, mode='mass')    
t91.add_mixture( 'Ni',  0.17, mode='mass')    
t91.add_mixture( 'Mo',  0.92, mode='mass')    
t91.add_mixture( 'Nb',  0.04, mode='mass')    
t91.finalize()

#
# SIMP steel
# wt%, from http://pure.qub.ac.uk/portal/files/17599818/341_manuscript.pdf # couldn't find reference for density...
simp = calculate_materials.mixture('SIMP')
simp.mass_density=7.8
simp.add_mixture( 'Fe',   84.53, mode='mass')
simp.add_mixture( 'C' ,   0.25 , mode='mass')    
simp.add_mixture( 'Si',   1.5  , mode='mass')    
simp.add_mixture( 'V',    0.2  , mode='mass')    
simp.add_mixture( 'Cr',   10.8 , mode='mass')    
simp.add_mixture( 'Mn',   0.5  , mode='mass')    
simp.add_mixture( 'W',    1.2  , mode='mass')    
simp.add_mixture( 'Mo',   0.9  , mode='mass')    
simp.add_mixture( 'Nb',   0.01 , mode='mass')    
simp.add_mixture( 'Ta',   0.11 , mode='mass') 
simp.finalize()

#
# CLAM steel
# http://www.sciencedirect.com/science/article/pii/S0261306914004774 # couldn't find reference for density...
clam = calculate_materials.mixture('CLAM')
clam.mass_density=7.8
clam.add_mixture( 'Fe', 88.709, mode='mass')
clam.add_mixture( 'C',   0.091, mode='mass')
clam.add_mixture( 'Cr',  8.93 , mode='mass')
clam.add_mixture( 'Mn',  0.49 , mode='mass')
clam.add_mixture( 'W',   1.51 , mode='mass') 
clam.add_mixture( 'V',   0.15 , mode='mass')
clam.add_mixture( 'Ta',  0.15 , mode='mass')
clam.finalize()

#
# Al6061
# http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA6061t6
al_6061 = calculate_materials.mixture('Al6061')
al_6061.mass_density=2.7
al_6061.add_mixture( 'Al',  97.2 , mode='mass')
al_6061.add_mixture( 'Cr',  0.195, mode='mass')
al_6061.add_mixture( 'Cu',  0.275, mode='mass')
al_6061.add_mixture( 'Fe',  0.35 , mode='mass') 
al_6061.add_mixture( 'Mg',  1.0  , mode='mass')
al_6061.add_mixture( 'Mn',  0.075, mode='mass')	 	 
al_6061.add_mixture( 'Si',  0.6  , mode='mass')
al_6061.add_mixture( 'Ti',  0.075, mode='mass')	 
al_6061.add_mixture( 'Zn',  0.125, mode='mass')
al_6061.finalize()

#
# Ti6Al4V
#
ti6al4v = calculate_materials.mixture('Ti6Al4V')
ti6al4v.mass_density=4.43
ti6al4v.add_mixture( 'Ti', 6.0 , mode='atom')
ti6al4v.add_mixture( 'Al', 4.0 , mode='atom')
ti6al4v.add_mixture( 'V' , 1.0 , mode='atom')
ti6al4v.finalize()

#
# Ti3AlC2
#
ti3alc2 = calculate_materials.mixture('Ti3AlC2')
ti3alc2.mass_density=4.24
ti3alc2.add_mixture( 'Ti', 3.0 , mode='atom')
ti3alc2.add_mixture( 'Al', 1.0 , mode='atom')
ti3alc2.add_mixture( 'C' , 2.0 , mode='atom')
ti3alc2.finalize()

#
# Ti3SiC2
#
ti3sic2 = calculate_materials.mixture('Ti3SiC2')
ti3sic2.mass_density=4.53
ti3sic2.add_mixture( 'Ti', 3.0 , mode='atom')
ti3sic2.add_mixture( 'Si', 1.0 , mode='atom')
ti3sic2.add_mixture( 'C' , 2.0 , mode='atom')
ti3sic2.finalize()

#
# Ti2AlC
#
ti3alc = calculate_materials.mixture('Ti2AlC')
ti3alc.mass_density=4.25
ti3alc.add_mixture( 'Ti', 3.0 , mode='atom')
ti3alc.add_mixture( 'Al', 1.0 , mode='atom')
ti3alc.add_mixture( 'C' , 1.0 , mode='atom')
ti3alc.finalize()

#
# Y2O3
#
y2o3 = calculate_materials.mixture('Y2O3')
y2o3.mass_density=5.010
y2o3.add_mixture('Y',2.0,mode='atom')
y2o3.add_mixture('O',3.0,mode='atom')
y2o3.finalize()

#
# 9Cr-ODS
#
cr9_ods = calculate_materials.mixture('9Cr-ODS')
cr9_ods.mass_density=7.8
cr9_ods.add_mixture( 'Fe'   , 87.85 , mode='mass')
cr9_ods.add_mixture( 'Cr'   ,  9.0  , mode='mass')
cr9_ods.add_mixture( 'W'    ,  2.5  , mode='mass')
cr9_ods.add_mixture( 'Ti'   ,  0.4  , mode='mass') 
cr9_ods.add_mixture( 'Y2O3' ,  0.25 , mode='mass')   
cr9_ods.finalize()

#
# 14Cr-ODS
#
cr14_ods = calculate_materials.mixture('14Cr-ODS')
cr14_ods.mass_density=7.8
cr14_ods.add_mixture( 'Fe'   , 82.85 , mode='mass')
cr14_ods.add_mixture( 'Cr'   , 14.0  , mode='mass')
cr14_ods.add_mixture( 'W'    ,  2.5  , mode='mass')
cr14_ods.add_mixture( 'Ti'   ,  0.4  , mode='mass') 
cr14_ods.add_mixture( 'Y2O3' ,  0.25 , mode='mass')   
cr14_ods.finalize()

#
# Fe-Cr alloy
#
fecr = calculate_materials.mixture('FeCr')
fecr.mass_density=7.8
fecr.add_mixture( 'Fe', 88.0 , mode='mass')
fecr.add_mixture( 'Cr', 12.0 , mode='mass')
fecr.finalize()

#
# SiC
#
sic = calculate_materials.mixture('SiC')
sic.mass_density=3.21
sic.add_mixture( 'Si', 1.0 , mode='atom')
sic.add_mixture( 'C',  1.0 , mode='atom')
sic.finalize()

#
# B4C
#
b4c = calculate_materials.mixture('B4C')
b4c.mass_density=2.52
b4c.add_mixture( 'B',  4.0 , mode='atom')
b4c.add_mixture( 'C',  1.0 , mode='atom')
b4c.finalize()

#
# high density polyethylene
#
hdpe = calculate_materials.mixture('HDPE')
hdpe.mass_density=0.95
hdpe.add_mixture( 'H',  4.0 , mode='atom')
hdpe.add_mixture( 'C',  2.0 , mode='atom')
hdpe.finalize()

#
# Borated concrete
#
concrete_borated = calculate_materials.mixture('Borated Concrete')
concrete_borated.mass_density=3.10
concrete_borated.add_mixture( 'H ', 0.005600, mode='mass')
concrete_borated.add_mixture( 'B ', 0.010400, mode='mass')
concrete_borated.add_mixture( 'O ', 0.338000, mode='mass')
concrete_borated.add_mixture( 'F ', 0.002300, mode='mass')
concrete_borated.add_mixture( 'Na', 0.012100, mode='mass')
concrete_borated.add_mixture( 'Mg', 0.002300, mode='mass')
concrete_borated.add_mixture( 'Al', 0.006400, mode='mass')
concrete_borated.add_mixture( 'Si', 0.033100, mode='mass')
concrete_borated.add_mixture( 'S ', 0.091500, mode='mass')
concrete_borated.add_mixture( 'K ', 0.001000, mode='mass')
concrete_borated.add_mixture( 'Ca', 0.062600, mode='mass')
concrete_borated.add_mixture( 'Mn', 0.000200, mode='mass')
concrete_borated.add_mixture( 'Fe', 0.021900, mode='mass')
concrete_borated.add_mixture( 'Zn', 0.006600, mode='mass')
concrete_borated.add_mixture( 'Ba', 0.401300, mode='mass')
concrete_borated.finalize()

#
# borosilicate glass
#
glass_borosilicate = calculate_materials.mixture('Borosilicate Glass')
glass_borosilicate.mass_density=2.23
glass_borosilicate.add_mixture( 'B ', 0.040066, mode='mass')
glass_borosilicate.add_mixture( 'O ', 0.539559, mode='mass')
glass_borosilicate.add_mixture( 'Na', 0.028191, mode='mass')
glass_borosilicate.add_mixture( 'Al', 0.011644, mode='mass')
glass_borosilicate.add_mixture( 'Si', 0.377220, mode='mass')
glass_borosilicate.add_mixture( 'K ', 0.003321, mode='mass')
glass_borosilicate.finalize()

#
# borosilicate glass PSI from NAA irradiation
#
glass_borosilicate_PSI = calculate_materials.mixture('Borosilicate Glass PSI NAA')
glass_borosilicate_PSI.mass_density=2.23
glass_borosilicate_PSI.add_mixture( 'B ', 0.040066,  mode='mass')
glass_borosilicate_PSI.add_mixture( 'O ', 0.539559,  mode='mass')
glass_borosilicate_PSI.add_mixture( 'Na', 0.028191,  mode='mass')
glass_borosilicate_PSI.add_mixture( 'Al', 0.011644,  mode='mass')
glass_borosilicate_PSI.add_mixture( 'Si', 0.377220,  mode='mass')
glass_borosilicate_PSI.add_mixture( 'K ', 0.003321,  mode='mass')
glass_borosilicate_PSI.add_mixture( 'Sc', 0.58*1e-6, mode='mass') 
glass_borosilicate_PSI.add_mixture( 'La', 3.87*1e-6, mode='mass')
glass_borosilicate_PSI.finalize()

#
# plate glass
#
glass_plate = calculate_materials.mixture('Plate Glass')
glass_plate.mass_density=2.40
glass_plate.add_mixture(  'O ', 0.459800, mode='mass') 
glass_plate.add_mixture(  'Na', 0.096441, mode='mass') 
glass_plate.add_mixture(  'Si', 0.336553, mode='mass') 
glass_plate.add_mixture(  'Ca', 0.107205, mode='mass')
glass_plate.finalize()

#
# plate glass PSI from NAA irradiation
#
glass_plate_PSI = calculate_materials.mixture('Plate Glass PSI NAA')
glass_plate_PSI.mass_density=2.40
glass_plate_PSI.add_mixture(  'O ', 0.459800,  mode='mass') 
glass_plate_PSI.add_mixture(  'Na', 0.096441,  mode='mass') 
glass_plate_PSI.add_mixture(  'Si', 0.336553,  mode='mass') 
glass_plate_PSI.add_mixture(  'Ca', 0.107205,  mode='mass')
glass_plate_PSI.add_mixture(  'Sc', 0.58*1e-6, mode='mass') 
glass_plate_PSI.add_mixture(  'La', 3.87*1e-6, mode='mass')
glass_plate_PSI.finalize()


#
# m=2 guide layers
#
guide_layers = calculate_materials.mixture('Guide Layers')
guide_layers.mass_density=2.40
guide_layers.add_mixture(  'Ni', 7.07348E-01,   mode='volume') 
guide_layers.add_mixture(  'Ti', 2.92652E-01,   mode='volume') 
guide_layers.finalize()


#
# m=2 guide layers, PSI from NAA irradiation
#
guide_layers_PSI = calculate_materials.mixture('Guide Layers PSI NAA')
guide_layers_PSI.mass_density=2.40
guide_layers_PSI.add_mixture(  'Ni', 0.82573012,   mode='mass') 
guide_layers_PSI.add_mixture(  'Ti', 0.17426988,   mode='mass') 
guide_layers_PSI.add_mixture(  'Co', 5.96*1e-6,    mode='mass') 
guide_layers_PSI.add_mixture(  'Cr', 8000*1e-6,    mode='mass') 
guide_layers_PSI.finalize()

#
# Schrottbeton/heavy concrete/heavy mortar
# Assay number   10 : Representative Schrottbeton
#
schrottbeton = calculate_materials.mixture('Schrottbeton')
schrottbeton.mass_density=5.7
schrottbeton.add_mixture( 'H ',   3000.00, mode='mass')
schrottbeton.add_mixture( 'Li',      0.10, mode='mass')
schrottbeton.add_mixture( 'Be',      0.09, mode='mass')
schrottbeton.add_mixture( 'B ',     63.0 , mode='mass')
schrottbeton.add_mixture( 'C ',   3000.00, mode='mass')
schrottbeton.add_mixture( 'N ',     70.00, mode='mass')
schrottbeton.add_mixture( 'O ',  80000.00, mode='mass')
schrottbeton.add_mixture( 'Na',     87.00, mode='mass')
schrottbeton.add_mixture( 'Mg',    837.00, mode='mass')
schrottbeton.add_mixture( 'Al',   3270.00, mode='mass')
schrottbeton.add_mixture( 'Si',  17600.00, mode='mass')
schrottbeton.add_mixture( 'P ',   5770.00, mode='mass')
schrottbeton.add_mixture( 'S ',   2560.00, mode='mass')
schrottbeton.add_mixture( 'Cl',     30.00, mode='mass')
schrottbeton.add_mixture( 'K ',    260.00, mode='mass')
schrottbeton.add_mixture( 'Ca',    280.00, mode='mass')
schrottbeton.add_mixture( 'Ti',    555.00, mode='mass')
schrottbeton.add_mixture( 'V ',    510.00, mode='mass')
schrottbeton.add_mixture( 'Cr',    710.00, mode='mass')
schrottbeton.add_mixture( 'Mn',   4300.00, mode='mass')
schrottbeton.add_mixture( 'Fe', 861000.00, mode='mass')
schrottbeton.add_mixture( 'Co',    120.00, mode='mass')
schrottbeton.add_mixture( 'Ni',    615.00, mode='mass')
schrottbeton.add_mixture( 'Cu',   1700.00, mode='mass')
schrottbeton.add_mixture( 'Zn',     77.00, mode='mass')
schrottbeton.add_mixture( 'Ga',     10.00, mode='mass')
schrottbeton.add_mixture( 'As',    238.00, mode='mass')
schrottbeton.add_mixture( 'Rb',      3.00, mode='mass')
schrottbeton.add_mixture( 'Sr',    140.00, mode='mass')
schrottbeton.add_mixture( 'Y ',      1.00, mode='mass')
schrottbeton.add_mixture( 'Zr',     10.00, mode='mass')
schrottbeton.add_mixture( 'Nb',      1.00, mode='mass')
schrottbeton.add_mixture( 'Mo',     50.00, mode='mass')
schrottbeton.add_mixture( 'Ag',      0.70, mode='mass')
schrottbeton.add_mixture( 'Sn',      5.00, mode='mass')
schrottbeton.add_mixture( 'Sb',     70.00, mode='mass')
schrottbeton.add_mixture( 'Te',    100.00, mode='mass')
schrottbeton.add_mixture( 'Cs',      6.00, mode='mass')
schrottbeton.add_mixture( 'Ba',     55.00, mode='mass')
schrottbeton.add_mixture( 'La',      5.00, mode='mass')
schrottbeton.add_mixture( 'Ce',      1.00, mode='mass')
schrottbeton.add_mixture( 'Sm',      1.00, mode='mass')
schrottbeton.add_mixture( 'Eu',      0.10, mode='mass')
schrottbeton.add_mixture( 'Gd',      0.50, mode='mass')
schrottbeton.add_mixture( 'Dy',      0.30, mode='mass')
schrottbeton.add_mixture( 'Ho',      0.50, mode='mass')
schrottbeton.add_mixture( 'Yb',      0.10, mode='mass')
schrottbeton.add_mixture( 'Lu',     20.00, mode='mass')
schrottbeton.add_mixture( 'W ',    380.00, mode='mass')
schrottbeton.add_mixture( 'Tl',      2.00, mode='mass') 
schrottbeton.add_mixture( 'Pb',      6.00, mode='mass')
schrottbeton.add_mixture( 'Bi',      1.00, mode='mass')
schrottbeton.add_mixture( 'Th',      0.50, mode='mass')
schrottbeton.add_mixture( 'U ',      1.00, mode='mass')
schrottbeton.finalize()

#
#  
# schrottbeton from some old mcnp definition
#
schrottbeton2 = calculate_materials.mixture('Schrottbeton-PSI')
schrottbeton2.mass_density=4.783
schrottbeton2.add_mixture( 'H ',   0.004395, mode='mass')
schrottbeton2.add_mixture( 'O ',   0.184241, mode='mass') 
schrottbeton2.add_mixture( 'Fe',   0.765413, mode='mass')
schrottbeton2.add_mixture( 'Ca',   0.002704, mode='mass')
schrottbeton2.add_mixture( 'Si',   0.020705, mode='mass')
schrottbeton2.add_mixture( 'Al',   0.002077, mode='mass')
schrottbeton2.finalize()

#
# Bundeseisen , calculated from drawing 0-10009.22.026
#
bundeseisen = calculate_materials.mixture('Bundeseisen')
bundeseisen.mass_density=7.80488
bundeseisen.add_mixture( 'C' 	,	2689.	, mode='mass')
bundeseisen.add_mixture( 'Na' 	,	2.		, mode='mass')
bundeseisen.add_mixture( 'Mg' 	,	5.		, mode='mass')
bundeseisen.add_mixture( 'Al' 	,	100.	, mode='mass')
bundeseisen.add_mixture( 'Si' 	,	7451.	, mode='mass')
bundeseisen.add_mixture( 'P' 	,	344.	, mode='mass')
bundeseisen.add_mixture( 'S' 	,	303.	, mode='mass')
bundeseisen.add_mixture( 'K' 	,	17.		, mode='mass')
bundeseisen.add_mixture( 'Ca' 	,	13.		, mode='mass')
bundeseisen.add_mixture( 'Ti' 	,	12.		, mode='mass')
bundeseisen.add_mixture( 'V' 	,	310.	, mode='mass')
bundeseisen.add_mixture( 'Cr' 	,	728.	, mode='mass')
bundeseisen.add_mixture( 'Mn' 	,	9699.	, mode='mass')
bundeseisen.add_mixture( 'Fe' 	,	971278.	, mode='mass')
bundeseisen.add_mixture( 'Co' 	,	153.	, mode='mass')
bundeseisen.add_mixture( 'Ni' 	,	1796.	, mode='mass')
bundeseisen.add_mixture( 'Cu' 	,	3701.	, mode='mass')
bundeseisen.add_mixture( 'Zn' 	,	70.		, mode='mass')
bundeseisen.add_mixture( 'As' 	,	245.	, mode='mass')
bundeseisen.add_mixture( 'Rb' 	,	19.		, mode='mass')
bundeseisen.add_mixture( 'Mo' 	,	95.		, mode='mass')
bundeseisen.add_mixture( 'Sn' 	,	769.	, mode='mass')
bundeseisen.add_mixture( 'Cs' 	,	93.		, mode='mass')
bundeseisen.add_mixture( 'Yb' 	,	1.		, mode='mass')
bundeseisen.add_mixture( 'W' 	,	3.		, mode='mass')
bundeseisen.add_mixture( 'Pb' 	,	84.		, mode='mass')
bundeseisen.finalize()

#
#  Granatsand, Australien
#  4.1 g/cc solid, 2.4 bulk, from http://www.abritec.ch/index.php?nav=5,32
granatsand1 = calculate_materials.mixture('Granatsand 1')
granatsand1.mass_density=2.40
granatsand1.add_mixture( 'P' 	,240.	 , mode='mass')
granatsand1.add_mixture( 'S' 	,270.	 , mode='mass')
granatsand1.add_mixture( 'As' 	,20.	 , mode='mass')
granatsand1.add_mixture( 'Sn' 	,20.	 , mode='mass')
granatsand1.add_mixture( 'Hg' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Mo' 	,3.		 , mode='mass')
granatsand1.add_mixture( 'Cr' 	,142.	 , mode='mass')
granatsand1.add_mixture( 'Zn' 	,43.4	 , mode='mass')
granatsand1.add_mixture( 'Pb' 	,46.	 , mode='mass')
granatsand1.add_mixture( 'Co' 	,34.	 , mode='mass')
granatsand1.add_mixture( 'Cd' 	,1.0	 , mode='mass')
granatsand1.add_mixture( 'Ni' 	,20.	 , mode='mass')
granatsand1.add_mixture( 'B' 	,7.		 , mode='mass')
granatsand1.add_mixture( 'Si' 	,17.6e4	 , mode='mass')
granatsand1.add_mixture( 'Mn' 	,0.72e4	 , mode='mass')
granatsand1.add_mixture( 'Fe' 	,22.9e4	 , mode='mass')
granatsand1.add_mixture( 'Mg' 	,3.57e4	 , mode='mass')
granatsand1.add_mixture( 'V' 	,140.	 , mode='mass')
granatsand1.add_mixture( 'Be' 	,0.5	 , mode='mass')
granatsand1.add_mixture( 'Cu' 	,2.		 , mode='mass')
granatsand1.add_mixture( 'Ag' 	,2.		 , mode='mass')
granatsand1.add_mixture( 'Ti' 	,89.5	 , mode='mass')
granatsand1.add_mixture( 'Zr' 	,33.	 , mode='mass')
granatsand1.add_mixture( 'Ca' 	,1.03e4	 , mode='mass')
granatsand1.add_mixture( 'Al' 	,10.6e4	 , mode='mass')
granatsand1.add_mixture( 'Sr' 	,11.8	 , mode='mass')
granatsand1.add_mixture( 'Ba' 	,64.4	 , mode='mass')
granatsand1.add_mixture( 'Na' 	,72.	 , mode='mass')
granatsand1.add_mixture( 'Li' 	,8.		 , mode='mass')
granatsand1.add_mixture( 'K' 	,85.	 , mode='mass')
granatsand1.add_mixture( 'Rb' 	,1.		 , mode='mass')
granatsand1.add_mixture( 'Cs' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Se' 	,20.	 , mode='mass')
granatsand1.add_mixture( 'W' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Te' 	,108.	 , mode='mass')
granatsand1.add_mixture( 'Sb' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Re' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Bi' 	,15.	 , mode='mass')
granatsand1.add_mixture( 'Ir' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Os' 	,20.	 , mode='mass')
granatsand1.add_mixture( 'In' 	,20.	 , mode='mass')
granatsand1.add_mixture( 'Ru' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Au' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Ge' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Ta' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Ga' 	,23.	 , mode='mass')
granatsand1.add_mixture( 'Pr' 	,50.	 , mode='mass')
granatsand1.add_mixture( 'Nb' 	,2.		 , mode='mass')
granatsand1.add_mixture( 'Hf' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Pd' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Rh' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Tl' 	,26.	 , mode='mass')
granatsand1.add_mixture( 'U' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Th' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Lu' 	,17.2	 , mode='mass')
granatsand1.add_mixture( 'Yb' 	,46.9	 , mode='mass')
granatsand1.add_mixture( 'Gd' 	,98.	 , mode='mass')
granatsand1.add_mixture( 'Ho' 	,8.		 , mode='mass')
granatsand1.add_mixture( 'Tm' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Dy' 	,30.	 , mode='mass')
granatsand1.add_mixture( 'Sm' 	,10.	 , mode='mass')
granatsand1.add_mixture( 'Sc' 	,1333.	 , mode='mass')
granatsand1.add_mixture( 'Tb' 	,5.		 , mode='mass')
granatsand1.add_mixture( 'Y' 	,322.	 , mode='mass')
granatsand1.add_mixture( 'La' 	,15.	 , mode='mass')
granatsand1.add_mixture( 'Eu' 	,0.5	 , mode='mass')
granatsand1.add_mixture( 'Er' 	,35.	 , mode='mass')
granatsand1.add_mixture( 'Pr' 	,3.		 , mode='mass')
granatsand1.add_mixture( 'Ce' 	,25.	 , mode='mass')
granatsand1.add_mixture( 'Nd' 	,11. 	 , mode='mass')
granatsand1.add_mixture( 'O' 	,432070.8, mode='mass')  # balance
granatsand1.finalize()

#
#  Granatsand, "Neuer Abschirmsand"
#  4.1 g/cc solid, 2.4 bulk, from http://www.abritec.ch/index.php?nav=5,32
granatsand2 = calculate_materials.mixture('Granatsand 2')
granatsand2.mass_density=2.40
granatsand2.add_mixture(  'Lu'	,	15.3		, mode='mass')
granatsand2.add_mixture(  'Yb'	,	18.4		, mode='mass')
granatsand2.add_mixture(  'Gd'	,	103.		, mode='mass')
granatsand2.add_mixture(  'Ho'	,	1.			, mode='mass')
granatsand2.add_mixture(  'Tm'	,	2.			, mode='mass')
granatsand2.add_mixture(  'Dy'	,	1.			, mode='mass')
granatsand2.add_mixture(  'Sm'	,	5.			, mode='mass')
granatsand2.add_mixture(  'Sc'	,	119.		, mode='mass')
granatsand2.add_mixture(  'Tb'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Y'	,	133.		, mode='mass')
granatsand2.add_mixture(  'La'	,	12.			, mode='mass')
granatsand2.add_mixture(  'Eu'	,	1.			, mode='mass')
granatsand2.add_mixture(  'Er'	,	13.			, mode='mass')
granatsand2.add_mixture(  'Pr'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Ce'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Nd'	,	10.			, mode='mass')
granatsand2.add_mixture(  'P'	,	450.		, mode='mass')
granatsand2.add_mixture(  'S'	,	370.		, mode='mass')
granatsand2.add_mixture(  'As'	,	20.			, mode='mass')
granatsand2.add_mixture(  'Sn'	,	20.			, mode='mass')
granatsand2.add_mixture(  'Hg'	,	20.			, mode='mass')
granatsand2.add_mixture(  'Mo'	,	5.			, mode='mass')
granatsand2.add_mixture(  'Zn'	,	79.			, mode='mass')
granatsand2.add_mixture(  'Pb'	,	20.			, mode='mass')
granatsand2.add_mixture(  'Co'	,	30.			, mode='mass')
granatsand2.add_mixture(  'Cd'	,	1.			, mode='mass')
granatsand2.add_mixture(  'Ni'	,	3.			, mode='mass')
granatsand2.add_mixture(  'B'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Si'	,	206000.		, mode='mass')
granatsand2.add_mixture(  'Mn'	,	5550.		, mode='mass')
granatsand2.add_mixture(  'Fe'	,	301000.		, mode='mass')
granatsand2.add_mixture(  'Cr'	,	49.			, mode='mass')
granatsand2.add_mixture(  'Mg'	,	28100.		, mode='mass')
granatsand2.add_mixture(  'V'	,	74.			, mode='mass')
granatsand2.add_mixture(  'Be'	,	0.5			, mode='mass')
granatsand2.add_mixture(  'Cu'	,	26.			, mode='mass')
granatsand2.add_mixture(  'Ag'	,	9.			, mode='mass')
granatsand2.add_mixture(  'Ti'	,	1790.		, mode='mass')
granatsand2.add_mixture(  'Zr'	,	84.			, mode='mass')
granatsand2.add_mixture(  'Ca'	,	14900.		, mode='mass')
granatsand2.add_mixture(  'Al'	,	127000.		, mode='mass')
granatsand2.add_mixture(  'Sr'	,	9.86		, mode='mass')
granatsand2.add_mixture(  'Ba'	,	225.		, mode='mass')
granatsand2.add_mixture(  'Na'	,	837.		, mode='mass')
granatsand2.add_mixture(  'Li'	,	5.			, mode='mass')
granatsand2.add_mixture(  'K'	,	1050.		, mode='mass')
granatsand2.add_mixture(  'Cs'	,	3.			, mode='mass')
granatsand2.add_mixture(  'Rb'	,	18.			, mode='mass')
granatsand2.add_mixture(  'Se'	,	20.			, mode='mass')
granatsand2.add_mixture(  'W'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Te'	,	50.			, mode='mass')
granatsand2.add_mixture(  'Sb'	,	20.			, mode='mass')
granatsand2.add_mixture(  'Re'	,	5.			, mode='mass')
granatsand2.add_mixture(  'Bi'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Ir'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Os'	,	20.			, mode='mass')
granatsand2.add_mixture(  'In'	,	50.			, mode='mass')
granatsand2.add_mixture(  'Ru'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Au'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Ge'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Ta'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Ga'	,	28.			, mode='mass')
granatsand2.add_mixture(  'Pt'	,	50.			, mode='mass')
granatsand2.add_mixture(  'Nb'	,	5.			, mode='mass')
granatsand2.add_mixture(  'Hf'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Pd'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Rh'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Tl'	,	50.			, mode='mass')
granatsand2.add_mixture(  'U'	,	10.			, mode='mass')
granatsand2.add_mixture(  'Th'	,	5.			, mode='mass')
granatsand2.add_mixture(  'O'	,	311364.94  	, mode='mass') # balance
granatsand2.finalize()

#
# soil, from PNNL-15870 Rev. 1
#
soil = calculate_materials.mixture('soil')
soil.mass_density=1.52
soil.add_mixture(  'H ', 0.316855, mode='atom') 
soil.add_mixture(  'O ', 0.501581, mode='atom') 
soil.add_mixture(  'Al', 0.039951, mode='atom') 
soil.add_mixture(  'Si', 0.141613, mode='atom')
soil.finalize()

#
# asphalt/bitumen full density from PNNL-15870 Rev. 1
#
asphalt = calculate_materials.mixture('asphalt')
asphalt.mass_density=1.3
asphalt.add_mixture(  'H ', 0.586755, mode='atom') 
asphalt.add_mixture(  'C ', 0.402588, mode='atom') 
asphalt.add_mixture(  'N ', 0.002463, mode='atom') 
asphalt.add_mixture(  'O ', 0.001443, mode='atom')
asphalt.add_mixture(  'S ', 0.006704, mode='atom') 
asphalt.add_mixture(  'V ', 0.000044, mode='atom') 
asphalt.add_mixture(  'Ni', 0.000003, mode='atom')
asphalt.finalize()

#
# polyurethane foam insulation, from PNNL-15870 Rev. 1, swisspor PUR premium
#
pur = calculate_materials.mixture('pur')
pur.mass_density=0.03
pur.add_mixture(  'H ', 0.360023, mode='atom') 
pur.add_mixture(  'C ', 0.400878, mode='atom') 
pur.add_mixture(  'N ', 0.076459, mode='atom') 
pur.add_mixture(  'O ', 0.162639, mode='atom')
pur.finalize()

#
#  swisspor Drain WS20, 20mm polypropylene stuff, mostly air
#
ws20 = calculate_materials.mixture('ws20')
ws20.mass_density=0.0325
ws20.add_mixture(  'H ', 0.666653, mode='atom') 
ws20.add_mixture(  'C ', 0.333347, mode='atom') 
ws20.finalize()

#
#  E24 Steel, 0.05% Co, >99% Fe+C
#
E24 = calculate_materials.mixture('E24-insert')
E24.mass_density=7.85
E24.add_mixture('Fe'  ,  0.990         , mode='mass')
E24.add_mixture('C '  ,  0.0044        , mode='mass')
E24.add_mixture('Co'  ,  0.0005        , mode='mass')
E24.add_mixture('Si'  ,  1.63200000e-04, mode='mass')
E24.add_mixture('Mn'  ,  7.34400000e-04, mode='mass')
E24.add_mixture('S '  ,  6.52800000e-05, mode='mass')
E24.add_mixture('P '  ,  5.71200000e-05, mode='mass')
E24.add_mixture('Cr'  ,  1.63200000e-03, mode='mass')
E24.add_mixture('Mo'  ,  3.26400000e-04, mode='mass')
E24.add_mixture('Ni'  ,  2.12160000e-03, mode='mass')
E24.finalize()

#
#  GRANITE, from PNNL
#
granite = calculate_materials.mixture('granite')
granite.mass_density=2.69
granite.add_mixture( 'O ', 0.484170, mode='mass')
granite.add_mixture( 'Na', 0.027328, mode='mass')
granite.add_mixture( 'Mg', 0.004274, mode='mass')
granite.add_mixture( 'Al', 0.076188, mode='mass')
granite.add_mixture( 'Si', 0.336169, mode='mass')
granite.add_mixture( 'K ', 0.034144, mode='mass')
granite.add_mixture( 'Ca', 0.012985, mode='mass')
granite.add_mixture( 'Ti', 0.001795, mode='mass')
granite.add_mixture( 'Mn', 0.000387, mode='mass')
granite.add_mixture( 'Fe', 0.021555, mode='mass')
granite.add_mixture( 'Pb', 0.001004, mode='mass')
granite.finalize()

#
#  boric acid 
#
boric_acid = calculate_materials.mixture('boric_acid')
boric_acid.mass_density=1.435
boric_acid.add_mixture( 'O', 3.0, mode='atom')
boric_acid.add_mixture( 'H', 3.0, mode='atom')
boric_acid.add_mixture( 'B', 1.0, mode='atom')
boric_acid.finalize()



#
#  borax
#
borax = calculate_materials.mixture('borax')
borax.mass_density=1.73
borax.add_mixture( 'O ', 17., mode='atom')
borax.add_mixture( 'H ', 20., mode='atom')
borax.add_mixture( 'B ',  4., mode='atom')
borax.add_mixture( 'Na',  2., mode='atom')
borax.finalize()



#
#  light water 
#
light_water = calculate_materials.mixture('light water')
light_water.add_mixture( 'O', 1.0, mode='atom')
light_water.add_mixture( 'H', 2.0, mode='atom')
light_water.mass_density=1.0
light_water.finalize()

#
#  5% boron polyethylene 
#
bpe5 = calculate_materials.mixture('borated polyethylene 5%')
bpe5.mass_density=1.07
bpe5.add_mixture( 'H', 13.57143, mode='mass')
bpe5.add_mixture( 'C', 81.42857, mode='mass')
bpe5.add_mixture( 'B',  5.00000, mode='mass')
bpe5.finalize()

#
#  5% boron polyethylene 
#
bpe_b4c5 = calculate_materials.mixture('borated polyethylene 5wt% B4C')
bpe_b4c5.mass_density=1.07
bpe_b4c5.add_mixture( 'HDPE', 0.95, mode='mass')
bpe_b4c5.add_mixture( 'B4C',  0.05, mode='mass')
bpe_b4c5.finalize()

#
#  30% boron polyethylene 
#
bpe30 = calculate_materials.mixture('borated polyethylene 30%')
bpe30.mass_density=1.19
bpe30.add_mixture( 'H', 10.0, mode='mass')
bpe30.add_mixture( 'C', 60.0, mode='mass')
bpe30.add_mixture( 'B', 30.0, mode='mass')
bpe30.finalize()


#
#  SIEMENS composition concrete
#
concrete_seimens = calculate_materials.mixture('concrete, SIEMENS')
concrete_seimens.mass_density=2.3
concrete_seimens.add_mixture( 'H'  ,  3.3E-3  , mode='mass')
concrete_seimens.add_mixture( 'O'  ,  5.597E-1, mode='mass')
concrete_seimens.add_mixture( 'Al' ,  4.86E-2 , mode='mass')
concrete_seimens.add_mixture( 'Si' ,  1.942E-1, mode='mass')
concrete_seimens.add_mixture( 'Ca' ,  1.942E-1, mode='mass')
concrete_seimens.finalize()



#
#
# gravel, rock average of 5 types, PNNL
#
#
gravel = calculate_materials.mixture('gravel')
gravel.mass_density=2.662
gravel.add_mixture('H '  , 0.001657, mode='mass')
gravel.add_mixture('C '  , 0.026906, mode='mass')
gravel.add_mixture('O '  , 0.488149, mode='mass')
gravel.add_mixture('Na'  , 0.012403, mode='mass')
gravel.add_mixture('Mg'  , 0.023146, mode='mass')
gravel.add_mixture('Al'  , 0.054264, mode='mass')
gravel.add_mixture('Si'  , 0.246249, mode='mass')
gravel.add_mixture('S '  , 0.000577, mode='mass')
gravel.add_mixture('K '  , 0.018147, mode='mass')
gravel.add_mixture('Ca'  , 0.089863, mode='mass')
gravel.add_mixture('Ti'  , 0.003621, mode='mass')
gravel.add_mixture('Mn'  , 0.000386, mode='mass')
gravel.add_mixture('Fe'  , 0.033377, mode='mass')
gravel.add_mixture('Pb'  , 0.001255, mode='mass')
gravel.finalize()

#
#  dry air @ 20 degC
#
dryair = calculate_materials.mixture('dry air')
dryair.mass_density=0.00120479
dryair.add_mixture('C' , 0.000150, mode='atom')
dryair.add_mixture('N' , 0.784431, mode='atom')
dryair.add_mixture('O' , 0.210748, mode='atom')
dryair.add_mixture('Ar', 0.004671, mode='atom')
dryair.finalize()

#
#  45% RH air @ 24 degC
#
air_45RH_24C = calculate_materials.mixture('air 45RH 24C')
air_45RH_24C.mass_density=0.0011935
air_45RH_24C.add_mixture('dry air'     , 0.99172, mode='mass')
air_45RH_24C.add_mixture('light water' , 0.00828, mode='mass')
air_45RH_24C.finalize()

#
# pure He3
#
He3=calculate_materials.mixture('He3')
He3.atom_fractions[2003]=1.0
He3.mass_density=0.00018
He3.finalize()


#
#  low efficiency He3 counter
#
low_eff_he3 = calculate_materials.mixture('low eff he3')
low_eff_he3.mass_density=3.485e-3
low_eff_he3.add_mixture('Kr'  , 500., mode='atom')
low_eff_he3.add_mixture('He3' ,   1., mode='atom')
low_eff_he3.finalize()

#
#  normal efficiency He3 counter
#
normal_eff_he3 = calculate_materials.mixture('normal eff he3')
normal_eff_he3.mass_density=4.468741e-3
normal_eff_he3.add_mixture('Kr'  , 1.2, mode='atom')
normal_eff_he3.add_mixture('He3' , 2.3, mode='atom')
normal_eff_he3.finalize()

#
# ST37 steel comp from K Geismann, 1993
#
st37 = calculate_materials.mixture('ST37')
st37.mass_density=7.85
st37.add_mixture('P ' ,     120.0, mode='mass')
st37.add_mixture('S ' ,      20.0, mode='mass')
st37.add_mixture('As' ,      40.0, mode='mass')
st37.add_mixture('Sn' ,      20.0, mode='mass')
st37.add_mixture('Hg' ,      30.0, mode='mass')
st37.add_mixture('Mn' ,      80.0, mode='mass')
st37.add_mixture('Cr' ,     226.0, mode='mass')
st37.add_mixture('Zn' ,     160.0, mode='mass')
st37.add_mixture('Pb' ,      20.0, mode='mass')
st37.add_mixture('Co' ,      34.0, mode='mass')
st37.add_mixture('Cd' ,       2.0, mode='mass')
st37.add_mixture('Ni' ,     477.0, mode='mass')
st37.add_mixture('B ' ,       3.0, mode='mass')
st37.add_mixture('Si' ,    1800.0, mode='mass')
st37.add_mixture('Mn' ,   10700.0, mode='mass')
st37.add_mixture('Fe' ,  983000.0, mode='mass')
st37.add_mixture('Mg' ,       8.8, mode='mass')
st37.add_mixture('V ' ,      64.0, mode='mass')
st37.add_mixture('Be' ,       0.5, mode='mass')
st37.add_mixture('Cu' ,     157.0, mode='mass')
st37.add_mixture('Ag' ,       3.0, mode='mass')
st37.add_mixture('Ti' ,       8.0, mode='mass')
st37.add_mixture('Zr' ,       2.0, mode='mass')
st37.add_mixture('Ca' ,      20.0, mode='mass')
st37.add_mixture('Al' ,     288.0, mode='mass')
st37.add_mixture('Sr' ,       0.3, mode='mass')
st37.add_mixture('Ba' ,       1.2, mode='mass')
st37.add_mixture('Na' ,      10.0, mode='mass')
st37.add_mixture('Li' ,       2.0, mode='mass')
st37.add_mixture('K ' ,       5.4, mode='mass')
st37.add_mixture('Rb' ,       5.0, mode='mass')
st37.add_mixture('Cs' ,       9.0, mode='mass')
st37.add_mixture('Se' ,      50.0, mode='mass')
st37.add_mixture('W ' ,      50.0, mode='mass')
st37.add_mixture('Te' ,     200.0, mode='mass')
st37.add_mixture('Sb' ,      20.0, mode='mass')
st37.add_mixture('Re' ,       5.0, mode='mass')
st37.add_mixture('Bi' ,      30.0, mode='mass')
st37.add_mixture('Ir' ,      30.0, mode='mass')
st37.add_mixture('Os' ,       3.0, mode='mass')
st37.add_mixture('In' ,      30.0, mode='mass')
st37.add_mixture('Ru' ,      10.0, mode='mass')
st37.add_mixture('Au' ,      20.0, mode='mass')
st37.add_mixture('Ge' ,      20.0, mode='mass')
st37.add_mixture('Ta' ,      20.0, mode='mass')
st37.add_mixture('Ga' ,      30.0, mode='mass')
st37.add_mixture('Pt' ,      20.0, mode='mass')
st37.add_mixture('Nb' ,      10.0, mode='mass')
st37.add_mixture('Hf' ,      20.0, mode='mass')
st37.add_mixture('Pd' ,      20.0, mode='mass')
st37.add_mixture('Rh' ,      10.0, mode='mass')
st37.add_mixture('Tl' ,      10.0, mode='mass')
st37.add_mixture('U ' ,      20.0, mode='mass')
st37.add_mixture('Th' ,      10.0, mode='mass')
st37.add_mixture('Lu' ,       5.0, mode='mass')
st37.add_mixture('Yb' ,       2.0, mode='mass')
st37.add_mixture('Gd' ,       5.0, mode='mass')
st37.add_mixture('Ho' ,       5.0, mode='mass')
st37.add_mixture('Tm' ,       5.0, mode='mass')
st37.add_mixture('Dy' ,       5.0, mode='mass')
st37.add_mixture('Sm' ,      10.0, mode='mass')
st37.add_mixture('Sc' ,       2.0, mode='mass')
st37.add_mixture('Tb' ,      20.0, mode='mass')
st37.add_mixture('Y ' ,       2.0, mode='mass')
st37.add_mixture('La' ,       5.0, mode='mass')
st37.add_mixture('Eu' ,       2.0, mode='mass')
st37.add_mixture('Er' ,       5.0, mode='mass')
st37.add_mixture('Pr' ,      20.0, mode='mass')
st37.add_mixture('Ce' ,      10.0, mode='mass')
st37.add_mixture('Nd' ,      10.0, mode='mass')
st37.add_mixture('C ' ,    1340.0, mode='mass')
st37.finalize()

#
# BEAM steel comp from S. Koechli, 2017 (Cr Co No Mo Fe, remaining adapted from ST37)
#
beam_steel = calculate_materials.mixture('beam steel')
beam_steel.mass_density=7.85
beam_steel.add_mixture('Cr' ,     365.0,       mode='mass')
beam_steel.add_mixture('Co' ,     136.0,       mode='mass')
beam_steel.add_mixture('Ni' ,     536.0,       mode='mass')
beam_steel.add_mixture('Mo' ,      64.0,       mode='mass')
beam_steel.add_mixture('Fe' ,  990575.0,       mode='mass')
beam_steel.add_mixture('P ' ,  6.41582632e+01, mode='mass')
beam_steel.add_mixture('S ' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('As' ,  2.13860877e+01, mode='mass')
beam_steel.add_mixture('Sn' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Hg' ,  1.60395658e+01, mode='mass')
beam_steel.add_mixture('Mn' ,  4.27721755e+01, mode='mass')
beam_steel.add_mixture('Zn' ,  8.55443510e+01, mode='mass')
beam_steel.add_mixture('Pb' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Si' ,  9.62373948e+02, mode='mass')
beam_steel.add_mixture('Mn' ,  5.72077847e+03, mode='mass')
beam_steel.add_mixture('V ' ,  3.42177404e+01, mode='mass')
beam_steel.add_mixture('Cu' ,  8.39403944e+01, mode='mass')
beam_steel.add_mixture('Ca' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Al' ,  1.53979832e+02, mode='mass')
beam_steel.add_mixture('Na' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Se' ,  2.67326097e+01, mode='mass')
beam_steel.add_mixture('W ' ,  2.67326097e+01, mode='mass')
beam_steel.add_mixture('Te' ,  1.06930439e+02, mode='mass')
beam_steel.add_mixture('Sb' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Bi' ,  1.60395658e+01, mode='mass')
beam_steel.add_mixture('Ir' ,  1.60395658e+01, mode='mass')
beam_steel.add_mixture('In' ,  1.60395658e+01, mode='mass')
beam_steel.add_mixture('Ru' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Au' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Ge' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Ta' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Ga' ,  1.60395658e+01, mode='mass')
beam_steel.add_mixture('Pt' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Nb' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Hf' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Pd' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Rh' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Tl' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('U ' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Th' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Sm' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Tb' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Pr' ,  1.06930439e+01, mode='mass')
beam_steel.add_mixture('Ce' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('Nd' ,  5.34652193e+00, mode='mass')
beam_steel.add_mixture('C ' ,  7.16433939e+02, mode='mass')
beam_steel.finalize()


#
# SRM 361 - AISI 4340 Steel (chip form)
#
srm361_steel = calculate_materials.mixture('SRM 361 - AISI 4340 steel')
srm361_steel.mass_density=7.85
srm361_steel.add_mixture('Al',	0.021		, mode='mass')
srm361_steel.add_mixture('Nd',	0.00075		, mode='mass')
srm361_steel.add_mixture('Sb',	0.0042		, mode='mass')
srm361_steel.add_mixture('Ni',	2.00		, mode='mass')
srm361_steel.add_mixture('As',	0.017		, mode='mass')
srm361_steel.add_mixture('Nb',	0.022		, mode='mass')
srm361_steel.add_mixture('Ca',	0.00010		, mode='mass')
srm361_steel.add_mixture('P ',	0.014		, mode='mass')
srm361_steel.add_mixture('C ',	0.383		, mode='mass')
srm361_steel.add_mixture('Si',	0.222		, mode='mass')
srm361_steel.add_mixture('Ce',	0.0040		, mode='mass')
srm361_steel.add_mixture('Ag',	0.0004		, mode='mass')
srm361_steel.add_mixture('Cr',	0.694		, mode='mass')
srm361_steel.add_mixture('S ',	0.0143		, mode='mass')
srm361_steel.add_mixture('Co',	0.032		, mode='mass')
srm361_steel.add_mixture('Ta',	0.020		, mode='mass')
srm361_steel.add_mixture('Cu',	0.042		, mode='mass')
srm361_steel.add_mixture('Sn',	0.010		, mode='mass')
srm361_steel.add_mixture('Pb',	0.000025	, mode='mass')
srm361_steel.add_mixture('Ti',	0.020		, mode='mass')
srm361_steel.add_mixture('Mg',	0.00026		, mode='mass')
srm361_steel.add_mixture('W ',	0.017		, mode='mass')
srm361_steel.add_mixture('Mn',	0.66		, mode='mass')
srm361_steel.add_mixture('V ',	0.011		, mode='mass')
srm361_steel.add_mixture('Mo',	0.19		, mode='mass')
srm361_steel.add_mixture('Zr',	0.009		, mode='mass')
srm361_steel.add_mixture('B ',	4.78e-6		, mode='mass')
srm361_steel.add_mixture('Bi',	0.0004		, mode='mass')
srm361_steel.add_mixture('O ',	0.0009 		, mode='mass')
srm361_steel.add_mixture('Au',	0.00005		, mode='mass')
srm361_steel.add_mixture('Pr',	0.0003		, mode='mass')
srm361_steel.add_mixture('Hf',	0.0002		, mode='mass')
srm361_steel.add_mixture('Se',	0.004		, mode='mass')
srm361_steel.add_mixture('H ',	0.0005		, mode='mass')
srm361_steel.add_mixture('Sr',	0.0005		, mode='mass')
srm361_steel.add_mixture('Te',	0.0006		, mode='mass')
srm361_steel.add_mixture('La',	0.001		, mode='mass')
srm361_steel.add_mixture('Zn',	0.0001		, mode='mass')
srm361_steel.add_mixture('N ',	0.0037		, mode='mass')
srm361_steel.add_mixture('Fe',	95.57971022	, mode='mass')
srm361_steel.finalize()


#
# SRM 2165 - Low Alloy Steel
#
srm2165_steel = calculate_materials.mixture('SRM 2165 - low alloy steel')
srm2165_steel.mass_density=7.85
srm2165_steel.add_mixture('Sb' ,	0.0010,		mode='mass')
srm2165_steel.add_mixture('As' ,	0.0010,		mode='mass')
srm2165_steel.add_mixture('Cr' ,	0.050, 		mode='mass')
srm2165_steel.add_mixture('Co' ,	0.0012,		mode='mass')
srm2165_steel.add_mixture('Cu' ,	0.0013,		mode='mass')
srm2165_steel.add_mixture('Pb' ,	0.0003,		mode='mass')
srm2165_steel.add_mixture('Mn' ,	0.144, 		mode='mass')
srm2165_steel.add_mixture('Mo' ,	0.0055,		mode='mass')
srm2165_steel.add_mixture('Ni' ,	0.155, 		mode='mass')
srm2165_steel.add_mixture('Nb' ,	0.0004,		mode='mass')
srm2165_steel.add_mixture('P ' ,	0.0052,		mode='mass')
srm2165_steel.add_mixture('Ag' ,	0.0002,		mode='mass')
srm2165_steel.add_mixture('S ' ,	0.0036,		mode='mass')
srm2165_steel.add_mixture('Sn' ,	0.002, 		mode='mass')
srm2165_steel.add_mixture('Ti' ,	0.0051,		mode='mass')
srm2165_steel.add_mixture('V ' ,	0.0040,		mode='mass')
srm2165_steel.add_mixture('Al' ,	6.0e-5,		mode='mass')
srm2165_steel.add_mixture('Bi' ,	1.0e-6,		mode='mass')
srm2165_steel.add_mixture('Mg' ,	1.0e-6,		mode='mass')
srm2165_steel.add_mixture('Se' ,	3.5e-5,		mode='mass')
srm2165_steel.add_mixture('Si' ,	4.0e-5,		mode='mass')
srm2165_steel.add_mixture('Ta' ,	4.0e-5,		mode='mass')
srm2165_steel.add_mixture('Te' ,	3.0e-5,		mode='mass')
srm2165_steel.add_mixture('Fe' ,	99.619993, 	mode='mass')
srm2165_steel.finalize()


