sample input to illustrate mctal plotting etc
1  1  -1.0   1 -2 3 -4 5 -6
2  3 -8.96   -7
3  0         -8
4  0         -9
98 0        (-1:2:-3:4:-5:6) 7 8 9 -99
99 0           99

1   px  -500
2   px   500
3   py   100
4   py  1100
5   pz  -500
6   pz   500
7   s  -380 0 0  10
8   s     0 1120  0   15
9   s  -520  600  0   15
99  so  3000

c
c
c         'light water'
c
c         average amu     =   6.00509560
c         density         =   1.00000000
c
c         mixture     avg. amu     atom fraction    mass fraction    volume fraction
c         --------    --------     -------------    -------------    ---------------
c                O     15.9994     0.33333333       0.88810161       0.33281973
c                H      1.0079     0.66666667       0.11189839       0.66718027
c
c
c
c ISOTOPES FOR 'light water'
c
m1
       1001   6.6659000000E-01
       1002   7.6666666667E-05
       8016   3.3252333333E-01
       8017   1.2666666667E-04
mt1 lwtr
mx1:p            $ turn off photonuclear for hydrogen explicitly
          0
          1002
          8016
          8017
c
c
c
c         'B4C'
c
c         average amu     =  11.05096939
c         density         =   2.52000000
c
c         mixture     avg. amu     atom fraction    mass fraction    volume fraction
c         --------    --------     -------------    -------------    ---------------
c                B     10.8110     0.80000000       0.78263018       0.77665421
c                C     12.0107     0.20000000       0.21736982       0.22334579
c
c
c
c ISOTOPES FOR 'B4C'
c
m2
       5010   1.5920000000E-01
       5011   6.4080000000E-01
       6012   1.9786000000E-01
       6013   2.1400000000E-03
c
c
c
c         Cu
c
c         element     avg. amu     atom fraction    mass fraction
c         --------    --------     -------------    -------------
c            29000     63.5456     1.00000000       1.00000000
c
c         average amu     =  63.54564390
c         density         =   8.96000000
c
m3
      29063      6.9170000000E-01
      29065      3.0830000000E-01
c
mode n p e / * z
imp:n,p,e,/,*,z 1 1 1 1 1 0
print
mphys on
rand  gen=2  seed=777
nps 1e2
prdmp j 1e2 1 4 1e2
c
cut:e j 0.01
cut:n j 0.00 -1e-8  -5e-9
cut:p j 0.01     0      0
phys:n 1000
phys:p 1000  0 0 1
phys:e 1000
c wwp:n j j j j -1 0
c wwp:p j j j j -1 0
c wwp:e j j j j -1 0
c wwp:/ j j j j -1 0
c wwp:* j j j j -1 0
c wwp:z j j j j -1 0
c
c 1 GeV electrons on copper
sdef
       par=e
       axs=1 0 0
       x=-380
       y=-11
       z=0
       vec=0 1 0
       dir=1
       erg 1000
c
c
c  tallies
c
f1:n  7 8 9
fc1  neutron tallies in water sphere
c1   0 1
e1 1e-9  2046ilog  1e2
c
f11:p  7 8 9
fc11  photon tallies in water sphere
c11   0 1
e11 1e-9  2046ilog  1e2
c
c
c mesh tally
c
TMESH
rmesh101:n
 cora101    -500  199i  500
 corb101    -100  239i 1100
 corc101    -500        500
 rmesh111:p
  cora111    -500  199i  500
  corb111    -100  239i 1100
  corc111    -500        500
ENDMD
