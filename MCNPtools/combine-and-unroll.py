#! /home/l_bergmann/anaconda/bin/python -W ignore
#! /usr/local/bin/python -W ignore
#
# A MCNP surface source to histogram distribution maker
# which combined the outputs from previously binned distributions
# Ryan M. Bergmann, October 2015 
# ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import numpy, sys, cPickle, time


class histogram:

	def __init__(self,bins):
		self.bins		= 	copy.deepcopy(bins)  # bins are edges
		self.n_bins		=	len(bins)
		self.values		=	numpy.zeros((self.n_bins-1,))
		self.sqvals		=	numpy.zeros((self.n_bins-1,))
		self.counts		=	numpy.zeros((self.n_bins-1,))
		self.err		=	numpy.zeros((self.n_bins-1,))

	def add(self,bin_val,weight):

		# check if in bounds
		valid = True
		if bin_val < self.bins[0] or bin_val > self.bins[-1]:
			print bin_val,' out of bounds!!!'
			valid = False

		# add weight to bin if between bins
		if valid:
			dex = next((i for i, x in enumerate(bin_val < self.bins) if x), False) - 1
			self.values[dex] = self.values[dex] + weight
			self.sqvals[dex] = self.sqvals[dex] + weight*weight
			self.counts[dex] = self.counts[dex] + 1

	def update(self):

		# calculate error
		for dex in range(0,self.n_bins-1):
			N		= self.counts[dex]
			sum_xi	= self.values[dex]
			sum_xi2	= self.sqvals[dex]
			if N==1:
				self.err[dex] = 1.0
			elif N > 1:
				tally_err_sq =   1.0/(N-1) * ( N*sum_xi2/(sum_xi*sum_xi) - 1.0) 
				if tally_err_sq > 0:
					self.err[dex] = numpy.sqrt(tally_err_sq)
				else:
					self.err[dex] = 0.0
			else:
				self.err[dex] = 0.0

def make_independent_distribution(file_obj,dist_number,vector_vars,vector_probs):
	assert(len(vector_vars)==len(vector_probs)+1)
	string0 = 'SI%d      '%dist_number
	file_obj.write(string0)
	total_len = len(string0)
	for k in range(0,len(vector_vars)):
		#if vector_probs[k]>0.0:
		string1=' % 8.7E'%vector_vars[k]
		total_len = total_len + len(string1)
		if total_len > 80:
			file_obj.write('\n'+' '*max(5,len(string0)))
			total_len = len(string1)+max(5,len(string0))
		file_obj.write(string1)
	file_obj.write('\n')
	string0 = 'SP%d      '%dist_number
	file_obj.write(string0)
	total_len = len(string0)
	string1=' %6.4E'%0.0
	total_len = total_len + len(string1)
	file_obj.write(string1)
	for k in range(0,len(vector_probs)):
		#if vector_probs[k]>0.0:
		string1=' %6.4E'%vector_probs[k]
		total_len = total_len + len(string1)
		if total_len > 80:
			file_obj.write('\n'+' '*max(5,len(string0)))
			total_len = len(string1)+max(5,len(string0))
		file_obj.write(string1)
	file_obj.write('\n')

def make_independent_distribution_intlines(file_obj,dist_number,vector_vars,vector_probs):
	assert(len(vector_vars)==len(vector_probs))
	string0 = 'SI%d    L '%dist_number
	file_obj.write(string0)
	total_len = len(string0)
	for k in range(0,len(vector_vars)):
		#if vector_probs[k]>0.0:
		string1=' %d'%vector_vars[k]
		total_len = total_len + len(string1)
		if total_len > 80:
			file_obj.write('\n'+' '*max(5,len(string0)))
			total_len = len(string1)+max(5,len(string0))
		file_obj.write(string1)
	file_obj.write('\n')
	string0 = 'SP%d      '%dist_number
	file_obj.write(string0)
	total_len = len(string0)
	string1=''
	total_len = total_len + len(string1)
	file_obj.write(string1)
	for k in range(0,len(vector_probs)):
		#if vector_probs[k]>0.0:
		string1=' %6.4E'%vector_probs[k]
		total_len = total_len + len(string1)
		if total_len > 80:
			file_obj.write('\n'+' '*max(5,len(string0)))
			total_len = len(string1)+max(5,len(string0))
		file_obj.write(string1)
	file_obj.write('\n')


def make_dependent_distribution(file_obj,dist_number,secondary_dist_start,vector_vars,vector_probs):
	
	#write distribution of distributions card
	string0 = 'DS%d   S '%dist_number
	file_obj.write(string0)
	total_len = len(string0)
	for k in range(0,len(vector_probs)):
		#if probs[k]>0.0:
		string1=' D%d'%(k+secondary_dist_start)
		total_len = total_len + len(string1)
		if total_len > 80:
			file_obj.write('\n'+' '*max(5,len(string0)))
			total_len = len(string1)+max(5,len(string0))
		file_obj.write(string1)
	file_obj.write('\n')
	file_obj.write('c\nc\nc\n')

	# write secondary distributions themselves
	for k in range(0,len(vector_probs)):
		#if probs[k]>0.0:
		# SI card first
		string0 = 'SI%d    '%(k+secondary_dist_start)
		file_obj.write(string0)
		total_len = len(string0)  
		for j in range(0,len(vector_vars[k])):
			string1=' %6.4E'%vector_vars[k][j]
			total_len = total_len + len(string1)
			if total_len > 80:
				file_obj.write('\n'+' '*max(5,len(string0)))
				total_len = len(string1)+max(5,len(string0))
			file_obj.write(string1)
		file_obj.write('\n')
		# SP card second
		string0 = 'SP%d    '%(k+secondary_dist_start)
		file_obj.write(string0)
		total_len = len(string0)
		string1=' %6.4E'%0.0
		total_len = total_len + len(string1)
		file_obj.write(string1)  
		for j in range(0,len(vector_probs[k])):
			string1=' %6.4E'%vector_probs[k][j]
			total_len = total_len + len(string1)
			if total_len > 80:
				file_obj.write('\n'+' '*max(5,len(string0)))
				total_len = len(string1)+max(5,len(string0))
			file_obj.write(string1)
		file_obj.write('\n')
		file_obj.write('c \n')

def make_dependent_list(file_obj,dist_number,vector_vars):
	
	#write distribution of distributions card
	string0 = 'DS%d   L '%dist_number
	file_obj.write(string0)
	total_len = len(string0)
	for k in range(0,len(vector_vars)):
		#if probs[k]>0.0:
		string1=' %d'%vector_vars[k]
		total_len = total_len + len(string1)
		if total_len > 80:
			file_obj.write('\n'+' '*max(5,len(string0)))
			total_len = len(string1)+max(5,len(string0))
		file_obj.write(string1)
	file_obj.write('\n')
	file_obj.write('c\nc\nc\n')


def smooth(x,window_len=11,window='flat'):
	# take from stackexchange
	import numpy

	if x.ndim != 1:
		raise ValueError, "smooth only accepts 1 dimension arrays."

	if x.size < window_len:
		raise ValueError, "Input vector needs to be bigger than window size."

	if window_len<3:
		return x

	if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
		raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


	s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
	#print(len(s))
	if window == 'flat': #moving average
		w=numpy.ones(window_len,'d')
	else:
		w=eval('numpy.'+window+'(window_len)')

	y=numpy.convolve(w/w.sum(),s,mode='valid')
	return y



def sum_spec_bins(bins,spec_total,range1):
	this_sum=0.0
	for i in range(0,len(spec_total)):
		if bins[i]>=range1[0] and bins[i]<=range1[1] and bins[i+1]>=range1[0] and bins[i+1]<=range1[1]:
			this_sum = this_sum + spec_total[i]
		elif range1[0] > bins[i] and range1[0] < bins[i+1] and range1[1] > bins[i+1]:  # bin partially inside
			r =  (bins[i+1]-range1[0])/(bins[i+1]-bins[i])
			this_sum = this_sum + spec_total[i]*r
		elif range1[1] > bins[i] and range1[1] < bins[i+1] and range1[0] < bins[i]:  # bin partially inside
			r = (range1[1]-bins[i])/(bins[i+1]-bins[i])
			this_sum = this_sum + spec_total[i]*r
		elif range1[0] > bins[i] and range1[0] < bins[i+1] and range1[1] > bins[i] and range1[1] < bins[i+1]:
			r = (range1[1]-range1[0])/(bins[i+1]-bins[i])
			this_sum = this_sum + spec_total[i]*r
		else:
			pass 
			#print "bin %d, %6.4E > %6.4E"%(i,histograms_curr[0].bins[i],range1[1])
	return this_sum


def integrate_spec_points(bins,spec_total,range1):
	this_sum = quad(numpy.interp, range1[0], range1[1], args=(bins,spec_total))
	return this_sum[0]  # second value is error

def integrate_spec_bins(bins,spec_total,range1):
	def integrand(x,bins,vals):
		index = numpy.where( bins >= x )[0][0]
		return vals[index]
	this_sum = quad(integrand, range1[0], range1[1], args=(bins,spec_total))
	return this_sum[0]  # second value is error



offset_factor = -1e-6
indexing_start = 100
xfrm_starting_index = 990

source_list         = []
cosine_bins_total   = []
cosine_values_total = []
erg_bins_total      = []
erg_values_total    = []
x_bins_total        = []
x_values_total      = []
y_bins_total        = []
y_values_total      = []
xfrm_bins_total		= []
xfrm_values_total	= []
xfrm_bins_total		= []
surface_rotation_xy	= []
surface_centers		= []
 
for i in range(1,len(sys.argv)):

    filename = sys.argv[i]
    print "Loading '"+filename+"' as a pickled object"
    f=open(filename,'r')
    d = cPickle.load(f)
    f.close()
    source_list.append(d)

# calculate total normalization factors
additive = 0.0
total_weight_per_nps_total = 0.0
for d in source_list:
	total_weight_per_nps_total = total_weight_per_nps_total + d['total_weight']/d['surface_nps']


# make the unrolled vector lists
for j in range(0,len(source_list)):

	d 					= source_list[j] 
	dist            	= d['dist']           
	E_bins          	= d['E_bins']         
	x_bins          	= d['x_bins']         
	y_bins          	= d['y_bins']         
	theta_bins      	= d['theta_bins']     
	phi_bins        	= d['phi_bins']       
	surface_plane   	= d['surface_plane']  
	surface_normal  	= d['surface_normal'] 
	surface_center  	= d['surface_center'] 
	surface_vec1    	= d['surface_vec1']   
	surface_vec2    	= d['surface_vec2']
	surface_normal_rot	= d['surface_normal_rot'] 
	surface_vec1_rot	= d['surface_vec1_rot']   
	surface_vec2_rot	= d['surface_vec2_rot']   
	xy_rotation_degrees	= d['xy_rotation_degrees']
	yz_rotation_degrees	= d['yz_rotation_degrees']
	surface_nps     	= d['surface_nps']    
	total_weight    	= d['total_weight']   
	total_tracks    	= d['total_tracks']   
	npstrack_ratio  	= d['npstrack_ratio'] 
	this_sc         	= d['this_sc']            
	histograms_curr		= d['histograms_curr']
	histograms_flux		= d['histograms_flux']
	histograms_wght		= d['histograms_wght']
	spec_res 			= d['spec_res']

	total_weight_per_nps = total_weight/surface_nps 
	print "nps on surface", surface_nps
	print "total weight on surface %5d = %6.5E"%(this_sc,total_weight_per_nps)
	print "fractional weight on surface %5d = %6.5E"%(this_sc,total_weight_per_nps/total_weight_per_nps_total)

	cosine_bins = numpy.cos(theta_bins)

	# xfrm (main index)
	for i in range(0,(len(cosine_bins)-1)):
		xfrm_bins_total.append(j+xfrm_starting_index)
		xfrm_values_total.append(dist[i][0]/total_weight_per_nps_total)  # ugh so confusing, this has already been divided by nps at this point!  dists are always nps, the total_weight is NOT normalized!

	surface_rotation_xy.append(numpy.arctan(surface_normal[1]/surface_normal[0])*180.0/numpy.pi)
	surface_centers.append(surface_center)

	# angular bin values (flat)
	for i in range(0,(len(cosine_bins)-1)):
		cosine_bins_total.append([cosine_bins[i+1],cosine_bins[i]])
		cosine_values_total.append([1.0])

	# x bins
	for i in range(0,(len(cosine_bins)-1)):
		if dist[i][0] > 0.0:
			additive = 0.0
		else:
			additive = 1e-30
		x_bins_total.append(  dist[i][1].bins)
		x_values_total.append(dist[i][1].values+additive)

	#y bins
	for i in range(0,(len(cosine_bins)-1)):
		if dist[i][0] > 0.0:
			additive = 0.0
		else:
			additive = 1e-30
		y_bins_total.append(  dist[i][2].bins)
		y_values_total.append(dist[i][2].values+additive)

	# erg
	for i in range(0,(len(cosine_bins)-1)):
		if dist[i][0] > 0.0:
			additive = 0.0
		else:
			additive = 1e-30
		erg_bins_total.append(  dist[i][3].bins)
		erg_values_total.append(dist[i][3].values+additive)

#
# write mcnp sdef
#
dist_lengths = (len(cosine_bins)-1)*len(source_list)
name='dist_data_combined_unrolled.sdef'
print "\nWriting MCNP SDEF to '"+name+"'..."
#if sphere:
#	pass
#else:
print "SDEF plane offset by % 3.2E...\n"%offset_factor
f=open(name,'w')
# write easy stuff
f.write('c\n')
f.write('c Combined and unrolled SDEF from ss2dist2.py, '+time.strftime("%d.%m.%Y, %H:%M")+'\n')
f.write('c\n')
f.write('sdef    par=n\n')
f.write('        axs=0 0 1\n')
f.write('        vec=1 0 0\n')
f.write('        tr=d1\n')
f.write('        dir=ftr=d2\n')
f.write('        erg=ftr=d3\n')
f.write('        x=0.0\n')
f.write('        y=ftr=d4\n')
f.write('        z=ftr=d5\n')
f.write('        wgt=%10.8E\n'%(total_weight_per_nps_total))
f.write('c \n')
f.write('c TRANSFORMS\n')
f.write('c \n')
for i in range(0,len(source_list)):
	f.write('*tr%d   % 6.7E  % 6.7E  % 6.7E\n'%(i+xfrm_starting_index,(1.0+offset_factor)*surface_centers[i][0],(1.0+offset_factor)*surface_centers[i][1],(1.0+offset_factor)*surface_centers[i][2]))
	f.write('        % 6.7E  % 6.7E  % 6.7E\n'%(   surface_rotation_xy[i],90-surface_rotation_xy[i],90))
	f.write('        % 6.7E  % 6.7E  % 6.7E\n'%(90+surface_rotation_xy[i],   surface_rotation_xy[i],90))
	f.write('        % 6.7E  % 6.7E  % 6.7E\n'%(90,90,0))
# write dist cards
f.write('c \n')
f.write('c POSITION TRANSFORM PROBABILITIES\n')
f.write('c \n')
make_independent_distribution_intlines(f,1,xfrm_bins_total,xfrm_values_total)
#
f.write('c \n')
f.write('c ANGULAR DISTRIBUTIONS\n')
f.write('c \n')
make_dependent_distribution(f,2,indexing_start+dist_lengths*0,cosine_bins_total,cosine_values_total)
#
f.write('c \n')
f.write('c ENERGY DISTRIBUTIONS\n')
f.write('c \n')
make_dependent_distribution(f,3,indexing_start+dist_lengths*1,erg_bins_total,erg_values_total)
#
f.write('c \n')
f.write('c Y\n')
f.write('c \n')
make_dependent_distribution(f,4,indexing_start+dist_lengths*2,x_bins_total,x_values_total)
#
f.write('c \n')
f.write('c Z\n')
f.write('c \n')
make_dependent_distribution(f,5,indexing_start+dist_lengths*3,y_bins_total,y_values_total)
#
f.write('c \n')
f.close()
print "\nDONE.\n"
