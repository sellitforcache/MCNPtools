#! /usr/bin/env python
#
#
#
from MCNPtools import mctal
import matplotlib.pyplot as plt

#
tal = mctal('sample.m')

#

#
for i in [0,1,2,3,4]:
    tal.plot(tal=[1],obj=[i],cos=[0,1],options=['lethargy','logy'])
    plt.show()

tal.tallies[1].plot(obj=[0,1,2,3,4],cos=[0,1],options=['lethargy','logy'])
plt.show()


for i in [0,1,2]:
    tal.plot(tal=[101],obj=[i])
    plt.show()
