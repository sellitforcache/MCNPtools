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
	return [ene,vals,errs]


i=0
c=['b','r','g','k','c','m','y']
if len(sys.argv)>8:
	c.append(numpy.random.rand(3,1))
fig = pylab.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)
datalist = []
sumlist = []

for filename in sys.argv[1:]:
	
	data  	   = get_mcnp_mctal(filename) 
	tally      = data[1][:-1] #numpy.loadtxt(filename+".tally")
	sumlist.append(data[1][-1])
	tallybins  = data[0] #numpy.loadtxt(filename+".tallybins")
	tallyerr   = data[2][:-1]
	title = filename
	datalist.append(tally)
	
	tallybins=numpy.hstack((numpy.array([0]),tallybins))
	widths=numpy.diff(tallybins)
	avg=(tallybins[:-1]+tallybins[1:])/2;
	newflux=tally
	newflux=numpy.divide(newflux,widths)
	#newflux=numpy.multiply(newflux,avg)
	
	ax.semilogx(avg,newflux,linestyle='steps-mid',label=filename,color=c[i])
	i=i+1
	#ax.loglog(avg,np.multiply(newflux,np.add(1.0,tallyerr))     ,'r',linestyle='steps-mid',label='WARP')
	#ax.loglog(avg,np.multiply(newflux,np.subtract(1.0,tallyerr)),'b',linestyle='steps-mid',label='WARP')
	
ax.set_xlabel('Energy (MeV)')
ax.set_ylabel('Flux4 tally / bin width')
#ax.set_ylabel('Normalized Flux/Lethary')
#ax.set_title(title)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,labels,loc=1)
ax.set_xlim([1e-11,20])
ax.grid(True)
pylab.show()


fig = pylab.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)
ax.semilogx(avg,numpy.divide(datalist[1],datalist[0]),linestyle='steps-mid',color='k')
ax.set_xlabel('Energy (MeV)')
ax.set_ylabel('Ratio '+sys.argv[2]+' / '+sys.argv[1])
ax.set_xlim([1e-11,20])
ax.set_ylim([0,2])
ax.grid(True)
pylab.show()


### sum and find rel diff
a = numpy.sum(datalist[0])
b = numpy.sum(datalist[1])
print 'summed vector 1 =', a, '||| sum from output 1 =',sumlist[0]
print 'summed vector 2 =', b, '||| sum from output 2 =',sumlist[1]
print 'Rel. Diff. '+sys.argv[2]+' / '+sys.argv[1]+' - 1 = ',(b/a-1.0)
