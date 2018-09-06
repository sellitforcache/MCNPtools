#! /usr/bin/env python 



from MCNPtools.mctal import Mctal
tal=mctal('./case001-noww.mctal')
tal.write_weight_windows_from_meshtal(output='2dflux.wwinp',
                                      tals =[[101]     ,[111]    ,'e','/','*','z'],
                                      norms=[[0.5*5e-3],[0.5*1.0],'' ,'' ,'' ,'' ],
                                      energies=  [[],[],[],[],[],[]],
                                      normpoints=[[],[],[],[],[],[]],
                                      mask_weight=[[  0.],[ 0.],[ 0.],[ 0.],[ 0.],[ 0.]],
                                      kill_weight=[[ 10.],[10.],[10.],[10.],[10.],[10.]])
