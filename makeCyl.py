#! /usr/bin/env python
# Script to generate a rotated circular cylinder with GQ cards in MCNP
# Ryan M. Bergmann, Dec 9, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

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

### translation
trans_x = 0.0
trans_y = 0.0
trans_z = 0.0
print "translation (x,y,z) = ", trans_x, ", ",trans_y, ", ",trans_z

### define cylinder axis (x,y,z) and radius
## short sides, x, inside
#rad = 20.0
#axis_vec=numpy.array([-56.755,0.00000001,540.0])  
#print "x translation =",(rad-6.9385)
## long sides, y, inside
#rad = 46.72
#axis_vec=numpy.array([0.000000001,-7.19,540.0])
#print "x translation =",(rad-7.42)
## corner corrections, inside
#rad = 29.0  
#axis_vec=numpy.array([5.82,-0.38,54.0])
#corner_vec = numpy.array([5.75,7.07])
#mag = numpy.linalg.norm(corner_vec)
#cut = 1.0  # amount of overlap, ie the cut
#print "x/y translation = ",(1.0-(rad+cut)/mag)*corner_vec
## short sides, x, outside
#rad = 20.0
#axis_vec=numpy.array([-62.735,0.00000001,540.0])  
#print "x translation =",(rad-7.3385)
## long sides, y, outside
#rad = 46.72
#axis_vec=numpy.array([0.000000001,-13.19,540.0])
#print "x translation =",(rad-7.82)
## corner corrections, outside
rad = 29.0  
axis_vec=numpy.array([6.22,0.12,54.0])
corner_vec = numpy.array([5.72,7.48])
mag = numpy.linalg.norm(corner_vec)
cut = 1.0  # amount of overlap, ie the cut
print "x/y translation = ",(1.0-(rad+cut)/mag)*corner_vec

### print radius
print "radius = ", rad

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
A = ct*ct*cp*cp + sp*sp
B = ct*ct*sp*sp + cp*cp
C = st*st
D = -2.0*sp*cp*st*st
E = -2.0*st*ct*sp
F = -2.0*st*ct*cp
G = 0.0
H = 0.0
J = 0.0
K =  -rad*rad


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