def plot(objects,ax=None,tal=False,obj=False,cos=False,seg=False,mul=False,td=False,options=False,ylim=False,xlim=False,color='b'):
	### plotting routines for inter-mctal plots
	import numpy, pylab
	import matplotlib.pyplot as plt
	import MCNPtools.mctal
	import MCNPtools._do_ratio

	### type check
	for o in objects:
		if isinstance(o,MCNPtools.mctal.mctal):
			pass
		else:
			print "Objects in list are not MCNPtools.mctal instances!  Aborting."
			return

	### TeX flag of first object
	if objects[0].tex:
		plt.rc('text', usetex=True)
		plt.rc('font', family='serif')
		plt.rc('font', size=16)

	### options
	if not options:
		plot_options=['lin','wavelength','err']
	else:
		plot_options=options[:]
		if 'ratio' in options:
			plot_options.remove('ratio')
			plot_options.append('ratio_mctal')
		if 'rel' in plot_options:
			if 'ratio_mctal' not in plot_options:
				plot_options.append('ratio_mctal')
	if 'wavelength' in plot_options:
		if 'ratio_mctal' in plot_options:
			leg_loc = 1
		else:
			leg_loc = 1
	else:
		leg_loc = 1

	### init axes if not passed one
	if ax:
		show = 0
	else:
		show = 1
		fig = plt.figure(figsize=(10,6))
		ax = fig.add_subplot(1,1,1)

	### deal with a non-specified tally
	if not tal:
		tal = [objects[0].tally_n[0]]

	### input logic and plotting, using methods
	if not obj and not cos and not seg and not mul and not td:
		if 'ratio_mctal' in plot_options:
			obj = range(objects[0].tallies[tal[0]].object_bins)
			seg = range(objects[0].tallies[tal[0]].segment_bins)
			cos = range(objects[0].tallies[tal[0]].cosine_bins)
			mul = range(objects[0].tallies[tal[0]].multiplier_bins)
			td  = range(objects[0].tallies[tal[0]].totalvsdirect_bins)
			MCNPtools._do_ratio._do_ratio(objects,ax=ax,tal=tal,obj=obj,seg=seg,mul=mul,cos=cos,td=td,ylim=ylim,xlim=xlim,color=color,options=plot_options)
		else:
			for this_mctal in objects:
				for t in tal:
					this_mctal.tallies[t].plot(ax=ax,all=True,options=plot_options)
	else:
		if not obj:
			obj = [0]
		if not cos:
			cos = [0]
		if not seg:
			seg = [0]
		if not mul:
			mul = [0]
		if not td:
			td  = [0]
		if 'ratio_mctal' in plot_options:
			MCNPtools._do_ratio._do_ratio(objects,ax=ax,tal=tal,obj=obj,seg=seg,mul=mul,cos=cos,td=td,ylim=ylim,xlim=xlim,options=plot_options,color=color)
		else:
			for this_mctal in objects:
				for t in tal:
					this_mctal.tallies[t].plot(ax=ax,obj=obj,seg=seg,mul=mul,cos=cos,t_or_d=td,ylim=ylim,xlim=xlim,color=color,options=plot_options,prepend_label='{title:s}\n{com:s}\n Tally {a:4d} :'.format(title=this_mctal.title.strip(),com=this_mctal.tallies[t].comment,a=t))

	### show
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles,labels,loc=leg_loc,prop={'size':12})
	ax.grid(True)
	if show:
		plt.show()