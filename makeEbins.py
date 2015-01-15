#! /usr/bin/python

import sys
import numpy as np

if len(sys.argv) == 5:
	e0 = float(sys.argv[1])
	e1 = float(sys.argv[2])
	ne = int(sys.argv[3])
	unit = sys.argv[4]
	if unit == 'A' or unit == 'angstrom' or unit == 'a' or unit == 'Angstrom':
		unit = 'Angstrom'
else:
	print "must specifiy energy bounds, number of bins, and if it is in angstrom/MeV/eV"

print "Making",ne, "bins from",e0,"to",e1,unit

logoption = 0

a = np.linspace(e0,e1,ne+1)

if unit == 'MeV':
	c = a
	print "\n".join('      %10.8E'%F for F in c )
elif unit == 'eV':
	c = a*1.0e-6
	print "\n".join('      %10.8E'%F for F in c )
elif unit=='Angstrom':
	b = np.power(np.divide(0.286014369,a),2)*1.0e-6
	c = b[::-1]
	print "\n".join('      %10.8E'%F for F in c )
else:
	print "invalid unit!"