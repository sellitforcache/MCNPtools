#! /usr/bin/env python
#
#
#
from MCNPtools import Mctal
import matplotlib.pyplot as plt
import numpy

# load the file
tal = Mctal('sample.m')

# using the plot method of the Mctal class
# keywords (default):
# ax            = (None)    matplotlib axis object to plot onto.  makes one internally if not passed
# tal           = (False)   list of tally numbers to plot.  numbers are those used in MCNP, e.g. f1:n -> tal=[1]
# obj           = (False)   list of objects to plot.  numbers are the index (starting at 0), not the cell/surface/whatever number on the f card.  e.g.  f1:n  1001 1002 1003  ->  to plot surface 1003, you would do: tal=[1], obj=[2]
# cos           = (False)   list of cosine bins to plot.  numbers are the index (starting at 0). f1:n  1001 1002 1003; c1 0 1  ->  to plot the outward cosine bin of surface 1003, you would do: tal=[1], obj=[2], cos=[1]
# seg           = (False)   list of segment bins to plot.  numbers are the index (starting at 0).  f1:n  1001 1002 1003; fs1  -2003  ->  to plot the tally contribution from the (-) side of surface 2003, you would do: tal=[1], obj=[2], seg=[0]
# mul           = (False)   list of multiplier bins to plot.  numbers are the index (starting at 0). similar to the previous.
# t_or_d        = (False)   list of t bins to plot.  numbers are the index (starting at 0). similar to the previous.
#  TIME BINNING NOT SUPPORTED YET!
# options       = (False)   list of plotting options, see README.md
# ylim          = (False)   list of y limts to overrride the automatic ones
# renorm_to_sum = (False)   flag to divide the tally values by the sum of the bins
# color         = (False)   color of the trace - uses normal matplotlib options (just passes them)
# norm          = (1.0)     normalization factor to multiply by the tally values
# label         = (False)   label for legend
#
#
# !!! arguments of the tally segmentation must be *lists*
for i in [0,1,2,3,4]:
    tal.plot(tal=[1],obj=[i],cos=[0,1],options=['lethargy','logy']) #
    plt.show()

# you can also directly acess the tally plot method from the list of Tally instances in the  Mctal instance
tal.tallies[1].plot(obj=[0,1,2,3,4],cos=[0,1],options=['lethargy','logy'])
plt.show()

# mesh tallies cna also be plotted
for i in [0,1,2]:
    tal.plot(tal=[101],obj=[i])
    plt.show()

# passing an axis to the plotter
f=plt.figure()
ax=f.add_subplot(111)
tal.tallies[1].plot(ax=ax,obj=[0,1,2,3,4],cos=[0,1],options=['lethargy','logy'])
ax.set_xlabel('NOW I CAN CHANGE THINGS')
ax.set_title('DESCRIPIVE CUSTOM TITLE')
plt.tight_layout()
plt.show()

# the _hash function can provide the appropriate index in the data array in order to get the raw data
dex = tal.tallies[1]._hash(obj=1,cos=1)
erg = tal.tallies[1].energies[:-1]  # last bin is 'total' string
val = tal.tallies[1].vals[dex]['data'][:-1] # last bin is the total
erg = numpy.array(erg)  # convert list to array so can do next line
avg = (erg[1:]+erg[:-1])/2.  # compute midpoint
f=plt.figure()
ax=f.add_subplot(111)
ax.loglog(avg,val)
ax.set_xlabel('MeV')
ax.set_ylabel('Tally Value')
ax.set_title('USING THE matplotlib PLOTTER INSTEAD OF THE MCNPTOOLS STEP PLOTTER')
ax.grid(1)
plt.show()
