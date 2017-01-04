# From
# https://www.ncsu.edu/chemistry/msf/pdf/IsotopicMass_NaturalAbundance.pdf
#
# hydrogen
h=calculate_materials.mixture('H')
h.atom_fractions[1001]=99.9885
h.atom_fractions[1002]= 0.0115
h.mass_density=0.00008988
h.finalize()

# helium
he=calculate_materials.mixture('He')
he.atom_fractions[2003]=0.00000137
he.atom_fractions[2004]=0.99999863
he.mass_density=0.00018
he.finalize()

# lithium
li=calculate_materials.mixture('Li')
li.atom_fractions[3006]=7.59
li.atom_fractions[3007]=92.41
li.mass_density=0.53
li.finalize()

# beryllium
be=calculate_materials.mixture('Be')
be.atom_fractions[4009]=1.0
be.mass_density=1.85
be.finalize()

# boron
b=calculate_materials.mixture('B')
b.atom_fractions[5010]=19.9
b.atom_fractions[5011]=80.1
b.mass_density=2.34
b.finalize()

# carbon
c=calculate_materials.mixture('C')
c.atom_fractions[6012]=98.93
c.atom_fractions[6013]=1.07
c.mass_density=2.26
c.finalize()

# nitrogen
n=calculate_materials.mixture('N')
n.atom_fractions[7014]=99.632
n.atom_fractions[7015]=0.368
n.mass_density=0.00125
n.finalize()

# oxygen
o=calculate_materials.mixture('O')
o.atom_fractions[8016]=99.757
o.atom_fractions[8017]=0.038
o.atom_fractions[8018]=0.205
o.mass_density=0.00143
o.finalize()

# fluorine
f=calculate_materials.mixture('F')
f.atom_fractions[9019]=1.0
f.mass_density=0.00170
f.finalize()

# neon
ne=calculate_materials.mixture('Ne')
ne.atom_fractions[10020]=90.48
ne.atom_fractions[10021]=0.27
ne.atom_fractions[10022]=9.25
ne.mass_density=0.0009
ne.finalize()

# sodium
na=calculate_materials.mixture('Na')
na.atom_fractions(23,22.989770,1.0)
na.finalize()

# magnesium
mg=calculate_materials.mixture('Mg')
mg.atom_fractions(24,23.985042,78.99)
mg.atom_fractions(25,24.985837,10.00)
mg.atom_fractions(26,25.982593,11.01)
mg.finalize()

# aluminum
al=calculate_materials.mixture('Al')
al.atom_fractions(27,26.981538,1.0)
al.finalize()

# silicon
si=calculate_materials.mixture('Si')
si.atom_fractions(28,27.976927,92.2297)
si.atom_fractions(29,28.976495,4.6832 )
si.atom_fractions(30,29.973770,3.0872 )
si.finalize()

# phosphorous
p=calculate_materials.mixture('P')
p.atom_fractions(31,30.973762,1.0)
p.finalize()

# sulphur
s=calculate_materials.mixture('S')
s.atom_fractions(32,31.972071,94.93)
s.atom_fractions(33,32.971458,0.76)
s.atom_fractions(34,33.967867,4.29)
s.atom_fractions(36,35.967081,0.02)
s.finalize()

# chlorine
cl=calculate_materials.mixture('Cl')
cl.atom_fractions(35,34.968853,75.78)
cl.atom_fractions(37,36.965903,24.22)
cl.finalize()

# argon
ar=calculate_materials.mixture('Ar')
ar.atom_fractions(36,35.967546 ,0.3365 )
ar.atom_fractions(38,37.962732 ,0.0632 )
ar.atom_fractions(40,39.962383 ,99.6003 )
ar.finalize()

# potassium
k=calculate_materials.mixture('K')
k.atom_fractions(39,38.963707 ,93.2581 )
k.atom_fractions(40,39.963999 ,0.0117 )
k.atom_fractions(41,40.961826 ,6.7302 )
k.finalize()

# calcium
ca=calculate_materials.mixture('Ca')
ca.atom_fractions(40,39.962591 ,96.941 )
ca.atom_fractions(42,41.958618 ,0.647 )
ca.atom_fractions(43,42.958767 ,0.135 )
ca.atom_fractions(44,43.955481 ,2.086 )
ca.atom_fractions(46,45.953693 ,0.004 )
ca.atom_fractions(48,47.952534 ,0.187 )
ca.finalize()

# scandium
sc=calculate_materials.mixture('Sc')
sc.atom_fractions(45,44.955910 ,100. )
sc.finalize()

# titanium
ti=calculate_materials.mixture('Ti')
ti.atom_fractions(46,45.952629 ,8.25 )
ti.atom_fractions(47,46.951764 ,7.44 )
ti.atom_fractions(48,47.947947 ,73.72 )
ti.atom_fractions(49,48.947871 ,5.41 )
ti.atom_fractions(50,49.944792 ,5.18 )
ti.finalize()

# vanadium
v=calculate_materials.mixture('V')
v.atom_fractions(50,49.947163 ,0.250 )
v.atom_fractions(51,50.943964 ,99.750 )
v.finalize()

# chromium
cr=calculate_materials.mixture('Cr')
cr.atom_fractions(50,49.946050 ,4.345 )
cr.atom_fractions(52,51.940512 ,83.789 )
cr.atom_fractions(53,52.940654 ,9.501 )
cr.atom_fractions(54,53.938885 ,2.365 )
cr.finalize()

# manganese
mn=calculate_materials.mixture('Mn')
mn.atom_fractions(55,54.938050 ,100.0)
mn.finalize()

# iron
fe=calculate_materials.mixture('Fe')
fe.atom_fractions(54,53.939615 ,5.845 )
fe.atom_fractions(56,55.934942 ,91.754 )
fe.atom_fractions(57,56.935399 ,2.119 )
fe.atom_fractions(58,57.933280 ,0.282 )
fe.finalize()

# cobalt
co=calculate_materials.mixture('Co')
co.atom_fractions(59,58.933200 ,100.0)
co.finalize()

# nickel
ni=calculate_materials.mixture('Ni')
ni.atom_fractions(58,57.935348 ,68.0769 )
ni.atom_fractions(60,59.930791 ,26.2231 )
ni.atom_fractions(61,60.931060 ,1.1399 )
ni.atom_fractions(62,61.928349 ,3.6345 )
ni.atom_fractions(64,63.927970 ,0.9256 )
ni.finalize()

# copper
cu=calculate_materials.mixture('Cu')
cu.atom_fractions(63,62.929601 ,69.17 )
cu.atom_fractions(65,64.927794 ,30.83 )
cu.finalize()

# zinc
zinc=calculate_materials.mixture('Zn')
zinc.atom_fractions(64,63.929147 ,48.63 )
zinc.atom_fractions(66,65.926037 ,27.90 )
zinc.atom_fractions(67,66.927131 ,4.10 )
zinc.atom_fractions(68,67.924848 ,18.75 )
zinc.atom_fractions(70,69.925325 ,0.62 )
zinc.finalize()

# gallium
ga=calculate_materials.mixture('Ga')
ga.atom_fractions(69,68.925581 ,60.108 )
ga.atom_fractions(71,70.924705 ,39.892 )
ga.finalize()

# germanium
ge=calculate_materials.mixture('Ge')
ge.atom_fractions(70,69.924250 ,20.84 )
ge.atom_fractions(72,71.922076 ,27.54 )
ge.atom_fractions(73,72.923459 ,7.73 )
ge.atom_fractions(74,73.921178 ,36.28 )
ge.atom_fractions(76,75.921403 ,7.61 )
ge.finalize()

# arsenic
as_e=calculate_materials.mixture('As')
as_e.atom_fractions(75,74.921596 ,100.0)
as_e.finalize()

# selenium
se=calculate_materials.mixture('Se')
se.atom_fractions(74,73.922477 ,0.89 )
se.atom_fractions(76,75.919214 ,9.37 )
se.atom_fractions(77,76.919915 ,7.63 )
se.atom_fractions(78,77.917310 ,23.77 )
se.atom_fractions(80,79.916522 ,49.61 )
se.atom_fractions(82,81.916700 ,8.73 )
se.finalize()

# bromine
br=calculate_materials.mixture('Br')
br.atom_fractions(79,78.918338,50.69)
br.atom_fractions(81,80.916291,49.31)
br.finalize()

# krypton
kr=calculate_materials.mixture('Kr')
kr.atom_fractions(78,77.920386,0.35)
kr.atom_fractions(80,79.916378,2.28)
kr.atom_fractions(82,81.913485,11.58)
kr.atom_fractions(83,82.914136,11.49)
kr.atom_fractions(84,83.911507,57.00)
kr.atom_fractions(86,85.910610,17.30)
kr.finalize()

# rubidium
rb=calculate_materials.mixture('Rb')
rb.atom_fractions(85,84.911789,72.17)
rb.atom_fractions(87,86.909183,27.83)
rb.finalize()

# strontium
sr=calculate_materials.mixture('Sr')
sr.atom_fractions(84,83.913425,0.56)
sr.atom_fractions(86,85.909262,9.86)
sr.atom_fractions(87,86.908879,7.00)
sr.atom_fractions(88,87.905614,82.58)
sr.finalize()

# yttrium
y=calculate_materials.mixture('Y')
y.atom_fractions(89,88.905848,100.0)
y.finalize()

# zirconium
zr=calculate_materials.mixture('Zr')
zr.atom_fractions(90,89.904704,51.45)
zr.atom_fractions(91,90.905645,11.22)
zr.atom_fractions(92,91.905040,17.15)
zr.atom_fractions(94,93.906316,17.38)
zr.atom_fractions(96,95.908276,2.80)
zr.finalize()

# niobium
nb=calculate_materials.mixture('Nb')
nb.atom_fractions(93,92.906378,100.0)
nb.finalize()

# molybdenum
mo=calculate_materials.mixture('Mo')
mo.atom_fractions(92,91.906810,14.84)
mo.atom_fractions(94,93.905088,9.25)
mo.atom_fractions(95,94.905841,15.92)
mo.atom_fractions(96,95.904679,16.68)
mo.atom_fractions(97,96.906021,9.55)
mo.atom_fractions(98,97.905408,24.13)
mo.atom_fractions(100,99.907477,9.63)
mo.finalize()

# technetium
tc=calculate_materials.mixture('Tc')
tc.atom_fractions(98,97.907216,100.0)
tc.finalize()

# Ruthenium
ru=calculate_materials.mixture('Ru')
ru.atom_fractions(96,95.907598,5.54)
ru.atom_fractions(98,97.905287,1.87)
ru.atom_fractions(99,98.905939,12.76)
ru.atom_fractions(100,99.904220,12.60)
ru.atom_fractions(101,100.905582,17.06)
ru.atom_fractions(102,101.904350,31.55)
ru.atom_fractions(104,103.905430,18.62)
ru.finalize()

# Rhodium
rh=calculate_materials.mixture('Rh')
rh.atom_fractions(103,102.905504,100.0)
rh.finalize()

# Palladium
pd=calculate_materials.mixture('Pd')
pd.atom_fractions(102,101.905608,1.02)
pd.atom_fractions(104,103.904035,11.14)
pd.atom_fractions(105,104.905084,22.33)
pd.atom_fractions(106,105.903483,27.33)
pd.atom_fractions(108,107.903894,26.46)
pd.atom_fractions(110,109.905152,11.72)
pd.finalize()

# Silver
ag=calculate_materials.mixture('Ag')
ag.atom_fractions(107,106.905093,51.839)
ag.atom_fractions(109,108.904756,48.161)
ag.finalize()

# Cadmium
cd=calculate_materials.mixture('Cd')
cd.atom_fractions(106,105.906458,1.25)
cd.atom_fractions(108,107.904183,0.89)
cd.atom_fractions(110,109.903006,12.49)
cd.atom_fractions(111,110.904182,12.80)
cd.atom_fractions(112,111.902757,24.13)
cd.atom_fractions(113,112.904401,12.22)
cd.atom_fractions(114,113.903358,28.73)
cd.atom_fractions(116,115.904755,7.49)
cd.finalize()

# Indium
in_e=calculate_materials.mixture('In')
in_e.atom_fractions(113,112.904061,4.29)
in_e.atom_fractions(115,114.903878,95.71)
in_e.finalize()

# Tin
sn=calculate_materials.mixture('Sn')
sn.atom_fractions(112,111.904821,0.97)
sn.atom_fractions(114,113.902782,0.66)
sn.atom_fractions(115,114.903346,0.34)
sn.atom_fractions(116,115.901744,14.54)
sn.atom_fractions(117,116.902954,7.68)
sn.atom_fractions(118,117.901606,24.22)
sn.atom_fractions(119,118.903309,8.59)
sn.atom_fractions(120,119.902197,32.58)
sn.atom_fractions(122,121.903440,4.63)
sn.atom_fractions(124,123.905275,5.79)
sn.finalize()

# Antimony
sb=calculate_materials.mixture('Sb')
sb.atom_fractions(121,120.903818,57.21)
sb.atom_fractions(123,122.904216,42.79)
sb.finalize()

# Tellurium
te=calculate_materials.mixture('Te')
te.atom_fractions(120,119.904020,0.09)
te.atom_fractions(122,121.903047,2.55)
te.atom_fractions(123,122.904273,0.89)
te.atom_fractions(124,123.902819,4.74)
te.atom_fractions(125,124.904425,7.07)
te.atom_fractions(126,125.903306,18.84)
te.atom_fractions(128,127.904461,31.74)
te.atom_fractions(130,129.906223,34.08)
te.finalize()

# Iodine
i=calculate_materials.mixture('I')
i.atom_fractions(127,126.904468,100.0)
i.finalize()

# Xenon
xe=calculate_materials.mixture('Xe')
xe.atom_fractions(124,123.905896,0.09)
xe.atom_fractions(126,125.904269,0.09)
xe.atom_fractions(128,127.903530,1.92)
xe.atom_fractions(129,128.904779,26.44)
xe.atom_fractions(130,129.903508,4.08)
xe.atom_fractions(131,130.905082,21.18)
xe.atom_fractions(132,131.904154,26.89)
xe.atom_fractions(134,133.905395,10.44)
xe.atom_fractions(136,135.907220,8.87)
xe.finalize()

# Cesium
cs=calculate_materials.mixture('Cs')
cs.atom_fractions(133,132.905447,100.)
cs.finalize()

# Barium
ba=calculate_materials.mixture('Ba')
ba.atom_fractions(130,129.906310,0.106)
ba.atom_fractions(132,131.905056,0.101)
ba.atom_fractions(134,133.904503,2.417)
ba.atom_fractions(135,134.905683,6.592)
ba.atom_fractions(136,135.904570,7.854)
ba.atom_fractions(137,136.905821,11.232)
ba.atom_fractions(138,137.905241,71.698)
ba.finalize()

# Lanthanum
la=calculate_materials.mixture('La')
la.atom_fractions(138,137.907107,0.090)
la.atom_fractions(139,138.906348,99.910)
la.finalize()

# Cerium
ce=calculate_materials.mixture('Ce')
ce.atom_fractions(136,135.907144,0.185)
ce.atom_fractions(138,137.905986,0.251)
ce.atom_fractions(140,139.905434,88.450)
ce.atom_fractions(142,141.909240,11.114)
ce.finalize()

# Praseodymium
pr=calculate_materials.mixture('Pr')
pr.atom_fractions(141,140.907648,100.)
pr.finalize()

# Neodymium
nd=calculate_materials.mixture('Nd')
nd.atom_fractions(142,141.907719,27.2)
nd.atom_fractions(143,142.909810,12.2)
nd.atom_fractions(144,143.910083,23.8)
nd.atom_fractions(145,144.912569,8.3)
nd.atom_fractions(146,145.913112,17.2)
nd.atom_fractions(148,147.916889,5.7)
nd.atom_fractions(150,149.920887,5.6)
nd.finalize()

# Promethium
pm=calculate_materials.mixture('Pm')
pm.atom_fractions(145,144.912744,100.)
pm.finalize()

# Samarium
sm=calculate_materials.mixture('Sm')
sm.atom_fractions(144,143.911995,3.07)
sm.atom_fractions(147,146.914893,14.99)
sm.atom_fractions(148,147.914818,11.24)
sm.atom_fractions(149,148.917180,13.82)
sm.atom_fractions(150,149.917271,7.38)
sm.atom_fractions(152,151.919728,26.75)
sm.atom_fractions(154,153.922205,22.75)
sm.finalize()

# Europium
eu=calculate_materials.mixture('Eu')
eu.atom_fractions(151,150.919846,47.81)
eu.atom_fractions(153,152.921226,52.19)
eu.finalize()

# Gadolinium
gd=calculate_materials.mixture('Gd')
gd.atom_fractions(152,151.919788,0.20)
gd.atom_fractions(154,153.920862,2.18)
gd.atom_fractions(155,154.922619,14.80)
gd.atom_fractions(156,155.922120,20.47)
gd.atom_fractions(157,156.923957,15.65)
gd.atom_fractions(158,157.924101,24.84)
gd.atom_fractions(160,159.927051,21.86)
gd.finalize()

# Terbium
tb=calculate_materials.mixture('Tb')
tb.atom_fractions(159,158.925343,100.)
tb.finalize()

# Dysprosium
dy=calculate_materials.mixture('Dy')
dy.atom_fractions(156,155.924278,0.06)
dy.atom_fractions(158,157.924405,0.10)
dy.atom_fractions(160,159.925194,2.34)
dy.atom_fractions(161,160.926930,18.91)
dy.atom_fractions(162,161.926795,25.51)
dy.atom_fractions(163,162.928728,24.90)
dy.atom_fractions(164,163.929171,28.18)
dy.finalize()

# Holmium
ho=calculate_materials.mixture('Ho')
ho.atom_fractions(165,164.930319,100.)
ho.finalize()

# Erbium
er=calculate_materials.mixture('Er')
er.atom_fractions(162,161.928775,0.14)
er.atom_fractions(164,163.929197,1.61)
er.atom_fractions(166,165.930290,33.61)
er.atom_fractions(167,166.932045,22.93)
er.atom_fractions(168,167.932368,26.78)
er.atom_fractions(170,169.935460,14.93)
er.finalize()

# Thulium
tm=calculate_materials.mixture('Tm')
tm.atom_fractions(169,168.934211,100.)
tm.finalize()

# Ytterbium
yb=calculate_materials.mixture('Yb')
yb.atom_fractions(168,167.933894,0.13)
yb.atom_fractions(170,169.934759,3.04)
yb.atom_fractions(171,170.936322,14.28)
yb.atom_fractions(172,171.936378,21.83)
yb.atom_fractions(173,172.938207,16.13)
yb.atom_fractions(174,173.938858,31.83)
yb.atom_fractions(176,175.942568,12.76)
yb.finalize()

# Lutetium
lu=calculate_materials.mixture('Lu')
lu.atom_fractions(175,174.940768,97.41)
lu.atom_fractions(176,175.942682,2.59)
lu.finalize()

# Hafnium
hf=calculate_materials.mixture('Hf')
hf.atom_fractions(174,173.940040,0.16)
hf.atom_fractions(176,175.941402,5.26)
hf.atom_fractions(177,176.943220,18.60)
hf.atom_fractions(178,177.943698,27.28)
hf.atom_fractions(179,178.945815,13.62)
hf.atom_fractions(180,179.946549,35.08)
hf.finalize()

# Tantalum
ta=calculate_materials.mixture('Ta')
ta.atom_fractions(180,179.947466,0.012)
ta.atom_fractions(181,180.947996,99.988)
ta.finalize()

# Tungsten
w=calculate_materials.mixture('W')
w.atom_fractions(180,179.946706,0.12)
w.atom_fractions(182,181.948206,26.50)
w.atom_fractions(183,182.950224,14.31)
w.atom_fractions(184,183.950933,30.64)
w.atom_fractions(186,185.954362,28.43)
w.finalize()

# Rhenium
re=calculate_materials.mixture('Re')
re.atom_fractions(185,184.952956,37.40)
re.atom_fractions(187,186.955751,62.60)
re.finalize()

# Osmium
os=calculate_materials.mixture('Os')
os.atom_fractions(184,183.952491,0.02)
os.atom_fractions(186,185.953838,1.59)
os.atom_fractions(187,186.955748,1.96)
os.atom_fractions(188,187.955836,13.24)
os.atom_fractions(189,188.958145,16.15)
os.atom_fractions(190,189.958445,26.26)
os.atom_fractions(192,191.961479,40.78)
os.finalize()

# Iridium
ir=calculate_materials.mixture('Ir')
ir.atom_fractions(191,190.960591,37.3)
ir.atom_fractions(193,192.962924,62.7)
ir.finalize()

# Platinum
pt=calculate_materials.mixture('Pt')
pt.atom_fractions(190,189.959930,0.014)
pt.atom_fractions(192,191.961035,0.782)
pt.atom_fractions(194,193.962664,32.967)
pt.atom_fractions(195,194.964774,33.832)
pt.atom_fractions(196,195.964935,25.242)
pt.atom_fractions(198,197.967876,7.163)
pt.finalize()

# Gold
au=calculate_materials.mixture('Au')
au.atom_fractions(197,196.966552,100.)
au.finalize()

# Mercury
hg=calculate_materials.mixture('Hg')
hg.atom_fractions(196,195.965815,0.15)
hg.atom_fractions(198,197.966752,9.97)
hg.atom_fractions(199,198.968262,16.87)
hg.atom_fractions(200,199.968309,23.10)
hg.atom_fractions(201,200.970285,13.18)
hg.atom_fractions(202,201.970626,29.86)
hg.atom_fractions(204,203.973476,6.87)
hg.finalize()

# Thallium
tl=calculate_materials.mixture('Tl')
tl.atom_fractions(203,202.972329,29.524)
tl.atom_fractions(205,204.974412,70.476)
tl.finalize()

# Lead
pb=calculate_materials.mixture('Pb')
pb.atom_fractions(204,203.973029,1.4)
pb.atom_fractions(206,205.974449,24.1)
pb.atom_fractions(207,206.975881,22.1)
pb.atom_fractions(208,207.976636,52.4)
pb.finalize()

# Bismuth
bi=calculate_materials.mixture('Bi')
bi.atom_fractions(209,208.980383,100.)
bi.finalize()

# Thorium
th=calculate_materials.mixture('Th')
th.atom_fractions(232,232.038050,100.)
th.finalize()

# Protactinium
pa=calculate_materials.mixture('Pa')
pa.atom_fractions(232,231.035879,100.)
pa.finalize()

# Uranium
u=calculate_materials.mixture('U')
u.atom_fractions(234,234.040946,0.0055)
u.atom_fractions(235,235.043923,0.7200)
u.atom_fractions(238,238.050783,99.2745)
u.finalize()