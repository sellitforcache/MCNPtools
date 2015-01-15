#! /usr/bin/env python
# Script to generate transformation cards in MCNP
# Ryan M. Bergmann, Jan 5, 2015.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import numpy

def rod_rot(a,b,v='unset'):
	# Rodrigues' rotation formula, rotate a to b
	if v=='unset':
		v = numpy.cross(a, b)
	print "ortho ",v
	c  = numpy.dot(a, b)
	vx = numpy.array([[0.0,-v[2],v[1]],[v[2],0.0,-v[0]],[-v[1],v[0],0.0]])
	r  = c*numpy.identity(3)+numpy.sqrt(1.0-c*c)*vx + (1.0-c)*numpy.outer(v,v)
	return r

### print form
print "TRn card form: O1 O2 O3 B1 B2 B3 B4 B5 B6 B7 B8 B9 M"

### local coordinate system
o_l = numpy.array([0.0,0.0,0.0])   # old origin
v_l = numpy.array([0.0,0.0,1.0])   # object axis
v_l = v_l / numpy.linalg.norm(v_l)

### destination coordinate system
o_d = numpy.array([-18.6771,15.1242,5.0])             # new origin
v_d = numpy.array([15.1242,18.6771,0.0])  # vector to align old axis to
v_d = v_d / numpy.linalg.norm(v_d)


### origin translation
origin = o_d-o_l

### translation along destination direction
mag = 0.0
origin = origin + mag*v_d

### do first transform
r  = rod_rot(numpy.array([0.0,-1.0,0.0]),v_d,v_l) 
r2 = rod_rot(v_l,v_d) 
r  = numpy.dot(r2,r)

### print card
print "MCNP CARD:"
print "TRn  ",origin[0],origin[1],origin[2],r[0,0],r[1,0],r[2,0],r[0,1],r[1,1],r[2,1],r[0,2],r[1,2],r[2,2],1