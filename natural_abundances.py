# From
# https://www.ncsu.edu/chemistry/msf/pdf/IsotopicMass_NaturalAbundance.pdf
#

# hydrogen
h=calculate_materials.element('H')
h.add_isotope_atom(1,1.007825032239,99.9885)
h.add_isotope_atom(2,2.014101778121, 0.0115)
h.finalize()

# helium
he=calculate_materials.element('He')
he.add_isotope_atom(3,3.016029,0.00000137)
he.add_isotope_atom(4,4.002603,0.99999863)
he.finalize()

# lithium
li=calculate_materials.element('Li')
li.add_isotope_atom(6,6.015122,7.59)
li.add_isotope_atom(7,7.016004,92.41)
li.finalize()

# beryllium
bi=calculate_materials.element('Be')
bi.add_isotope_atom(9,9.012182,1.0)
bi.finalize()

# boron
b=calculate_materials.element('B')
b.add_isotope_atom(10,10.012937,19.9)
b.add_isotope_atom(11,11.009305,80.1)
b.finalize()

# carbon
c=calculate_materials.element('C')
c.add_isotope_atom(12,12.000000,98.93)
c.add_isotope_atom(13,13.003355,1.07)
c.finalize()

# nitrogen
n=calculate_materials.element('N')
n.add_isotope_atom(14,14.003074,99.632)
n.add_isotope_atom(15,15.000109,0.368)
n.finalize()

# oxygen
o=calculate_materials.element('O')
o.add_isotope_atom(16,15.994915,99.757)
o.add_isotope_atom(17,16.999132,0.038)
o.add_isotope_atom(18,17.999160,0.205)
o.finalize()

# fluorine
f=calculate_materials.element('F')
f.add_isotope_atom(19,18.998403,1.0)
f.finalize()

# neon
ne=calculate_materials.element('Ne')
ne.add_isotope_atom(20,19.992440,90.48)
ne.add_isotope_atom(21,20.993847,0.27)
ne.add_isotope_atom(22,21.991386,9.25)
ne.finalize()

# sodium
na=calculate_materials.element('Na')
na.add_isotope_atom(23,22.989770,1.0)
na.finalize()

# magnesium
mg=calculate_materials.element('Mg')
mg.add_isotope_atom(24,23.985042,78.99)
mg.add_isotope_atom(25,24.985837,10.00)
mg.add_isotope_atom(26,25.982593,11.01)
mg.finalize()

# aluminum
al=calculate_materials.element('Al')
al.add_isotope_atom(27,26.981538,1.0)
al.finalize()

# silicon
si=calculate_materials.element('Si')
si.add_isotope_atom(28,27.976927,92.2297)
si.add_isotope_atom(29,28.976495,4.6832 )
si.add_isotope_atom(30,29.973770,3.0872 )
si.finalize()

# phosphorous
p=calculate_materials.element('P')
p.add_isotope_atom(31,30.973762,1.0)
p.finalize()

# sulphur
s=calculate_materials.element('S')
s.add_isotope_atom(32,31.972071,94.93)
s.add_isotope_atom(33,32.971458,0.76)
s.add_isotope_atom(34,33.967867,4.29)
s.add_isotope_atom(36,35.967081,0.02)
s.finalize()

# chlorine
cl=calculate_materials.element('Cl')
cl.add_isotope_atom(35,34.968853,75.78)
cl.add_isotope_atom(37,36.965903,24.22)
cl.finalize()

# argon
ar=calculate_materials.element('Ar')
ar.add_isotope_atom(36,35.967546 ,0.3365 )
ar.add_isotope_atom(38,37.962732 ,0.0632 )
ar.add_isotope_atom(40,39.962383 ,99.6003 )
ar.finalize()

# potassium
k=calculate_materials.element('K')
k.add_isotope_atom(39,38.963707 ,93.2581 )
k.add_isotope_atom(40,39.963999 ,0.0117 )
k.add_isotope_atom(41,40.961826 ,6.7302 )
k.finalize()

# calcium
ca=calculate_materials.element('Ca')
ca.add_isotope_atom(40,39.962591 ,96.941 )
ca.add_isotope_atom(42,41.958618 ,0.647 )
ca.add_isotope_atom(43,42.958767 ,0.135 )
ca.add_isotope_atom(44,43.955481 ,2.086 )
ca.add_isotope_atom(46,45.953693 ,0.004 )
ca.add_isotope_atom(48,47.952534 ,0.187 )
ca.finalize()

# scandium
sc=calculate_materials.element('Sc')
sc.add_isotope_atom(45,44.955910 ,100. )
sc.finalize()

# titanium
ti=calculate_materials.element('Ti')
ti.add_isotope_atom(46,45.952629 ,8.25 )
ti.add_isotope_atom(47,46.951764 ,7.44 )
ti.add_isotope_atom(48,47.947947 ,73.72 )
ti.add_isotope_atom(49,48.947871 ,5.41 )
ti.add_isotope_atom(50,49.944792 ,5.18 )
ti.finalize()

# vanadium
v=calculate_materials.element('V')
v.add_isotope_atom(50,49.947163 ,0.250 )
v.add_isotope_atom(51,50.943964 ,99.750 )
v.finalize()

# chromium
cr=calculate_materials.element('Cr')
cr.add_isotope_atom(50,49.946050 ,4.345 )
cr.add_isotope_atom(52,51.940512 ,83.789 )
cr.add_isotope_atom(53,52.940654 ,9.501 )
cr.add_isotope_atom(54,53.938885 ,2.365 )
cr.finalize()

# manganese
mn=calculate_materials.element('Mn')
mn.add_isotope_atom(55,54.938050 ,100.0)
mn.finalize()

# iron
fe=calculate_materials.element('Fe')
fe.add_isotope_atom(54,53.939615 ,5.845 )
fe.add_isotope_atom(56,55.934942 ,91.754 )
fe.add_isotope_atom(57,56.935399 ,2.119 )
fe.add_isotope_atom(58,57.933280 ,0.282 )
fe.finalize()

# cobalt
co=calculate_materials.element('Co')
co.add_isotope_atom(59,58.933200 ,100.0)
co.finalize()

# nickel
ni=calculate_materials.element('Ni')
ni.add_isotope_atom(58,57.935348 ,68.0769 )
ni.add_isotope_atom(60,59.930791 ,26.2231 )
ni.add_isotope_atom(61,60.931060 ,1.1399 )
ni.add_isotope_atom(62,61.928349 ,3.6345 )
ni.add_isotope_atom(64,63.927970 ,0.9256 )
ni.finalize()

# copper
cu=calculate_materials.element('Cu')
cu.add_isotope_atom(63,62.929601 ,69.17 )
cu.add_isotope_atom(65,64.927794 ,30.83 )
cu.finalize()

# zinc
zinc=calculate_materials.element('Zn')
zinc.add_isotope_atom(64,63.929147 ,48.63 )
zinc.add_isotope_atom(66,65.926037 ,27.90 )
zinc.add_isotope_atom(67,66.927131 ,4.10 )
zinc.add_isotope_atom(68,67.924848 ,18.75 )
zinc.add_isotope_atom(70,69.925325 ,0.62 )
zinc.finalize()

# gallium
ga=calculate_materials.element('Ga')
ga.add_isotope_atom(69,68.925581 ,60.108 )
ga.add_isotope_atom(71,70.924705 ,39.892 )
ga.finalize()

# germanium
ge=calculate_materials.element('Ge')
ge.add_isotope_atom(70,69.924250 ,20.84 )
ge.add_isotope_atom(72,71.922076 ,27.54 )
ge.add_isotope_atom(73,72.923459 ,7.73 )
ge.add_isotope_atom(74,73.921178 ,36.28 )
ge.add_isotope_atom(76,75.921403 ,7.61 )
ge.finalize()

# arsenic
as_e=calculate_materials.element('As')
as_e.add_isotope_atom(75,74.921596 ,100.0)
as_e.finalize()

# selenium
se=calculate_materials.element('Se')
se.add_isotope_atom(74,73.922477 ,0.89 )
se.add_isotope_atom(76,75.919214 ,9.37 )
se.add_isotope_atom(77,76.919915 ,7.63 )
se.add_isotope_atom(78,77.917310 ,23.77 )
se.add_isotope_atom(80,79.916522 ,49.61 )
se.add_isotope_atom(82,81.916700 ,8.73 )
se.finalize()

# bromine
br=calculate_materials.element('Br')
br.add_isotope_atom(79,78.918338,50.69)
br.add_isotope_atom(81,80.916291,49.31)
br.finalize()

# krypton
kr=calculate_materials.element('Kr')
kr.add_isotope_atom(78,77.920386,0.35)
kr.add_isotope_atom(80,79.916378,2.28)
kr.add_isotope_atom(82,81.913485,11.58)
kr.add_isotope_atom(83,82.914136,11.49)
kr.add_isotope_atom(84,83.911507,57.00)
kr.add_isotope_atom(86,85.910610,17.30)
kr.finalize()

# rubidium
rb=calculate_materials.element('Rb')
rb.add_isotope_atom(85,84.911789,72.17)
rb.add_isotope_atom(87,86.909183,27.83)
rb.finalize()

# strontium
sr=calculate_materials.element('Sr')
sr.add_isotope_atom(84,83.913425,0.56)
sr.add_isotope_atom(86,85.909262,9.86)
sr.add_isotope_atom(87,86.908879,7.00)
sr.add_isotope_atom(88,87.905614,82.58)
sr.finalize()

# yttrium
y=calculate_materials.element('Y')
y.add_isotope_atom(89,88.905848,100.0)
y.finalize()

# zirconium
zr=calculate_materials.element('Zr')
zr.add_isotope_atom(90,89.904704,51.45)
zr.add_isotope_atom(91,90.905645,11.22)
zr.add_isotope_atom(92,91.905040,17.15)
zr.add_isotope_atom(94,93.906316,17.38)
zr.add_isotope_atom(96,95.908276,2.80)
zr.finalize()

# niobium
nb=calculate_materials.element('Nb')
nb.add_isotope_atom(93,92.906378,100.0)
nb.finalize()

# molybdenum
mo=calculate_materials.element('Mo')
mo.add_isotope_atom(92,91.906810,14.84)
mo.add_isotope_atom(94,93.905088,9.25)
mo.add_isotope_atom(95,94.905841,15.92)
mo.add_isotope_atom(96,95.904679,16.68)
mo.add_isotope_atom(97,96.906021,9.55)
mo.add_isotope_atom(98,97.905408,24.13)
mo.add_isotope_atom(100,99.907477,9.63)
mo.finalize()

# technetium
tc=calculate_materials.element('Tc')
tc.add_isotope_atom(98,97.907216,100.0)
tc.finalize()

# Ruthenium
ru=calculate_materials.element('Ru')
ru.add_isotope_atom(96,95.907598,5.54)
ru.add_isotope_atom(98,97.905287,1.87)
ru.add_isotope_atom(99,98.905939,12.76)
ru.add_isotope_atom(100,99.904220,12.60)
ru.add_isotope_atom(101,100.905582,17.06)
ru.add_isotope_atom(102,101.904350,31.55)
ru.add_isotope_atom(104,103.905430,18.62)
ru.finalize()

# Rhodium
rh=calculate_materials.element('Rh')
rh.add_isotope_atom(103,102.905504,100.0)
rh.finalize()

# Palladium
pd=calculate_materials.element('Pd')
pd.add_isotope_atom(102,101.905608,1.02)
pd.add_isotope_atom(104,103.904035,11.14)
pd.add_isotope_atom(105,104.905084,22.33)
pd.add_isotope_atom(106,105.903483,27.33)
pd.add_isotope_atom(108,107.903894,26.46)
pd.add_isotope_atom(110,109.905152,11.72)
pd.finalize()

# Silver
ag=calculate_materials.element('Ag')
ag.add_isotope_atom(107,106.905093,51.839)
ag.add_isotope_atom(109,108.904756,48.161)
ag.finalize()

# Cadmium
cd=calculate_materials.element('Cd')
cd.add_isotope_atom(106,105.906458,1.25)
cd.add_isotope_atom(108,107.904183,0.89)
cd.add_isotope_atom(110,109.903006,12.49)
cd.add_isotope_atom(111,110.904182,12.80)
cd.add_isotope_atom(112,111.902757,24.13)
cd.add_isotope_atom(113,112.904401,12.22)
cd.add_isotope_atom(114,113.903358,28.73)
cd.add_isotope_atom(116,115.904755,7.49)
cd.finalize()

# Indium
in_e=calculate_materials.element('In')
in_e.add_isotope_atom(113,112.904061,4.29)
in_e.add_isotope_atom(115,114.903878,95.71)
in_e.finalize()

# Tin
sn=calculate_materials.element('Sn')
sn.add_isotope_atom(112,111.904821,0.97)
sn.add_isotope_atom(114,113.902782,0.66)
sn.add_isotope_atom(115,114.903346,0.34)
sn.add_isotope_atom(116,115.901744,14.54)
sn.add_isotope_atom(117,116.902954,7.68)
sn.add_isotope_atom(118,117.901606,24.22)
sn.add_isotope_atom(119,118.903309,8.59)
sn.add_isotope_atom(120,119.902197,32.58)
sn.add_isotope_atom(122,121.903440,4.63)
sn.add_isotope_atom(124,123.905275,5.79)
sn.finalize()

# Antimony
sb=calculate_materials.element('Sb')
sb.add_isotope_atom(121,120.903818,57.21)
sb.add_isotope_atom(123,122.904216,42.79)
sb.finalize()

# Tellurium
te=calculate_materials.element('Te')
te.add_isotope_atom(120,119.904020,0.09)
te.add_isotope_atom(122,121.903047,2.55)
te.add_isotope_atom(123,122.904273,0.89)
te.add_isotope_atom(124,123.902819,4.74)
te.add_isotope_atom(125,124.904425,7.07)
te.add_isotope_atom(126,125.903306,18.84)
te.add_isotope_atom(128,127.904461,31.74)
te.add_isotope_atom(130,129.906223,34.08)
te.finalize()

# Iodine
i=calculate_materials.element('I')
i.add_isotope_atom(127,126.904468,100.0)
i.finalize()

# Xenon
xe=calculate_materials.element('Xe')
xe.add_isotope_atom(124,123.905896,0.09)
xe.add_isotope_atom(126,125.904269,0.09)
xe.add_isotope_atom(128,127.903530,1.92)
xe.add_isotope_atom(129,128.904779,26.44)
xe.add_isotope_atom(130,129.903508,4.08)
xe.add_isotope_atom(131,130.905082,21.18)
xe.add_isotope_atom(132,131.904154,26.89)
xe.add_isotope_atom(134,133.905395,10.44)
xe.add_isotope_atom(136,135.907220,8.87)
xe.finalize()

# Cesium
cs=calculate_materials.element('Cs')
cs.add_isotope_atom(133,132.905447,100.)
cs.finalize()

# Barium
ba=calculate_materials.element('Ba')
ba.add_isotope_atom(130,129.906310,0.106)
ba.add_isotope_atom(132,131.905056,0.101)
ba.add_isotope_atom(134,133.904503,2.417)
ba.add_isotope_atom(135,134.905683,6.592)
ba.add_isotope_atom(136,135.904570,7.854)
ba.add_isotope_atom(137,136.905821,11.232)
ba.add_isotope_atom(138,137.905241,71.698)
ba.finalize()

# Lanthanum
la=calculate_materials.element('La')
la.add_isotope_atom(138,137.907107,0.090)
la.add_isotope_atom(139,138.906348,99.910)
la.finalize()

# Cerium
ce=calculate_materials.element('Ce')
ce.add_isotope_atom(136,135.907144,0.185)
ce.add_isotope_atom(138,137.905986,0.251)
ce.add_isotope_atom(140,139.905434,88.450)
ce.add_isotope_atom(142,141.909240,11.114)
ce.finalize()

# Praseodymium
pr=calculate_materials.element('Pr')
pr.add_isotope_atom(141,140.907648,100.)
pr.finalize()

# Neodymium
nd=calculate_materials.element('Nd')
nd.add_isotope_atom(142,141.907719,27.2)
nd.add_isotope_atom(143,142.909810,12.2)
nd.add_isotope_atom(144,143.910083,23.8)
nd.add_isotope_atom(145,144.912569,8.3)
nd.add_isotope_atom(146,145.913112,17.2)
nd.add_isotope_atom(148,147.916889,5.7)
nd.add_isotope_atom(150,149.920887,5.6)
nd.finalize()

# Promethium
pm=calculate_materials.element('Pm')
pm.add_isotope_atom(145,144.912744,100.)
pm.finalize()

# Samarium
sm=calculate_materials.element('Sm')
sm.add_isotope_atom(144,143.911995,3.07)
sm.add_isotope_atom(147,146.914893,14.99)
sm.add_isotope_atom(148,147.914818,11.24)
sm.add_isotope_atom(149,148.917180,13.82)
sm.add_isotope_atom(150,149.917271,7.38)
sm.add_isotope_atom(152,151.919728,26.75)
sm.add_isotope_atom(154,153.922205,22.75)
sm.finalize()

# Europium
eu=calculate_materials.element('Eu')
eu.add_isotope_atom(151,150.919846,47.81)
eu.add_isotope_atom(153,152.921226,52.19)
eu.finalize()

# Gadolinium
gd=calculate_materials.element('Gd')
gd.add_isotope_atom(152,151.919788,0.20)
gd.add_isotope_atom(154,153.920862,2.18)
gd.add_isotope_atom(155,154.922619,14.80)
gd.add_isotope_atom(156,155.922120,20.47)
gd.add_isotope_atom(157,156.923957,15.65)
gd.add_isotope_atom(158,157.924101,24.84)
gd.add_isotope_atom(160,159.927051,21.86)
gd.finalize()

# Terbium
tb=calculate_materials.element('Tb')
tb.add_isotope_atom(159,158.925343,100.)
tb.finalize()

# Dysprosium
dy=calculate_materials.element('Dy')
dy.add_isotope_atom(156,155.924278,0.06)
dy.add_isotope_atom(158,157.924405,0.10)
dy.add_isotope_atom(160,159.925194,2.34)
dy.add_isotope_atom(161,160.926930,18.91)
dy.add_isotope_atom(162,161.926795,25.51)
dy.add_isotope_atom(163,162.928728,24.90)
dy.add_isotope_atom(164,163.929171,28.18)
dy.finalize()

# Holmium
ho=calculate_materials.element('Ho')
ho.add_isotope_atom(165,164.930319,100.)
ho.finalize()

# Erbium
er=calculate_materials.element('Er')
er.add_isotope_atom(162,161.928775,0.14)
er.add_isotope_atom(164,163.929197,1.61)
er.add_isotope_atom(166,165.930290,33.61)
er.add_isotope_atom(167,166.932045,22.93)
er.add_isotope_atom(168,167.932368,26.78)
er.add_isotope_atom(170,169.935460,14.93)
er.finalize()

# Thulium
tm=calculate_materials.element('Tm')
tm.add_isotope_atom(169,168.934211,100.)
tm.finalize()

# Ytterbium
yb=calculate_materials.element('Yb')
yb.add_isotope_atom(168,167.933894,0.13)
yb.add_isotope_atom(170,169.934759,3.04)
yb.add_isotope_atom(171,170.936322,14.28)
yb.add_isotope_atom(172,171.936378,21.83)
yb.add_isotope_atom(173,172.938207,16.13)
yb.add_isotope_atom(174,173.938858,31.83)
yb.add_isotope_atom(176,175.942568,12.76)
yb.finalize()

# Lutetium
lu=calculate_materials.element('Lu')
lu.add_isotope_atom(175,174.940768,97.41)
lu.add_isotope_atom(176,175.942682,2.59)
lu.finalize()

# Hafnium
hf=calculate_materials.element('Hf')
hf.add_isotope_atom(174,173.940040,0.16)
hf.add_isotope_atom(176,175.941402,5.26)
hf.add_isotope_atom(177,176.943220,18.60)
hf.add_isotope_atom(178,177.943698,27.28)
hf.add_isotope_atom(179,178.945815,13.62)
hf.add_isotope_atom(180,179.946549,35.08)
hf.finalize()

# Tantalum
ta=calculate_materials.element('Ta')
ta.add_isotope_atom(180,179.947466,0.012)
ta.add_isotope_atom(181,180.947996,99.988)
ta.finalize()

# Tungsten
w=calculate_materials.element('W')
w.add_isotope_atom(180,179.946706,0.12)
w.add_isotope_atom(182,181.948206,26.50)
w.add_isotope_atom(183,182.950224,14.31)
w.add_isotope_atom(184,183.950933,30.64)
w.add_isotope_atom(186,185.954362,28.43)
w.finalize()

# Rhenium
re=calculate_materials.element('Re')
re.add_isotope_atom(185,184.952956,37.40)
re.add_isotope_atom(187,186.955751,62.60)
re.finalize()

# Osmium
os=calculate_materials.element('Os')
os.add_isotope_atom(184,183.952491,0.02)
os.add_isotope_atom(186,185.953838,1.59)
os.add_isotope_atom(187,186.955748,1.96)
os.add_isotope_atom(188,187.955836,13.24)
os.add_isotope_atom(189,188.958145,16.15)
os.add_isotope_atom(190,189.958445,26.26)
os.add_isotope_atom(192,191.961479,40.78)
os.finalize()

# Iridium
ir=calculate_materials.element('Ir')
ir.add_isotope_atom(191,190.960591,37.3)
ir.add_isotope_atom(193,192.962924,62.7)
ir.finalize()

# Platinum
pt=calculate_materials.element('Pt')
pt.add_isotope_atom(190,189.959930,0.014)
pt.add_isotope_atom(192,191.961035,0.782)
pt.add_isotope_atom(194,193.962664,32.967)
pt.add_isotope_atom(195,194.964774,33.832)
pt.add_isotope_atom(196,195.964935,25.242)
pt.add_isotope_atom(198,197.967876,7.163)
pt.finalize()

# Gold
au=calculate_materials.element('Au')
au.add_isotope_atom(197,196.966552,100.)
au.finalize()

# Mercury
hg=calculate_materials.element('Hg')
hg.add_isotope_atom(196,195.965815,0.15)
hg.add_isotope_atom(198,197.966752,9.97)
hg.add_isotope_atom(199,198.968262,16.87)
hg.add_isotope_atom(200,199.968309,23.10)
hg.add_isotope_atom(201,200.970285,13.18)
hg.add_isotope_atom(202,201.970626,29.86)
hg.add_isotope_atom(204,203.973476,6.87)
hg.finalize()

# Thallium
tl=calculate_materials.element('Tl')
tl.add_isotope_atom(203,202.972329,29.524)
tl.add_isotope_atom(205,204.974412,70.476)
tl.finalize()

# Lead
pb=calculate_materials.element('Pb')
pb.add_isotope_atom(204,203.973029,1.4)
pb.add_isotope_atom(206,205.974449,24.1)
pb.add_isotope_atom(207,206.975881,22.1)
pb.add_isotope_atom(208,207.976636,52.4)
pb.finalize()

# Bismuth
bi=calculate_materials.element('Bi')
bi.add_isotope_atom(209,208.980383,100.)
bi.finalize()

# Thorium
th=calculate_materials.element('Th')
th.add_isotope_atom(232,232.038050,100.)
th.finalize()

# Protactinium
pa=calculate_materials.element('Pa')
pa.add_isotope_atom(232,231.035879,100.)
pa.finalize()

# Uranium
u=calculate_materials.element('U')
u.add_isotope_atom(234,234.040946,0.0055)
u.add_isotope_atom(235,235.043923,0.7200)
u.add_isotope_atom(238,238.050783,99.2745)
u.finalize()