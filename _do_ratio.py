def _do_ratio(objects,ax=False,tal=False,obj=False,seg=False,mul=False,cos=False,td=False,options=False,ylim=False,xlim=False):
	### internal function to make a new mctal object with ratio values and plot it on ax
	import numpy
	import MCNPtools.tally
	import MCNPtools.mctal

	### input check
	if not ax or not tal or not obj or not seg or not mul or not cos or not options:
		print "INPUT ERROR IN _do_ratio()!"
		return
	if 'normed' in options:
		print "Norming is invalid for ratios, ignored."
		options.remove('normed')
	if 'lethargy' in options:
		print "Lethargy is invalid for ratios, ignored."
		options.remove('lethargy')


	### set first title string
	title = 'a = {a:s}'.format(a=objects[0].title.strip())
	letter=['a','b','c','d','e','f','g','h','i']


	### do the ratios
	for o_in in range(len(objects)-1):

		### make mctal object
		dummy 			= MCNPtools.mctal.mctal(tex=objects[0].tex)
		dummy.title  	= objects[o_in+1].title
		#assert( set(objects[0].tally_n)	== set(objects[1].tally_n))
		dummy.ntal 		= len(tal)
	
		### insert new vector into empty mctal, copy necessary values
		for t in tal:
			### make tally for ratios
			#dummy.tally_n.append(objects[0].tally_n[t])
			dummy.tallies[t]  					= MCNPtools.tally.tally(tex=dummy.tex)
			dummy.tallies[t].comment 			= objects[0].tallies[t].comment
			dummy.tallies[t].name	 			= objects[0].tallies[t].name
			dummy.tallies[t].object_bins		= len(obj)
			dummy.tallies[t].segment_bins		= len(seg)
			dummy.tallies[t].cosine_bins		= len(cos)
			dummy.tallies[t].multiplier_bins	= len(mul)
			dummy.tallies[t].totalvsdirect_bins	= len(td)
			### check lengths for consistency:
			assert( set(objects[0].tallies[t].objects)  	== set(objects[o_in+1].tallies[t].objects))
			assert( set(objects[0].tallies[t].cosines) 		== set(objects[o_in+1].tallies[t].cosines))	
			assert( set(objects[0].tallies[t].energies) 	== set(objects[o_in+1].tallies[t].energies))
			### and copy energies now
			dummy.tallies[t].energies = objects[0].tallies[t].energies[:]
			### add to name vectors
			# print o0,o,objects[0].tallies[t].objects,dummy.tallies[t].objects
			# dummy.tallies[t].objects.append(objects[0].tallies[t].objects[o])
			# dummy.tallies[t].cosines.append(objects[0].tallies[t].cosines[c])
	
	
			o0 = 0
			for o in obj:
				t0 = 0
				for t_or_d in td:
					s0 = 0
					for s in seg:
						m0 = 0
						for m in mul:
							c0 = 0
							for c in cos:
								### check indexing, that order is consistent new tally object
								dex0 = dummy.tallies[t]._hash(obj=o0,seg=s0,mul=m0,cos=c0,td=t0)
								assert(dex0 == len(dummy.tallies[t].vals)) 
		
								### get values ratio
								dex 	= objects[0].tallies[t]._hash(obj=o,seg=s,mul=m,cos=c,td=t_or_d)
								a 		= objects[0].tallies[t].vals[dex]['data'][:]
								b 		= objects[o_in+1].tallies[t].vals[dex]['data'][:]
								a_err	= objects[0].tallies[t].vals[dex]['err'][:]
								b_err	= objects[o_in+1].tallies[t].vals[dex]['err'][:]
		
								### copy in data
								these_vals = {}
								if 'rel' in options:
									these_vals['data'] 		= numpy.subtract(numpy.divide(numpy.array(b),numpy.array(a)),1.0)
								else:
									these_vals['data'] 		= numpy.divide(numpy.array(b),numpy.array(a))
								these_vals['err'] 			= numpy.add(numpy.array(a_err),numpy.array(b_err))  # rel err of quotient is just the sum or errors?!
								these_vals['object']		= objects[0].tallies[t].vals[dex]['object']
								these_vals['multiplier']	= objects[0].tallies[t].vals[dex]['multiplier']
								these_vals['segment'] 		= objects[0].tallies[t].vals[dex]['segment']
								these_vals['cosine_bin']	= objects[0].tallies[t].vals[dex]['cosine_bin'][:]
								these_vals['user_bin'] 		= objects[0].tallies[t].vals[dex]['user_bin']
								these_vals['t_or_d'] 		= objects[0].tallies[t].vals[dex]['t_or_d']
								dummy.tallies[t].vals.append(these_vals)
								c0 = c0 + 1
							m0 = m0 +1
						s0 = s0 + 1
					t0 = t0 + 1
				o0 = o0 + 1
	
		### finally plot the sucker
		for t in tal:
			labelstr = '{a1:s} : {com:s}\n Tally {t:4d} :'.format(a1=letter[o_in+1],com=dummy.tallies[t].comment,t=t)
			dummy.tallies[t].plot(all=True,ax=ax,options=options,ylim=ylim,xlim=xlim,prepend_label=labelstr)

		### append to title string
		title = title + '\n {a:s} = {b:s}'.format(a=letter[o_in+1],b=objects[o_in+1].title.strip())

	### slight differences
	if 'rel' in options:
		ax.set_ylabel('Rel. Diff. ( ([x]-a)/a) ')
	else:
		ax.set_ylabel('Ratio ([x]/a)')
	ax.set_title(title)

