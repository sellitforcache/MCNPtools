#! /home/l_bergmann/anaconda/bin/python -W ignore
#
# ss2dist, the MCNP surface source to histogram distribution maker
# Ryan M. Bergmann, March 2015 
# ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

from pyne import mcnp
import pylab, numpy, sys, cPickle, progressbar
import matplotlib.pyplot as plt

filename = sys.argv[1]
phi_bin = int(sys.argv[2])
theta_bin = int(sys.argv[3])
E_bin = int(sys.argv[4])
obj_bin = 1

printflag = bool(1)
errorflag = bool(0)

if printflag:
	progress = progressbar.ProgressBar()
else:
	def progress(inp):
		return inp

if filename[-4:]=='wssa':
	typeflag = 1
elif filename[-4:]=='trks':
	typeflag = 2
else:
	typeflag = 0

### interpret file name
if printflag:
	print "\n============================\n"
	if typeflag == 1:
		print "Loading '"+filename+"' as a MCNP binary surface source"
	elif typeflag == 2:
		print "Loading '"+filename+"' as a pickled pyne.mcnp.SurfSrc object"
	else:
		print "Loading '"+filename+"' as a pickled numpy.array object"

### load data
if typeflag == 1:
	ss = mcnp.SurfSrc(filename)
	ss.read_header()
	ss.read_tracklist()
elif typeflag == 2:
	f=open(filename,'r')
	ss = cPickle.load(f)
	f.close()
else:
	f=open(filename,'r')
	dist_list = cPickle.load(f)
	f.close()

if printflag:
	print "Done."

### init
if typeflag:
	#  bin parameters
	E_bins   = numpy.array([0.0, 4e-9,  6e-9,    9e-9, 1.1e-8,   1.9e-8, 2.1e-8,  60])
	#x_bins   = numpy.linspace(-15,15,61)
	x_bins   = numpy.linspace(-2,2,2)
	y_bins   = numpy.linspace(-10,10,41)
	#theta_bins  = numpy.linspace(0,  numpy.pi,2)  
	theta_bins = numpy.array([0,5,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
	phi_bins = numpy.linspace(0,2*numpy.pi,2) 
	dist	 = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
	#  surface plane parameters
	surface_plane	= numpy.array([ 9.9862953E-01,  -5.2335956E-02,   0.0000000E+00,   4.4486150E+01])   # plane, GLOBAL coordinates
	surface_center  = numpy.array([42.44175502   ,  -40.17427813,     0.            ])   # global again
	surface_normal 	= numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]])  
	surface_vec1    = numpy.array([ 5.2335956E-02,   9.9862953E-01,  0.0])
	surface_vec2    = numpy.array([0.0,0.0,1.0])
else:
	dist	 		= dist_list[0]
	E_bins   		= dist_list[1]
	x_bins   		= dist_list[2]
	y_bins   		= dist_list[3]
	theta_bins  	= dist_list[4]
	phi_bins 		= dist_list[5]
	surface_plane	= dist_list[6]
	surface_center  = dist_list[7]
	surface_normal 	= dist_list[8]
	surface_vec1    = dist_list[9]
	surface_vec2    = dist_list[10]

### print some details
if printflag:
	print "\n============================\n"

	if typeflag == 1:
		print "Binning '"+filename+"' according to:\n"
	else:
		print "Binning in '"+filename+"' done according to:\n"

	print "Energy bin boundaries (MeV)\n",E_bins 
	print "    "
	print "Theta (polar) bin boundaries (degrees)\n", theta_bins*180.0/numpy.pi
	print "    "
	print "Phi (azimuthal) bin boundaries (degrees)\n", phi_bins*180.0/numpy.pi
	print "    "
	print "Y bin boundaries (cm)\n", y_bins
	print "    "
	print "X bin boundaries (cm)\n", x_bins
	print "    "

### check to make sure surface basis vectors are orthogonal
assert( numpy.abs(numpy.dot(surface_vec1,surface_vec2)  ) <= 1.e-8 )
assert( numpy.abs(numpy.dot(surface_vec1,surface_normal)) <= 1.e-8 )
assert( numpy.abs(numpy.dot(surface_vec2,surface_normal)) <= 1.e-8 )

### scan tracks
if typeflag:
	if printflag:
		print "\n============================\n"
		print "Binning tracks... "
	for i in progress(range(0,len(ss.tracklist))):
		
		### get track global position/direction
		track = ss.tracklist[i]
		vec = numpy.array([track.u,track.v,track.w])
		pos = numpy.array([track.x,track.y,track.z])
		this_E 	  = track.erg
		this_wgt  = track.wgt
		
		### transform vector to normal system
		this_vec = numpy.array([numpy.dot(surface_vec1,vec),numpy.dot(surface_vec2,vec),numpy.dot(surface_normal,vec)])
	
		### transform position to surface coordinates using basis vectors specified
		xfm_pos  = numpy.subtract(pos,surface_center)
		this_pos = numpy.array([numpy.dot(surface_vec1,xfm_pos),numpy.dot(surface_vec2,xfm_pos)])
	
		### calc angular values
		this_theta  = numpy.arccos(this_vec[2])
		this_phi = numpy.arctan2(this_vec[1],this_vec[0])
		if this_phi < 0.0:
			this_phi = 2.0*numpy.pi + this_phi
	
		### find the bins
		if (this_E > E_bins[0] and this_E < E_bins[-1]):
			E_dex 	=  numpy.nonzero(this_E      < E_bins  )[0][0]-1
		else:
			E_dex = sys.maxint
		if (this_pos[0] > x_bins[0] and this_pos[0] < x_bins[-1]):
			x_dex 	=  numpy.nonzero(this_pos[0] < x_bins  )[0][0]-1
		else:
			x_dex= sys.maxint
		if (this_pos[1] > y_bins[0] and this_pos[1] < y_bins[-1]):	
			y_dex 	=  numpy.nonzero(this_pos[1] < y_bins  )[0][0]-1
		else:
			y_dex= sys.maxint
		if (this_theta > theta_bins[0] and this_theta < theta_bins[-1]):
			theta_dex	=  numpy.nonzero(this_theta     < theta_bins )[0][0]-1
		else:
			theta_dex= sys.maxint
		if (this_phi > phi_bins[0] and this_phi < phi_bins[-1]):	
			phi_dex	=  numpy.nonzero(this_phi    < phi_bins)[0][0]-1
		else:
			phi_dex=sys.maxint
	
		### increment array
		if (E_dex < len(E_bins)-1) and (theta_dex < len(theta_bins)-1) and (phi_dex < len(phi_bins)-1) and (y_dex < len(y_bins)-1) and (x_dex < len(x_bins)-1) :
			dist[E_dex][theta_dex][phi_dex][y_dex][x_dex] = dist[E_dex][theta_dex][phi_dex][y_dex][x_dex] + this_wgt
			#print this_E," between ", E_bins[E_dex:E_dex+2]
		else:
			if (E_dex >= len(E_bins)-1 and printflag and errorflag): 
				print "E = %6.4E index %i is outside bin boundaries" % (this_E,E_dex,)
			if(theta_dex >= len(theta_bins)-1 and printflag and errorflag): 
				print "theta = %6.4E index %i is outside bin boundaries" % (this_theta,theta_dex)
			if(phi_dex >= len(phi_bins)-1 and printflag and errorflag): 
				print "phi = %6.4E index %i is outside bin boundaries" % (this_phi,phi_dex)
			if(y_dex >= len(y_bins)-1 and printflag and errorflag): 
				print "y = %6.4E index %i is outside bin boundaries" % (this_pos[1],y_dex)
			if(x_dex >= len(x_bins)-1 and printflag and errorflag):
				print "x = %6.4E index %i is outside bin boundaries" % (this_pos[0],x_dex)
	
	### normalize dist to nps:
	nps = ss.tracklist[-1].nps
	#nps = 2.0e7
	dist = dist / nps

	### dump array to file
	if printflag:
		print "\n============================\n"
		print "writing binned array to file 'dist'... "
	f = open('dist','wf')
	cPickle.dump([dist,E_bins,x_bins,y_bins,theta_bins,phi_bins,surface_plane,surface_center,surface_normal,surface_vec1,surface_vec2],f)
	f.flush()
	f.close()
	if printflag:
		print "Done."

#	if printflag:
#		print "\n============================\n"
#		print "writing binned array to file 'trks'... "
#	f = open('trks','wf')
#	cPickle.dump(ss,f)
#	f.flush()
#	f.close()
#	if printflag:
#		print "Done."

if printflag:
	print "\n============================\n"

if typeflag == 1:
	ss.close()

### plot stuff
#E_bin = 1
#theta_bin = 5
#phi_bin = 0

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)

f = plt.figure()
ax = f.add_subplot(111)
imgplot = ax.imshow(dist[E_bin][theta_bin][phi_bin][:][:],extent=[x_bins[0],x_bins[-1],y_bins[0],y_bins[-1]],origin='lower')

theta_deg = theta_bins[theta_bin:theta_bin+2]*180.0/numpy.pi
phi_deg = phi_bins[phi_bin:phi_bin+2]*180.0/numpy.pi
E_meV   = E_bins[E_bin:E_bin+2]*1.0e9

ax.set_ylabel(r'y (cm)')
ax.set_xlabel(r'x (cm)')
ax.set_title(r'Energies %4.2f - %4.2f meV \\ $\theta$ %4.2f - %4.2f $^{\circ}$, $\phi$ %4.2f - %4.2f $^{\circ}$' % (E_meV[0],E_meV[1],theta_deg[0],theta_deg[1],phi_deg[0],phi_deg[1]))
ax.grid()
cbar=pylab.colorbar(imgplot)
cbar.set_label(r"n p$^{-1}$")

ax.quiver([0.7*x_bins[-1],0.7*x_bins[-1]],[0.8*y_bins[0],0.8*y_bins[0]],[5,0],[0,5],color='r',width=.002)
ax.text(0.69*x_bins[-1],0.65*y_bins[0],'y',color='r',fontsize=10)
ax.text(0.81*x_bins[-1],0.81*y_bins[0],'x',color='r',fontsize=10)

pylab.show()
