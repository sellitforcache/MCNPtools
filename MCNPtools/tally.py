class Tally:
	### static mappings, shared by all
	###  MCNPX particle encodings
	particles={
		 1 : ['neutron'						, 'n' ],
		 5 : ['anti-neutron'				, 'q' ],
		 2 : ['photon'						, 'p' ],
		 3 : ['electron'					, 'e' ],
		 8 : ['positron'					, 'f' ],
		 4 : ['muon-' 						, '|' ],
		16 : ['muon+'				    	, '!' ],
		 6 : ['electron neutrino'			, 'u' ],
		17 : ['anti-electron neutrino'		, '<' ],
		 7 : ['muon neutrino'				, 'v' ],
		18 : ['anti muon neutrino'			, '>' ],
		 9 : ['proton'						, 'h' ],
		19 : ['anti-proton'					, 'g'],
		10 : ['lambda baryon'				, 'l' ],
		25 : ['anti lambda baryon'			, 'b' ],
		11 : ['positive sigma baryon'		, '+' ],
		26 : ['anti positive sigma baryon'	, '_' ],
		12 : ['negative sigma baryon'		, '-' ],
		27 : ['anti negative sigma baryon'	, '~' ],
		13 : ['cascade'						, 'x' ],
		28 : ['anti cascade'				, 'c' ],
		14 : ['negative cascade'			, 'y' ],
		29 : ['positive cascade'			, 'w' ],
		15 : ['omega baryon'				, 'o' ],
		30 : ['anti omega baryon'			, '@' ],
		20 : ['positive pion'				, '/'],
		35 : ['negative pion'				, '*'],
		21 : ['neutral pion'				, 'z'],
		22 : ['positive kaon'				, 'k'],
		36 : ['negative kaon'				, '?'],
		23 : ['kaon, short'					, '%'],
		24 : ['kaon, long'					, '^'],
		31 : ['deuteron'					, 'd'],
		32 : ['triton'						, 't'],
		33 : ['helion'						, 's'],
		34 : ['alpha'						, 'a'],
		37 : ['heavy ions'					, '#']}
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
	meshtally_units={
          1 : r' cm$^{-2}$ primary$^{-1}$',
          2 : r' ?',
	      4 : r' MeV cm$^{-3}$ primary$^{-1}$',
	      5 : r' cm$^{-2}$ primary$^{-1}$'}

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
		self.is_meshtal			= False

	def what_particles(self,flag='symbol'):
		### decode particle data to human-readable
		if self.particle_type>0:
			### shorthand list, can return directly
			ret_string = self.particles_shorthand[self.particle_type][0]
		else:
			### explicit list, collect results
			if flag == 'number':
				ret_string=[]
			else:
				ret_string=''
			for x in range(len(self.particle_list)):
				if self.particle_list[x] != 0:
					if flag == 'name':
						ret_string = ret_string + self.particles[(x+1)*self.particle_list[x]][0]   ### the multiplication is to switch the sign if anti-particle and then the dictionary will know!
					elif flag == 'symbol':
						ret_string = ret_string + self.particles[(x+1)*self.particle_list[x]][1]
					elif flag == 'number':
						ret_string.append((x+1)*self.particle_list[x])
					else:
						print "flag of ",flag,"is not valid!"
		return  ret_string


	def _hash(self,obj=0,td=0,user=0,seg=0,mul=0,cos=0):
		# update once multiplier and user are understood
		assert(obj  < self.object_bins)
		assert(seg  < self.segment_bins)
		assert(cos  < self.cosine_bins)
		assert(mul  < self.multiplier_bins)
		assert(td   < self.totalvsdirect_bins)
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


	def _make_steps(self,ax,bins_in,avg_in,values_in,options=['log'],color=None,label='',ylim=False):
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
				v1= 0
				v2=None
				v1s='0'
				v2s=''
				if len(coarsen_opts)==1:
					bin_red = 2
				elif len(coarsen_opts)==2:
					bin_red = coarsen_opts[1]
				else:
					bin_red = coarsen_opts[1]
					print "MULTIPLE = SIGNS IN COARSEN.  WHY?  ACCEPTING FIRST VALUE."
				#split again for slice options
				s_options = bin_red.split(',')
				if len(s_options)==1:
					bin_red = int(bin_red)
				else:
					bin_red = int(s_options[0])
					this_match = re.search('\[([0-9-]*):([0-9-]*)\]',s_options[1])
					if this_match:
						if len(this_match.group(1))>0:
							v1=int(this_match.group(1))
							v1s='%d'%v1
						if len(this_match.group(2))>0:
							v2=int(this_match.group(2))
							v2s='%d'%v2
						print "taking array slices of values and bins like [%s:%s]"%(v1s,v2s)
				if len(values[v1:v2])%bin_red==0:
					print "Reducing bins by factor of %d ..."%bin_red
					label = label + ' COMBINED %d BINS'%bin_red
					values,bins = self._coarsen(numpy.array(values[v1:v2]),numpy.array(bins[v1:v2]),bin_red=bin_red)
				else:
					print "DATA LENGHTH NOT EVENLY DIVISIBLE BY COARSEN FACTOR, IGNORING..."

		### despike data?  parse format
		for opt in options:
			res = re.match('despike',opt)
			if res:
				coarsen_opts = opt.split('=')
				if len(coarsen_opts)==1:
					factor = 2
				elif len(coarsen_opts)==2:
					factor = float(coarsen_opts[1])
				else:
					factor = float(coarsen_opts[1])
					print "MULTIPLE = SIGNS IN DESPIKE.  WHY?  ACCEPTING FIRST VALUE."
				print "data that is greater than %2.1E times neightboring bins replaced with neighboring bin average ..."%factor
				label = label + ' DESPIKE FACTOR %2.1E '%factor
				for i in range(0, len(values)):
					if i==0:
						avg=values[i+1]
					elif i==len(values)-1:
						avg=values[i-1]
					else:
						avg=(values[i-1]+values[i+1])/2.0
					if values[i]>=factor*avg:
						values[i]=avg

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

	def write_csv(self,filename,all=False,obj=[0],cos=[0],seg=[0],mul=[0],t_or_d=[0],options=[],prepend_label=False):
		import numpy as np
		import pylab as pl
		import matplotlib.pyplot as plt

		### I don't care that I'm overriding the built-in 'all' within this method

		### make consistency checks
		if 'lethargy' in options:
			if 'enormed' in options:
				pass
			else:
				options.append('enormed')

		### open file
		this_file = open(filename,'w')

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

		### go through selected objets and write them
		for o in plot_objects:
			for td in plot_t_or_d:
				for s in plot_segments:
					for m in plot_multipliers:
						for c in plot_cosines:
							### GET DATA
							dex  		= self._hash(obj=o,cos=c,seg=s,mul=m,td=td)
							tally 		= self.vals[dex]['data'][:-1]  # clip off totals from ends
							err 		= self.vals[dex]['err'][:-1]
							tally_total = self.vals[dex]['data'][-1]
							err_total 	= self.vals[dex]['err'][-1]
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

							### UNITS
							if self.name%10 == 1:
								units = 'n'
							elif self.name%10 ==2:
								units = 'n/cm2'
							elif self.name%10 ==4:
								units = 'n/cm2'
							elif self.name%10 ==5:
								units = 'n/cm2'
							elif self.name%10 ==6:
								units = 'MeV/g'
							else:
								print "Tally type %d not handled!!!!!"%(self.name%10)

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
									units = units + '/lethargy'
									tally_norm  = np.divide(tally,widths)
									tally_norm	= np.multiply(tally_norm,avg)
								else:
									tally_norm = np.divide(tally,widths)
									if 'wavelength' in options:
										units = units + '/AA'
									else:
										units = units + '/MeV'
							if 'sanormed' in options:   #  divide by solid angle bin width
								units = units + '/str'
								sa = 2.0*np.pi*(self.vals[dex]['cosine_bin'][1]-self.vals[dex]['cosine_bin'][0])
								tally_norm = np.divide(tally_norm,sa)

							### SCALE
							if 'mA' in options:
								units = units + '/mA'
								tally_norm = np.multiply(tally_norm,6.241e15)  # convert protons to milliAmpere*seconds
								tally_total = tally_total*6.241e15
							else:
								units = units + '/p'

							#### LABEL
							if prepend_label:
								label = prepend_label+r' obj %2d (%4d) seg %d cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1])
							else:
								label = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1])

							### WRITE
							this_file.write('\n\n'+label+'\n\n')
							if 'wavelength' in options:
								this_file.write("Bin Boundaries (AA),     ,   "+units+",          Rel. Err.\n")
							else:
								this_file.write("Bin Boundaries (MeV),    ,   "+units+",          Rel. Err.\n")
							for i in range(0,len(bins)-1):
								this_file.write("% 6.4E,  % 6.4E,  % 6.4E,  % 6.4E\n"%(bins[i],bins[i+1],tally_norm[i],err[i]))

							if self.name%10 == 1:
								units = 'n'
							elif self.name%10 ==2:
								units = 'n/cm2'
							elif self.name%10 ==4:
								units = 'n/cm2'
							elif self.name%10 ==5:
								units = 'n/cm2'
							elif self.name%10 ==6:
								units = 'MeV/g'
							if 'mA' in options:
								units = units + '/mA'
							else:
								units = units + '/p'
							this_file.write(    "TOTAL, "+units+", % 6.4E,  % 6.4E\n"%(tally_total,err_total))

		this_file.close()

	def write_sdef(self,filename,all=False,obj=0,cos=0,seg=0,mul=0):
		import numpy as np
		import pylab as pl
		import matplotlib.pyplot as plt

		### open file
		this_file = open(filename,'w')

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
			#plot_t_or_d		= t_or_d

		### GET DATA
		dex  		= self._hash(obj=obj,cos=cos,seg=seg,mul=mul)
		tally 		= self.vals[dex]['data'][:-1]  # clip off totals from ends
		err 		= self.vals[dex]['err'][:-1]
		tally_total = self.vals[dex]['data'][-1]
		err_total 	= self.vals[dex]['err'][-1]
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

		#
		# print mcnp cards, E dist only
		#
		if self.particle_type < 0:
			ptype = self.what_particles('symbol')
		else:
			ptype = self.particle_type
		dist_number = 1
		this_file.write("sdef   par=%s\n"%ptype)
		this_file.write("       axs=0 0 1\n")
		this_file.write("       erg=d%d\n"%dist_number)
		this_file.write("       x=0\n")
		this_file.write("       y=0\n")
		this_file.write("       z=0\n")
		this_file.write("       vec=1 0 0\n")
		this_file.write("       dir=1\n")
		this_file.write("c\n")
		this_file.write("c\n")
		string1 = "si%d H"%(dist_number)
		string2 = "sp%d  "%(dist_number)
		for i in range(0,len(tally)):
			string1 = string1 + (" % 6.4E"%(bins[i+1]))
			string2 = string2 + (" % 6.4E"%(tally[i]))
			l = len(string1.split('\n')[-1])
			if l>68:
				string1 = string1+"\n     "
				string2 = string2+"\n     "
		this_file.write(string1.rstrip()+"\n")
		this_file.write(string2.rstrip()+"\n")
		this_file.write("c\n")

		this_file.close()


	def plot_meshtal(self,all=False,ax=None,obj=[0],norm='log'):
		import matplotlib.pyplot as plt
		from matplotlib.colors import LogNorm

		last_integer = self.name % 10
		units = self.meshtally_units[last_integer]

		xgrid=self.objects[1]
		ygrid=self.objects[2]
		zgrid=self.objects[3]
		this_extent = [xgrid[0],xgrid[-1],ygrid[0],ygrid[-1]]

		z_dex = obj[0]

		data = self.vals[0][z_dex]['data']

		cax=ax.imshow(data,origin='lower',extent=this_extent,norm=LogNorm(),cmap=plt.get_cmap('nipy_spectral'),interpolation='nearest',aspect='auto')
		f1=ax.get_figure()
		cbar=f1.colorbar(cax)
		cbar.ax.set_ylabel(units)
		ax.grid(1)
		ax.set_xlabel(r'z (cm)')
		ax.set_ylabel(r'y (cm)')
		ax.set_title('Averaged over z=[ % 3.2E , % 3.2E ]'%(zgrid[z_dex],zgrid[z_dex+1]))
		ax.set_xlim([xgrid[0],xgrid[-1]])
		ax.set_ylim([ygrid[0],ygrid[-1]])


	def plot(self,all=False,ax=None,obj=[0],cos=[0],seg=[0],mul=[0],t_or_d=[0],color=None,options=[],label=False,prepend_label=False,ylim=False,xlim=False,renorm_to_sum=False,norm=1.0):
		import numpy as np
		import pylab as pl
		import matplotlib.pyplot as plt

		### I don't care that I'm overriding the built-in 'all' within this method

		### check if mesh tally
		if self.is_meshtal:
			self.plot_meshtal(all=all,ax=ax,obj=obj)
			return

		### make consistency checks
		if 'lethargy' in options:
			if 'enormed' in options:
				pass
			else:
				options.append('enormed')

		if 'wavelength' in options:
			leg_loc = 'best'
		else:
			leg_loc = 'best'

		### set TeX
		if self.tex:
			plt.rc('text', usetex=True)
			plt.rc('font', family='serif')
			plt.rc('font', size=16)

		### color scheme
		#plt.style.use('ggplot')

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
			plot_t_or_d		= range(self.totalvsdirect_bins)
		else:
			plot_objects	= obj
			plot_segments	= seg
			plot_cosines	= cos
			plot_multipliers= mul
			plot_t_or_d		= t_or_d

		total_string={}
		total_string[0]='TOTAL'
		total_string[1]='FLAGGED'

		### go through selected objets and plot them
		for o in plot_objects:
			for td in plot_t_or_d:
				for s in plot_segments:
					for m in plot_multipliers:
						for c in plot_cosines:
							### GET DATA
							dex  		= self._hash(obj=o,cos=c,seg=s,mul=m,td=td)
							tally 		= np.array(self.vals[dex]['data'][:-1])*norm  # clip off totals from ends, multiply by specified norm
							err 		=          self.vals[dex]['err'][:-1]
							t_or_d 		=          self.vals[dex]['t_or_d']
							cosine_bin	=          self.vals[dex]['cosine_bin']
							name		=          self.vals[dex]['object']
							if norm!=1.0:
								prepend_label = r'NORM=%3.2E'%norm
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
							if renorm_to_sum:
								tally_norm = tally_norm/np.sum(np.multiply(tally_norm,np.divide(widths,avg)))

							if not label and not prepend_label:
								plabel = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] %s' % (o,name,s,cosine_bin[0],cosine_bin[1],total_string[td])
							if label:
								plabel = label
							elif prepend_label and label:
								plabel = prepend_label+label
							elif prepend_label and not label:
								plabel = prepend_label+r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] %s' % (o,name,s,cosine_bin[0],cosine_bin[1],total_string[td])

							if 'ratio_mctal' in options:
								total 		= self.vals[dex]['data'][-1]
								total_err 	= self.vals[dex]['err'][-1]
								plabel = plabel + '\n Total = {total:5.4f} +- {err:5.4f}'.format(total=total,err=total_err)

							### PLOT
							if 'ratio_cos' in options:
								if c == plot_cosines[0]:
									a     = tally_norm[:]
									a_err = err[:]
									a_bin = cosine_bin[:]
								else:
									if prepend_label:
										plabel = prepend_label+r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] / cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									else:
										plabel = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] / cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									self._make_steps(ax,bins,avg,np.divide(tally_norm,a),color=color,options=options,label=plabel)
							if 'diff_cos' in options:
								if c == plot_cosines[0]:
									a     = tally_norm[:]
									a_err = err[:]
									a_bin = cosine_bin[:]
								else:
									if prepend_label:
										plabel = prepend_label+r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] - cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									else:
										plabel = r'Obj %2d (%4d) seg %d cos [%4.2e, %4.2e] - cos [%4.2e, %4.2e]' % (o,name,s,cosine_bin[0],cosine_bin[1],a_bin[0],a_bin[1])
									self._make_steps(ax,bins,avg,np.subtract(tally_norm,a),color=color,options=options,label=plabel)
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
									plabel = prepend_label+r'Obj %2d (%4d) seg %d cos [%5.4f - %5.4f]' % (o,name,s,bin_min_d,bin_max_d)
								else:
									plabel = r'Obj %2d (%4d) seg %d cos [%5.4f, %5.4f]' % (o,name,s,bin_min_d,bin_max_d)
								self._make_steps(ax,bins,avg,this_sum,color=color,options=options,label=plabel)
								#if 'err' in options:
								#	ax.errorbar(avg,values,yerr=numpy.multiply(numpy.array(err),numpy.array(values)),linestyle='None',alpha=1.0,color='r')
							else:
								self._make_steps(ax,bins,avg,tally_norm,color=color,options=options,label=plabel)
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
		if 'wavelength' in options:
			label = r'$\Phi(\lambda)$ (' + label
		elif 'lethargy' in options:
			label = r'$\Phi(u)$ (' + label
		else:
			label = r'$\Phi(E)$ (' + label

		if 'mA' in options:
			units = label.replace(r'p$^{-1}$',r'mAs$^{-1}$')

		if 'enormed' in options:
			if 'wavelength' in options:
				label =  label + r' \AA$^{-1}$'
			elif 'lethargy' in options:
				label = label + r' $u^{-1}$'
			else:
				label = label + r' MeV$^{-1}$'

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
		import numpy as np
		# calculate based on binning
		if type(self.objects[0])==type([]):
			self.is_meshtal=True
			total_bins = self.object_bins
			# de-interlace the errors
			vals = self.vals[0::2]
			errs = self.vals[1::2]
			self.vals = []
			# make containers for each energy bin
			e_bins=max(1,len(self.objects[0])-1)
			for e in range(0,e_bins):
				self.vals.append([])
			# split into xy plots
			n_xy_plots = total_bins / (len(self.objects[3])-1)
			x_bins = len(self.objects[1])-1
			y_bins = len(self.objects[2])-1
			for e in range(0,e_bins):
				for b in range(0,len(self.objects[3])-1):
					# get length, and reshape
					these_vals = {}
					these_vals['data']	= np.reshape(vals[b*n_xy_plots:(b+1)*n_xy_plots],(y_bins,x_bins))
					these_vals['err']	= np.reshape(errs[b*n_xy_plots:(b+1)*n_xy_plots],(y_bins,x_bins))
					self.vals[e].append(these_vals)
		else:
			total_bins = self.object_bins*(self.multiplier_bins*self.segment_bins*self.cosine_bins*self.totalvsdirect_bins)  ## update for user/multiplier

			# check based on e vec length
			total_bins_e = len(self.vals)/(2*(len(self.energies)+1))

			# check consistency (should be thick by now)
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
			# indexing only for segment and cosine bins now, add others once I understand what they mean...
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
									if self.cosine_bins > 1:
										these_vals['cosine_bin']	= [self.cosines[c]] # radiography
									else:
										these_vals['cosine_bin']	= [-1,1]   # regular pd
								these_vals['user_bin'] 		= self.user_bins       # replace once understood
								these_vals['data'] 			= subset[0::2]
								these_vals['err'] 			= subset[1::2]
								new_vals.append(these_vals)
								n = n+1
			self.vals = new_vals
