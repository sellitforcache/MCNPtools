class tally:
	### static mappings, shared by all
	###  MCNPX particle encodings
	particles={
		 1  : ['neutron'				, 'n' ],
		-1  : ['anti-neutron'			, '-n'],
		 2  : ['photon'					, 'p' ],
		 3  : ['electron'				, 'e' ],
		-3  : ['positron'				, '-e'],
		 4  : ['muon-' 					, '|' ],
		-4  : ['anti-muon-'				, '-|'],
		 5  : ['tau'					, '*' ],
		 6  : ['electron neutrino'		, 'u' ],
		-6  : ['anti-electron neutrino'	, '-u'],
		 7  : ['muon neutrino'			, 'v' ],
		 8  : ['tau neutrino'			, 'w' ],
		 9  : ['proton'					, 'h' ],
		-9  : ['anti-proton'			, '-h'],
		 10 : ['lambda0'				, 'l' ],
		 11 : ['sigma+'					, '+' ],
		 12 : ['sigma-'					, '-' ],
		 13 : ['cascade+'				, 'x' ],
		 14 : ['caccade-'				, 'y' ],
		 15 : ['omega-'					, 'o' ],
		 16 : ['lambda_c+'				, 'c' ],
		 17 : ['cascade_c+'				, '!' ],
		 18 : ['cascade_c0'				, '?' ],
		 19 : ['lambda_b0'				, '<' ],
		 20 : ['pion+'					, '/' ],
		-20 : ['pion-'					, '-/'],
		 21 : ['pion0'					, 'z' ],
		 22 : ['kaon+'					, 'k' ],
		-22 : ['kaon-'					, '-k'],
		 23 : ['K0 short'				, '%' ],
		 24 : ['K0 long'				, '^' ],
		 25 : ['D+'						, 'g' ],
		 26 : ['D0'						, '@' ],
		 27 : ['D_s+'					, 'f' ],
		 28 : ['B+'						, '>' ],
		 29 : ['B0'						, 'b' ],
		 30 : ['B_s0'					, 'q' ],
		 31 : ['deuteron'				, 'd' ],
		 32 : ['triton'					, 't' ],
		 33 : ['helium-3'				, 's' ],
		 34 : ['helium-4'				, 'a' ],
		 35 : ['heavy ions'				, '#' ]}
	particles_shorthand={
		  1 : ['neutron'					,'n ' ],
		  2 : ['photon'						,'p ' ],
		  3 : ['neutron, photon'			,'np' ], 
		  4 : ['electron'					,'e'  ],
		  5 : ['neutron, electron'			,'ne' ],
		  6 : ['photon, electron'			,'pe' ],
		  7 : ['neutron, photon, electron'	,'npe']}
	tally_units={
          1 : r'n p$^{-1}$',
          2 : r'n cm$^{-2}$ p$^{-1}$',
	      4 : r'n cm$^{-2}$ p$^{-1}$',
	      5 : r'n cm$^{-2}$ p$^{-1}$'}

	def __init__(self,verbose=False,tex=False):
		self.name 				= 0    # tally name number
		self.particle_type 		= 0    # i>0 particle type, i<0 i=number of particle type, list following
		self.detector_type		= 0    # j=type of detector tally (0=none)
		self.particle_list 		= []   # list of included particles
		self.comment 			= ''  
		self.object_bins 		= 0
		self.objects     		= []
		self.totalvsdirect_bins = 1
		self.user_bins 			= 0
		self.segment_bins 		= 0
		self.segments 			= []
		self.multiplier_bins 	= 0 
		self.multiplier_flag 	= True
		self.cosine_bins 		= 0
		self.cosines 			= []
		self.energy_bins 		= 0
		self.energies 			= []
		self.time_bins 			= 0
		self.times 				= []
		self.total_bins 		= 0
		self.vals 				= []
		self.tfc 				= [0,0,0,0,0,0,0,0,0]
		self.tfc_data 			= []
		self.verbose 			= verbose
		self.tex				= tex

	def what_particles(self):
		ret_string=''
		### decode particle data to human-readable
		if self.particle_type>0:
			### shorthand list, can return directly
			ret_string = self.particles_shorthand[self.particle_type][0]
		else:
			### explicit list, collect results
			for x in range(len(self.particle_list)):
				if self.particle_list[x] != 0:
					ret_string = ret_string + self.particles[(x+1)*self.particle_list[x]][0]   ### the multiplication is ti switch the sign if anti-particle and then the dictionary will know!
		return  ret_string


	def _hash(self,obj=0,td=0,user=0,seg=0,mul=0,cos=0):
		# update once multiplier and user are understood
		assert(obj  < self.object_bins)
		assert(seg  < self.segment_bins)
		assert(cos  < self.cosine_bins)
		assert(mul  < self.multiplier_bins)
		dex = obj*(self.segment_bins*self.cosine_bins*self.multiplier_bins*self.totalvsdirect_bins)+ td*(self.segment_bins*self.cosine_bins*self.multiplier_bins) +seg*(self.cosine_bins*self.multiplier_bins)+ mul*(self.cosine_bins) + cos
		return dex

	def _smooth(self,x,window_len=11,window='flat'):
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

	def _coarsen(self,values,bins,bin_red=2):
		import numpy
		v_out=[]
		b_out=[]
		for i in range(0,len(values)/bin_red):
			v = 0.0
			for j in range(0,bin_red):
				v = v + values[i*bin_red+j]
			v_out.append(v)
			b_out.append(bins[i*bin_red])
		b_out.append(bins[-1])
		return numpy.array(v_out),numpy.array(b_out)


	def _make_steps(self,ax,bins_in,avg_in,values_in,options=['log'],color='b',label='',ylim=False):
		import numpy, re
		assert(len(bins_in)==len(values_in)+1)

		### make copies
		bins=bins_in[:]
		values=values_in[:]
		avg=avg_in[:]
		#err=err_in[:]

		### smooth data?  parse format
		for opt in options:
			res = re.match('smooth',opt)
			if res:
				smooth_opts = opt.split('=')
				if len(smooth_opts)==1:
					wlen = 7
				elif len(smooth_opts)==2:
					wlen = int(smooth_opts[1])
				else:
					wlen = int(smooth_opts[1])
					print "MULTIPLE = SIGNS IN SMOOTH.  WHY?  ACCEPTING FIRST VALUE."
				if wlen%2==0:
					print "WINDOW LENGTH EVEN, ADDING 1..."
					wlen = wlen + 1
				print "smoothing %d bins..."%wlen
				label = label + ' SMOOTHED %d BINS'%wlen
				values = self._smooth(numpy.array(values),window_len=wlen)
				values = values[(wlen-1)/2:-(wlen-1)/2]   # trim to original length

		### coarsen data?  parse format
		for opt in options:
			res = re.match('coarsen',opt)
			if res:
				coarsen_opts = opt.split('=')
				if len(coarsen_opts)==1:
					bin_red = 2
				elif len(coarsen_opts)==2:
					bin_red = int(coarsen_opts[1])
				else:
					bin_red = int(coarsen_opts[1])
					print "MULTIPLE = SIGNS IN SMOOTH.  WHY?  ACCEPTING FIRST VALUE."
				if len(values)%bin_red==0:
					print "Reducing bins by factor of %d ..."%bin_red
					label = label + ' COMBINED %d BINS'%bin_red
					values,bins = self._coarsen(numpy.array(values),numpy.array(bins),bin_red=bin_red)
				else:
					print "DATA LENGHTH NOT EVENLY DIVISIBLE BY COARSEN FACTOR, IGNORING..."

		### make rectangles
		x=[]
		y=[]
		x.append(bins[0])
		y.append(0.0)
		for n in range(len(values)):
			x.append(bins[n])
			x.append(bins[n+1])
			y.append(values[n])
			y.append(values[n])
		x.append(bins[len(values)])
		y.append(0.0)

		### plot with correct scale
		if 'lin' in options:
			if 'logy' in options:
				ax.semilogy(x,y,color=color,label=label)
			else:
				ax.plot(x,y,color=color,label=label)
		else:   #default to log if lin not present
			if 'logy' in options:
				ax.loglog(x,y,color=color,label=label)
			else:
				ax.semilogx(x,y,color=color,label=label)


	def plot(self,all=False,ax=None,obj=[0],cos=[0],seg=[0],mul=[0],t_or_d=[0],color=None,options=[],prepend_label=False,ylim=False,xlim=False):
		import numpy as np
		import pylab as pl
		import matplotlib.pyplot as plt

		### I don't care the I'm overriding the built-in 'all' within this method

		### make consistency checks
		if 'lethargy' in options:
			if 'enormed' in options:
				pass
			else:
				options.append('enormed')

		if 'wavelength' in options:
			leg_loc = 1
		else:
			leg_loc = 1
		
		### set TeX
		if self.tex:
			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')
			plt.rc('font', size=16)

		### init axes if not passed one
		if ax:
			show = False
		else:
			show = True
			fig = plt.figure(figsize=(10,6))
			ax  = fig.add_subplot(1,1,1)

		### deal with data to be plotted
		if all:
			plot_objects	= range(self.object_bins)
			plot_segments	= range(self.segment_bins)
			plot_cosines	= range(self.cosine_bins)
			plot_multipliers= range(self.multiplier_bins)
			plot_t_or_d		= [0]
		else:
			plot_objects	= obj
			plot_segments	= seg
			plot_cosines	= cos
			plot_multipliers= mul
			plot_t_or_d		= t_or_d

		### go through selected objets and plot them
		for o in plot_objects:
			for td in plot_t_or_d:
				for s in plot_segments:
					for m in plot_multipliers:
						for c in plot_cosines:
							### GET DATA
							dex  		= self._hash(obj=o,cos=c,seg=s,mul=m,td=td)
							tally 		= self.vals[dex]['data'][:-1]  # clip off totals from ends
							err 		= self.vals[dex]['err'][:-1]
							t_or_d 		= self.vals[dex]['t_or_d']
							cosine_bin	= self.vals[dex]['cosine_bin']
							name		= self.vals[dex]['object']
							if len(tally) < 2:
								print "tally has length <=1, aborting."
								if show:
									pl.close(fig)
								return
							bins 		= self.energies[:-1]
							widths 	 	= np.diff(bins)
							avg 		= np.divide(np.array(bins[:-1])+np.array(bins[1:]),2.0)

							### MODIFY DATA
							tally_norm = tally
							if 'wavelength' in options:
								bins 	= np.divide(0.286014369,np.sqrt(np.array(bins)*1.0e6))
								widths 	= -np.diff(bins)
								avg 	= np.divide(np.array(bins[:-1])+np.array(bins[1:]),2.0)
								#err     = err[::-1]
								#tally_norm = tally_norm[::-1]
							else:
								widths 	= np.diff(bins)
								avg 	= np.divide(np.array(bins[:-1])+np.array(bins[1:]),2.0)

							### NORM
							if 'enormed' in options:   # divide by energy/wavelength bin width
								if 'lethargy' in options:   # defaults to being normed for lethargy
									tally_norm  = np.divide(tally,widths)
									tally_norm	= np.multiply(tally_norm,avg)
								else:
									tally_norm = np.divide(tally,widths)
							if 'sanormed' in options:   #  divide by solid angle bin width
								sa = 2.0*np.pi*(self.vals[dex]['cosine_bin'][1]-self.vals[dex]['cosine_bin'][0])
								tally_norm = np.divide(tally_norm,sa)

							### SCALE 
							if 'mA' in options: 
								if 'ratio_mctal' in options:
									print "renormalizing to mA invalid for ratios, ignoring"
								else:
									tally_norm = np.multiply(tally_norm,6.241e15)  # convert protons to milliAmpere*seconds


							if prepend_label:
								label = prepend_label+r' obj %2d (%4d) seg %d cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1])
							else:
								label = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1])
	
							if 'ratio_mctal' in options:
								total 		= self.vals[dex]['data'][-1]
								total_err 	= self.vals[dex]['err'][-1]
								label = label + '\n Total = {total:5.4f} +- {err:5.4f}'.format(total=total,err=total_err)

							### PLOT
							if 'ratio_cos' in options:
								if c == plot_cosines[0]:
									a     = tally_norm[:]
									a_err = err[:]
									a_bin = cosine_bin[:]
								else:
									if prepend_label:
										label = prepend_label+r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] / cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									else:
										label = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] / cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									self._make_steps(ax,bins,avg,np.divide(tally_norm,a),color=color,options=options,label=label)
							if 'diff_cos' in options:
								if c == plot_cosines[0]:
									a     = tally_norm[:]
									a_err = err[:]
									a_bin = cosine_bin[:]
								else:
									if prepend_label:
										label = prepend_label+r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] - cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									else:
										label = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] - cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									self._make_steps(ax,bins,avg,np.subtract(tally_norm,a),color=color,options=options,label=label)
							if 'sum_cos' in options:
								if c == plot_cosines[0]:
									this_sum = tally_norm[:]
									a_err    = err[:]
									bin_min  = cosine_bin[0]
									bin_max  = cosine_bin[1]
								else:
									this_sum = np.add(tally_norm,this_sum)
									bin_min  = np.min([bin_min,cosine_bin[0]])
									bin_max  = np.max([bin_max,cosine_bin[1]])
								if 'degrees' in options:
									bin_min_d = np.arccos(bin_min)*180.0/np.pi
									bin_max_d = np.arccos(bin_max)*180.0/np.pi
								else:
									bin_min_d = bin_min
									bin_max_d = bin_max
								if prepend_label:
									label = prepend_label+r'Obj %2d (%4d) seg %d cos [%5.4f - %5.4f]' % (o,name,s,bin_min_d,bin_max_d)
								else:
									label = r'Obj %2d (%4d) seg %d cos [%5.4f, %5.4f]' % (o,name,s,bin_min_d,bin_max_d)
								self._make_steps(ax,bins,avg,this_sum,np.add(err,a_err),color=color,options=options,label=label)
								#if 'err' in options:
								#	ax.errorbar(avg,values,yerr=numpy.multiply(numpy.array(err),numpy.array(values)),alpha=0.0,color='r')
							else:
								self._make_steps(ax,bins,avg,tally_norm,color=color,options=options,label=label)
								if 'err' in options:
									ax.errorbar(avg,tally_norm,yerr=np.multiply(np.array(err),np.array(tally_norm)),linestyle='None',alpha=1.0,color='r')		

		### labels
		if 'wavelength' in options:
			if self.tex:
				ax.set_xlabel(r'Wavelength (\AA)')
			else:
				ax.set_xlabel('Wavelength (A)')
		else:
			if self.tex:
				ax.set_xlabel(r'Energy (MeV)')
			else:
				ax.set_xlabel('Energy (MeV)')

		### limits
		if ylim:
			ax.set_ylim(ylim)
		if xlim:
			ax.set_xlim(xlim)


		### labeling
		### get units
		last_integer = self.name % 10
		units = self.tally_units[last_integer]
		label = units
		if 'mA' in options:
			units = label.replace(r'p$^{-1}$',r'mAs$^{-1}$')
		if 'enormed' in options:
			if 'wavelength' in options:
				label = r'$\Phi(\lambda)$ (' + label + r' \AA$^{-1}$'
			elif 'lethargy' in options:
				label = r'$\Phi(u)$ (' + label + r' $u^{-1}$'
			else:
				label = r'$\Phi(E)$ (' + label + r' MeV$^{-1}$'
		if 'sanormed' in options:
			label = label + r'$\Omega^{-1}$'

		ax.set_ylabel(label+r')')

		### title legend grid, show if self-made
		if show:
			ax.set_title(r'Tally %d: %s'% (self.name,self.what_particles())+'\n'+r'%s'%self.comment)
			handles, labels = ax.get_legend_handles_labels()
			ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
			ax.grid(True)
			pl.show()


	def _process_vals(self):
		# calculate based on binning
		total_bins = self.object_bins*(self.multiplier_bins*self.segment_bins*self.cosine_bins*self.totalvsdirect_bins)  ## update for user/multiplier

		# check based on e vec length
		total_bins_e = len(self.vals)/(2*(len(self.energies)+1))
		
		# check consistency (should be thick by now)
		#print total_bins, total_bins_e
		#print self.energies
		assert(total_bins == total_bins_e)
		self.total_bins = total_bins
		if self.verbose:
			print "...... %d non-energy bins in tally" % (self.total_bins)

		# make full vector of cosine edges if not a point detector
		if self.cosine_bins==1:
				self.cosines=[-1.0,1.0]
		if (self.name % 10) != 5:
			self.cosines.insert(0,-1.0)

		# make ful vector of energy edges
		self.energies.insert(0,0.0)
		self.energies.append('total')
		
		# bag and tag em
		# indexing only for segment and cosine bins now, add others once I understand what they mean
		new_vals = []
		n = 0
		num_seg=self.segment_bins	
		num_cos=self.cosine_bins
		num_obj=self.object_bins
		num_mul=self.multiplier_bins
		num_td =self.totalvsdirect_bins

		for o in range(num_obj):
			for td in range(num_td):
				for s in range(num_seg):
					for m in range(num_mul):
						for c in range(num_cos):
							if self.verbose:
								if self.multiplier_flag:
									print "...... parsing object %2d (%4d) segment %2d multiplier %2d cosine bin %2d " % (o,self.objects[o],s,m,c)
								else:
									print "...... parsing object %2d (%4d) segment %2d cosine bin %2d " % (o,self.objects[o],s,c)
							these_vals 					= {}
							subset 						= self.vals[n*(self.energy_bins*2):(n+1)*(self.energy_bins*2)]
							these_vals['object']		= self.objects[o]
							if self.multiplier_flag:
								these_vals['multiplier']= m
							else:
								these_vals['multiplier']= False
							these_vals['segment'] 		= s
							these_vals['t_or_d'] 		= td
							if (self.name % 10) != 5:
								if c == len(self.cosines)-1:  #  only happens when there is a total bin
									these_vals['cosine_bin']	= [-1,1]
								else:
									these_vals['cosine_bin']	= [self.cosines[c],self.cosines[c+1]]
							else:
								these_vals['cosine_bin']	= [self.cosines[c]]
							these_vals['user_bin'] 		= self.user_bins       # replace once understood
							these_vals['data'] 			= subset[0::2]
							these_vals['err'] 			= subset[1::2]
							new_vals.append(these_vals)
							n = n+1
		self.vals = new_vals 

