sample input to illustrate mctal plotting etc
1  1  -1.0  -1
2  1  -1.0   1 -2
3  1  -1.0   2 -3
4  1  -1.0   3 -4 5
5  2  -2.52    -5
98 0        4 -99
99 0           99

1    so   1.0
2    so   2.0
3    so   5.0
4    so  10.0
5    s    7  0  0    1.5
99   so  99.0

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
mode n p
imp:n 1 1 1 1 1 1 0
print
prdmp j 1e5 1 4 1e5
nps     1e6
c Watt fission spec @ center
sdef pos 0 0 0
     erg d1
SP1 -3  0.965 2.29
c
c
c  tallies
c
f1:n  1 2 3 4 5
fc1  neutron tallies in water sphere
c1   0 1
e1 1e-9  2046ilog  1e2
c
f11:p  1 2 3 4
fc11  photon tallies in water sphere
c11   0 1
e11 1e-9  2046ilog  1e2
c
c
c mesh tally
c
TMESH
  rmesh101:n
   cora101    -10  199i  10
   corb101    -10  199i  10
   corc101     -2  0  2  10
ENDMD
