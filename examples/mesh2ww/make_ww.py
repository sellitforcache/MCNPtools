#! /usr/bin/env python
from MCNPtools.mctal import Mctal
import re


tal=Mctal('./iteration_3/flux2ww.m')

# look at target tally to get the average weight of the particles leaving
f=open('./iteration_1/flux2ww.o2','r')
output_file_string = f.read()
f.close()

nps = tal.nps
print "\nNPS %d"%nps

rxns=['total']
particles = ['neutron','photon']
wgt_out={}
for particle in particles:
    print "\n%s production\n========================\n"%particle
    print "%15s %15s %15s %15s %25s"%('Reaction','Tracks','Tracks/NPS','Weight/NPS','Avg. Weight/Track')
    for rxn in rxns:
        this_re = re.compile('%s creation.*?%s +([0-9]+) +([0-9.eE+-]+)'%(particle,rxn),flags=re.DOTALL)
        this_match = this_re.search(output_file_string)
        tracks = float(this_match.group(1))
        weight = float(this_match.group(2))
        print "%15s %15d %15.4E %15.4E %25.4E"%(rxn, tracks, tracks/nps, weight, weight/tracks*nps)
        if rxn=='total':
            wgt_out[particle]=weight/tracks*nps
print ""


#
#
#
tal.write_weight_windows_from_meshtal(output='2dflux.wwinp',
                                      tals =[[101]                   ,[111]                   ,'e','/','*','z'],
                                      norms=[[0.5*wgt_out['neutron']],[0.5**wgt_out['photon']],'' ,'' ,'' ,'' ],
                                      energies=  [[],[],[],[],[],[]],
                                      normpoints=[[],[],[],[],[],[]],
                                      smooth=    [[31],[31],[],[],[],[]],
                                      mask_weight=[[  0.],[ 0.],[ 0.],[ 0.],[ 0.],[ 0.]],
                                      kill_weight=[[ 10.],[10.],[10.],[10.],[10.],[10.]])
