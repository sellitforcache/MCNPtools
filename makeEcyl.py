#! /usr/bin/env python
# Script to generate a rotated elliptic cylinder with GQ cards in MCNP
# Ryan M. Bergmann, Dec 11, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm, Normalize
from matplotlib import cm
import sys
import numpy
import re

### print misc
print "GQ card form:  Ax^2 + By^2 + Cz^2 + Dxy + Eyz + Fxz + Gx + Hy + Jz + K = 0"

### cyclinder radius, translation
a =    # semimajor axis in x
b =    # semimajor axis in y
a_sqi = 1.0 / (a*a)
b_sqi = 1.0 / (b*b)
trans_x = 0.0
trans_y = 0.0
trans_z = 0.0
print "a (x) =", a,"b (y) =",b
print "translation (x,y,z) = ", trans_x, ", ",trans_y, ", ",trans_z

### define cylinder axis (x,y,z)
#axis_vec=numpy.array([0.0000001,-15.65,540.0])   # long sides
axis_vec=numpy.array([3.27,64.91,540.0])   # corner corrections

### normalize
axis_vec      = numpy.divide(axis_vec,numpy.sqrt(numpy.sum(numpy.multiply(axis_vec,axis_vec))))
print "normed axis vector = ", axis_vec

### get spherical coordinates
phi   = numpy.arctan(axis_vec[1]/axis_vec[0])
theta = numpy.arccos(axis_vec[2])
print "theta = ",theta," phi = ",phi

### variablize trigs
st = numpy.sin(theta)
ct = numpy.cos(theta)
sp = numpy.sin(phi)
cp = numpy.cos(phi)

### calculate coeffs
A = a_sqi*ct*ct*cp*cp + b_sqi*sp*sp
B = a_sqi*ct*ct*sp*sp + b_sqi*cp*cp
C = a_sqi*st*st
D =  2.0*cp*sp*(a_sqi*ct*ct-b_sqi)
E = -2.0*a_sqi*st*ct*sp
F = -2.0*a_sqi*st*ct*cp
G =  0.0
H =  0.0
J =  0.0
K = -1.0


### do linear translation
K = K + A*trans_x*trans_x + B*trans_y*trans_y + C*trans_z*trans_z + D*trans_x*trans_y + E*trans_y*trans_z + F*trans_x*trans_z - G*trans_x - H*trans_y - J*trans_z
G = G - 2.0*A*trans_x - D*trans_y - F*trans_z
H = H - 2.0*B*trans_y - D*trans_x - E*trans_z
J = J - 2.0*C*trans_z - E*trans_y - F*trans_x

### print
print 'A = ', A      # x^2
print 'B = ', B      # y^2
print 'C = ', C      # z^2
print 'D = ', D     # xy
print 'E = ', E      # yz
print 'F = ', F      # xz
print 'G = ', G      # x
print 'H = ', H      # y
print 'J = ', J      # z
print 'K = ', K      # const

print "MCNP CARD:"

print "XX  gq  ",A,B,C,D
print "      ",E,F,G
print "      ",H,J,K