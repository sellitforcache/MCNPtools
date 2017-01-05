# From
# https://www.ncsu.edu/chemistry/msf/pdf/IsotopicMass_NaturalAbundance.pdf
#
# hydrogen
H=calculate_materials.mixture('H')
H.atom_fractions[1001]=99.9885
H.atom_fractions[1002]= 0.0115
H.mass_density=0.00008988
H.finalize()

# helium
He=calculate_materials.mixture('He')
He.atom_fractions[2003]=0.00000137
He.atom_fractions[2004]=0.99999863
He.mass_density=0.00018
He.finalize()

# lithium
Li=calculate_materials.mixture('Li')
Li.atom_fractions[3006]=7.59
Li.atom_fractions[3007]=92.41
Li.mass_density=0.53
Li.finalize()

# beryllium
Be=calculate_materials.mixture('Be')
Be.atom_fractions[4009]=1.0
Be.mass_density=1.85
Be.finalize()

# boron
B=calculate_materials.mixture('B')
B.atom_fractions[5010]=19.9
B.atom_fractions[5011]=80.1
B.mass_density=2.34
B.finalize()

# carbon
C=calculate_materials.mixture('C')
C.atom_fractions[6012]=98.93
C.atom_fractions[6013]=1.07
C.mass_density=2.26
C.finalize()

# nitrogen
N=calculate_materials.mixture('N')
N.atom_fractions[7014]=99.632
N.atom_fractions[7015]=0.368
N.mass_density=0.00125
N.finalize()

# oxygen
O=calculate_materials.mixture('O')
O.atom_fractions[8016]=99.757
O.atom_fractions[8017]=0.038
O.atom_fractions[8018]=0.205
O.mass_density=0.00143
O.finalize()

# fluorine
F=calculate_materials.mixture('F')
F.atom_fractions[9019]=1.0
F.mass_density=0.00170
F.finalize()

# neon
Ne=calculate_materials.mixture('Ne')
Ne.atom_fractions[10020]=90.48
Ne.atom_fractions[10021]=0.27
Ne.atom_fractions[10022]=9.25
Ne.mass_density=0.0009
Ne.finalize()

# sodium
Na=calculate_materials.mixture('Na')
Na.atom_fractions[11023]=1.0
Na.mass_density=0.971
Na.finalize()

# magnesium
Mg=calculate_materials.mixture('Mg')
Mg.atom_fractions[12024]=78.99
Mg.atom_fractions[12025]=10.00
Mg.atom_fractions[12026]=11.01
Mg.mass_density=1.738
Mg.finalize()

# aluminum
Al=calculate_materials.mixture('Al')
Al.atom_fractions[13027]=1.0
Al.mass_density=2.702
Al.finalize()

# silicon
Si=calculate_materials.mixture('Si')
Si.atom_fractions[14028]=92.2297
Si.atom_fractions[14029]=4.6832 
Si.atom_fractions[14030]=3.0872 
Si.mass_density=2.33
Si.finalize()

# phosphorous
P=calculate_materials.mixture('P')
P.atom_fractions[15031]=1.0
P.mass_density=1.82
P.finalize()

# sulphur
S=calculate_materials.mixture('S')
S.atom_fractions[16032]=94.93
S.atom_fractions[16033]=0.76
S.atom_fractions[16034]=4.29
S.atom_fractions[16036]=0.02
S.mass_density=2.07
S.finalize()

# chlorine
Cl=calculate_materials.mixture('Cl')
Cl.atom_fractions[17035]=75.78
Cl.atom_fractions[17037]=24.22
Cl.mass_density=0.003214
Cl.finalize()

# argon
Ar=calculate_materials.mixture('Ar')
Ar.atom_fractions[18036]=0.3365 
Ar.atom_fractions[18038]=0.0632 
Ar.atom_fractions[18040]=99.6003 
Ar.mass_density=0.0017824
Ar.finalize()

# potassium
K=calculate_materials.mixture('K')
K.atom_fractions[19039]=93.2581 
K.atom_fractions[19040]=0.0117  
K.atom_fractions[19041]=6.7302  
K.mass_density=0.862
K.finalize()

# calcium
Ca=calculate_materials.mixture('Ca')
Ca.atom_fractions[20040]=96.941
Ca.atom_fractions[20042]=0.647 
Ca.atom_fractions[20043]=0.135 
Ca.atom_fractions[20044]=2.086 
Ca.atom_fractions[20046]=0.004 
Ca.atom_fractions[20048]=0.187 
Ca.mass_density=1.55
Ca.finalize()

# scandium
Sc=calculate_materials.mixture('Sc')
Sc.atom_fractions[21045]=1.0
Sc.mass_density=2.99
Sc.finalize()

# titanium
Ti=calculate_materials.mixture('Ti')
Ti.atom_fractions[22046]=8.25 
Ti.atom_fractions[22047]=7.44 
Ti.atom_fractions[22048]=73.72
Ti.atom_fractions[22049]=5.41 
Ti.atom_fractions[22050]=5.18 
Ti.mass_density=4.54
Ti.finalize()

# vanadium
V=calculate_materials.mixture('V')
V.atom_fractions[23050]=0.250 
V.atom_fractions[23051]=99.750
V.mass_density=6.11
V.finalize()

# chromium
Cr=calculate_materials.mixture('Cr')
Cr.atom_fractions[24050]=4.345 
Cr.atom_fractions[24052]=83.789
Cr.atom_fractions[24053]=9.501 
Cr.atom_fractions[24054]=2.365 
Cr.mass_density=7.19
Cr.finalize()

# manganese
Mn=calculate_materials.mixture('Mn')
Mn.atom_fractions[25055]=1.0
Mn.mass_density=7.43
Mn.finalize()

# iron
Fe=calculate_materials.mixture('Fe')
Fe.atom_fractions[26054]=5.845 
Fe.atom_fractions[26056]=91.754
Fe.atom_fractions[26057]=2.119 
Fe.atom_fractions[26058]=0.282 
Fe.mass_density=7.874
Fe.finalize()

# cobalt
Co=calculate_materials.mixture('Co')
Co.atom_fractions[27059]=1.0
Co.mass_density=8.9
Co.finalize()

# nickel
Ni=calculate_materials.mixture('Ni')
Ni.atom_fractions[28058]=68.0769
Ni.atom_fractions[28060]=26.2231
Ni.atom_fractions[28061]=1.1399 
Ni.atom_fractions[28062]=3.6345 
Ni.atom_fractions[28064]=0.9256 
Ni.mass_density=8.9
Ni.finalize()

# copper
Cu=calculate_materials.mixture('Cu')
Cu.atom_fractions[29063]=69.17
Cu.atom_fractions[29065]=30.83
Cu.mass_density=8.96
Cu.finalize()

# zinc
Zn=calculate_materials.mixture('Zn')
Zn.atom_fractions[30064]=48.63
Zn.atom_fractions[30066]=27.90
Zn.atom_fractions[30067]=4.10 
Zn.atom_fractions[30068]=18.75
Zn.atom_fractions[30070]=0.62 
Zn.mass_density=7.13
Zn.finalize()

# gallium
Ga=calculate_materials.mixture('Ga')
Ga.atom_fractions[31069]=60.108
Ga.atom_fractions[31071]=39.892
Ga.mass_density=5.907
Ga.finalize()

# germanium
Ge=calculate_materials.mixture('Ge')
Ge.atom_fractions[32070]=20.84
Ge.atom_fractions[32072]=27.54
Ge.atom_fractions[32073]=7.73 
Ge.atom_fractions[32074]=36.28
Ge.atom_fractions[32076]=7.61 
Ge.mass_density=5.323
Ge.finalize()

# arsenic
As=calculate_materials.mixture('As')
As.atom_fractions[33075]=1.0
As.mass_density=5.72
As.finalize()

# selenium
Se=calculate_materials.mixture('Se')
Se.atom_fractions[34074]=0.89 
Se.atom_fractions[34076]=9.37 
Se.atom_fractions[34077]=7.63 
Se.atom_fractions[34078]=23.77
Se.atom_fractions[34080]=49.61
Se.atom_fractions[34082]=8.73 
Se.mass_density=4.79
Se.finalize()

# bromine
Br=calculate_materials.mixture('Br')
Br.atom_fractions[35079]=50.69
Br.atom_fractions[35081]=49.31
Br.mass_density=3.119
Br.finalize()

# krypton
Kr=calculate_materials.mixture('Kr')
Kr.atom_fractions[36078]=0.35
Kr.atom_fractions[36080]=2.28
Kr.atom_fractions[36082]=11.58
Kr.atom_fractions[36083]=11.49
Kr.atom_fractions[36084]=57.00
Kr.atom_fractions[36086]=17.30
Kr.mass_density=0.00375
Kr.finalize()

# rubidium
Rb=calculate_materials.mixture('Rb')
Rb.atom_fractions[37085]=72.17
Rb.atom_fractions[37087]=27.83
Rb.mass_density=1.63
Rb.finalize()

# strontium
Sr=calculate_materials.mixture('Sr')
Sr.atom_fractions[38084]=0.56
Sr.atom_fractions[38086]=9.86
Sr.atom_fractions[38087]=7.00
Sr.atom_fractions[38088]=82.58
Sr.mass_density=2.54
Sr.finalize()

# yttrium
Y=calculate_materials.mixture('Y')
Y.atom_fractions[39089]=1.0
Y.mass_density=4.47
Y.finalize()

# zirconium
Zr=calculate_materials.mixture('Zr')
Zr.atom_fractions[40090]=51.45
Zr.atom_fractions[40091]=11.22
Zr.atom_fractions[40092]=17.15
Zr.atom_fractions[40094]=17.38
Zr.atom_fractions[40096]=2.80
Zr.mass_density=6.51
Zr.finalize()

# niobium
Nb=calculate_materials.mixture('Nb')
Nb.atom_fractions[41093]=1.0
Nb.mass_density=8.57
Nb.finalize()

# molybdenum
Mo=calculate_materials.mixture('Mo')
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
Tc=calculate_materials.mixture('Tc')
Tc.atom_fractions[43098]=1.0
Tc.mass_density=11.5
Tc.finalize()

# Ruthenium
Ru=calculate_materials.mixture('Ru')
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
Rh=calculate_materials.mixture('Rh')
Rh.atom_fractions[45103]=1.0
Rh.mass_density=12.41
Rh.finalize()

# Palladium
Pd=calculate_materials.mixture('Pd')
Pd.atom_fractions[46102]=1.02
Pd.atom_fractions[46104]=11.14
Pd.atom_fractions[46105]=22.33
Pd.atom_fractions[46106]=27.33
Pd.atom_fractions[46108]=26.46
Pd.atom_fractions[46110]=11.72
Pd.mass_density=12.02
Pd.finalize()

# Silver
Ag=calculate_materials.mixture('Ag')
Ag.atom_fractions[47107]=51.839
Ag.atom_fractions[47109]=48.161
Ag.mass_density=10.5
Ag.finalize()

# Cadmium
Cd=calculate_materials.mixture('Cd')
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
In=calculate_materials.mixture('In')
In.atom_fractions[49113]=4.29
In.atom_fractions[49115]=95.71
In.mass_density=7.31
In.finalize()

# Tin
Sn=calculate_materials.mixture('Sn')
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
Sb=calculate_materials.mixture('Sb')
Sb.atom_fractions[51121]=57.21
Sb.atom_fractions[51123]=42.79
Sb.mass_density=6.684
Sb.finalize()

# Tellurium
Te=calculate_materials.mixture('Te')
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
I=calculate_materials.mixture('I')
I.atom_fractions[53127]=1.0
I.mass_density=4.93
I.finalize()

# Xenon
Xe=calculate_materials.mixture('Xe')
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
Cs=calculate_materials.mixture('Cs')
Cs.atom_fractions[55133]=1.0
Cs.mass_density=1.873
Cs.finalize()

# Barium
Ba=calculate_materials.mixture('Ba')
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
La=calculate_materials.mixture('La')
La.atom_fractions[57138]=0.090
La.atom_fractions[57139]=99.910
La.mass_density=6.15
La.finalize()

# Cerium
Ce=calculate_materials.mixture('Ce')
Ce.atom_fractions[58136]=0.185
Ce.atom_fractions[58138]=0.251
Ce.atom_fractions[58140]=88.450
Ce.atom_fractions[58142]=11.114
Ce.mass_density=6.77
Ce.finalize()

# Praseodymium
Pr=calculate_materials.mixture('Pr')
Pr.atom_fractions[59141]=1.0
Pr.mass_density=6.77
Pr.finalize()

# Neodymium
Nd=calculate_materials.mixture('Nd')
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
Pm=calculate_materials.mixture('Pm')
Pm.atom_fractions[61145]=1.0
Pm.mass_density=7.3
Pm.finalize()

# Samarium
Sm=calculate_materials.mixture('Sm')
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
Eu=calculate_materials.mixture('Eu')
Eu.atom_fractions[63151]=47.81
Eu.atom_fractions[63153]=52.19
Eu.mass_density=5.24
Eu.finalize()

# Gadolinium
Gd=calculate_materials.mixture('Gd')
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
Tb=calculate_materials.mixture('Tb')
Tb.atom_fractions[65159]=1.0
Tb.mass_density=8.23
Tb.finalize()

# Dysprosium
Dy=calculate_materials.mixture('Dy')
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
Ho=calculate_materials.mixture('Ho')
Ho.atom_fractions[67165]=1.0
Ho.mass_density=8.8
Ho.finalize()

# Erbium
Er=calculate_materials.mixture('Er')
Er.atom_fractions[68162]=0.14
Er.atom_fractions[68164]=1.61
Er.atom_fractions[68166]=33.61
Er.atom_fractions[68167]=22.93
Er.atom_fractions[68168]=26.78
Er.atom_fractions[68170]=14.93
Er.mass_density=9.07
Er.finalize()

# Thulium
Tm=calculate_materials.mixture('Tm')
Tm.atom_fractions[69169]=1.0
Tm.mass_density=9.32
Tm.finalize()

# Ytterbium
Yb=calculate_materials.mixture('Yb')
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
Lu=calculate_materials.mixture('Lu')
Lu.atom_fractions[71175]=97.41
Lu.atom_fractions[71176]=2.59
Lu.mass_density=9.84
Lu.finalize()

# Hafnium
Hf=calculate_materials.mixture('Hf')
Hf.atom_fractions[72174]=0.16
Hf.atom_fractions[72176]=5.26
Hf.atom_fractions[72177]=18.60
Hf.atom_fractions[72178]=27.28
Hf.atom_fractions[72179]=13.62
Hf.atom_fractions[72180]=35.08
Hf.mass_density=13.31
Hf.finalize()

# Tantalum
Ta=calculate_materials.mixture('Ta')
Ta.atom_fractions[73180]=0.012
Ta.atom_fractions[73181]=99.988
Ta.mass_density=16.65
Ta.finalize()

# Tungsten
W=calculate_materials.mixture('W')
W.atom_fractions[74180]=0.12
W.atom_fractions[74182]=26.50
W.atom_fractions[74183]=14.31
W.atom_fractions[74184]=30.64
W.atom_fractions[74186]=28.43
W.mass_density=19.35
W.finalize()

# Rhenium
Re=calculate_materials.mixture('Re')
Re.atom_fractions[75185]=37.40
Re.atom_fractions[75187]=62.60
Re.mass_density=21.04
Re.finalize()

# Osmium
Os=calculate_materials.mixture('Os')
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
Ir=calculate_materials.mixture('Ir')
Ir.atom_fractions[77191]=37.3
Ir.atom_fractions[77193]=62.7
Ir.mass_density=22.4
Ir.finalize()

# Platinum
Pt=calculate_materials.mixture('Pt')
Pt.atom_fractions[78190]=0.014
Pt.atom_fractions[78192]=0.782
Pt.atom_fractions[78194]=32.967
Pt.atom_fractions[78195]=33.832
Pt.atom_fractions[78196]=25.242
Pt.atom_fractions[78198]=7.163
Pt.mass_density=21.45
Pt.finalize()

# Gold
Au=calculate_materials.mixture('Au')
Au.atom_fractions[79197]=1.0
Au.mass_density=19.32
Au.finalize()

# Mercury
Hg=calculate_materials.mixture('Hg')
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
Tl=calculate_materials.mixture('Tl')
Tl.atom_fractions[81203]=29.524
Tl.atom_fractions[81205]=70.476
Tl.mass_density=11.85
Tl.finalize()

# Lead
Pb=calculate_materials.mixture('Pb')
Pb.atom_fractions[82204]=1.4
Pb.atom_fractions[82206]=24.1
Pb.atom_fractions[82207]=22.1
Pb.atom_fractions[82208]=52.4
Pb.mass_density=11.35
Pb.finalize()

# Bismuth
Bi=calculate_materials.mixture('Bi')
Bi.atom_fractions[83209]=1.0
Bi.mass_density=9.75
Bi.finalize()

# Thorium
Th=calculate_materials.mixture('Th')
Th.atom_fractions[90232]=1.0
Th.mass_density=11.724
Th.finalize()

# Protactinium
Pa=calculate_materials.mixture('Pa')
Pa.atom_fractions[91232]=1.0
Pa.mass_density=15.4
Pa.finalize()

# Uranium
U=calculate_materials.mixture('U')
U.atom_fractions[92234]=0.0055
U.atom_fractions[92235]=0.7200
U.atom_fractions[92238]=99.2745
U.mass_density=18.95
U.finalize()