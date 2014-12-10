#! /usr/bin/python
import pylab
import sys
import numpy
import os
import re
import numpy as np

def get_serpent_det(filepath):
	fobj    = open(filepath)
	fstr    = fobj.read()
	names   = re.findall('[a-zA-Z]+ *= *\[',fstr)
	data    = re.findall('\[ *\n[\w\s+-.]+\];',fstr)
	alldata = dict()
	dex     = 0
	for name in names:
		varname  = name.split()[0]
		moredata = re.findall(' [ .+-eE0-9^\[]+\n',data[dex])
		thisarray = numpy.array(moredata[0].split(),dtype=float)
		for line in moredata[1:]:
			thisarray=numpy.vstack((thisarray,numpy.array(line.split(),dtype=float)))
		alldata[varname]=numpy.mat(thisarray)
		dex = dex + 1
	return alldata

def get_mcnp_mctal(filepath):
	fobj    = open(filepath)
	fstr    = fobj.read()
	ene 	= re.findall('et +[0-9.E\+\- \n]+',fstr)
	ene 	= ene[0].split()
	ene 	= numpy.array(ene[2:],dtype=float)
	vals    = re.findall('vals *[0-9.E\+\- \n]+',fstr)
	vals 	= vals[0].split()
	vals 	= numpy.array(vals[1:],dtype=float)
	errs 	= vals[1::2]
	vals 	= vals[0::2]
	alldata = numpy.array([ene,vals,errs])
	return alldata

filename   = sys.argv[1]
tally      = numpy.loadtxt(filename+".tally")
tallybins  = numpy.loadtxt(filename+".tallybins")
title = filename

widths=numpy.diff(tallybins);
avg=(tallybins[:-1]+tallybins[1:])/2;
newflux=numpy.array(tally[:,0])
warp_err = numpy.array(tally[:,1])
newflux=numpy.divide(newflux,widths)
newflux=numpy.multiply(newflux,avg)

fig = pylab.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)
ax.semilogx(avg,newflux,'k',linestyle='steps-mid',label='WARP')
ax.semilogx(avg,np.multiply(newflux,np.add(1.0,warp_err))     ,'r',linestyle='steps-mid',label='WARP')
ax.semilogx(avg,np.multiply(newflux,np.subtract(1.0,warp_err)),'b',linestyle='steps-mid',label='WARP')
ax.set_xlabel('Energy (MeV)')
ax.set_ylabel('Normalized Flux/Lethary')
ax.set_title(title)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,labels,loc=2)
ax.set_xlim([1e-11,20])
ax.grid(True)
pylab.show()

