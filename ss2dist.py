#! /usr/local/bin/python 
# /home/l_bergmann/anaconda/bin/python -W ignore
#
# ss2dist, the MCNP surface source to histogram distribution maker
# Ryan M. Bergmann, March 2015 
# ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

from pyne import mcnp
import math
import pylab, numpy, sys, cPickle, progressbar, copy, time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib import gridspec
from MCNPtools import to_energy
from MCNPtools import to_temperature
from MCNPtools import to_wavelength
from scipy.integrate import quad
from matplotlib.colors import LogNorm


class SourceSurf(object):
    def __init__(self):
        pass

class TrackData(object):
    def __init__(self):
        pass

class SurfSrc(mcnp.SurfSrc):
    def __init__(self, filename, mode="rb"):
        super(SurfSrc, self).__init__(filename, mode)
    def __str__(self):
        return self.print_header()
    def print_header(self):
        """Returns contents of SurfSrc's header as an informative string.

        Returns
        -------
        header_string : str
            A line-by-line listing of the contents of the SurfSrc's header.

        """
        header_string = "Code: {0} (version: {1}) [{2}]\n".format(
            self.kod, self.ver, self.loddat)
        header_string += "Problem info: ({0}) {1}\n{2}\n".format(
            self.idtm, self.probid, self.aid)
        header_string += "Showing dump #{0}\n".format(self.knod)
        header_string += (
            "{0} histories, {1} tracks, {2} record size, "
            "{3} surfaces, {4} histories\n").format(
            self.np1, self.nrss, self.ncrd,
            self.njsw, self.niss)
        header_string += (
            "{0} cells, source particle: {1},"
            " macrobody facet flag: {2}\n").format(
            self.niwr, self.mipts, self.kjaq)
        for i in self.surflist:
            header_string += (
                "Surface {0}: facet {1},"
                " type {2} with {3} parameters: (").format(
                i.id, i.facet_id, i.type, i.num_params)
            if i.num_params > 1:
                for j in i.surf_params:
                    header_string += " {0}".format(j)
            else:
                header_string += " {0}".format(i.surf_params)
            header_string += ")\n"
        header_string += "Summary Table: " + str(self.summary_table)

        return header_string
    def next_track(self):
        """Reads in track records for individual particles."""
        track_data = TrackData()
        track_info = self.get_fortran_record()
        track_data.record = track_info.get_double(abs(self.ncrd))
        track_data.nps = track_data.record[0]
        track_data.bitarray = track_data.record[1]
        track_data.wgt = track_data.record[2]
        track_data.erg = track_data.record[3]
        track_data.tme = track_data.record[4]
        track_data.x   = track_data.record[5]
        track_data.y   = track_data.record[6]
        track_data.z   = track_data.record[7]
        track_data.u   = track_data.record[8]
        track_data.v   = track_data.record[9]
        track_data.cs  = track_data.record[10]
        if ((track_data.u*track_data.u+track_data.v*track_data.v)<1.0):
            track_data.w   = math.copysign(
                math.sqrt(1 - track_data.u*track_data.u -
                          track_data.v*track_data.v), track_data.bitarray)
        else:
            track_data.w = 0.0
        return track_data
    def read_header(self):
        """Read in the header block data. This block comprises 4 fortran
        records which we refer to as: header, table1, table2, summary.
        """
        # read header record
        header = self.get_fortran_record()

        # interpret header
        self.kod = header.get_string(8)[0]  # code identifier
        if 'SF_00001' not in self.kod:
            self.ver = header.get_string(5)[0]  # code version identifier
            if '2.6.0' in self.ver:
                self.loddat = header.get_string(28)[0]  # code version date
                self.idtm = header.get_string(19)[0]    # current date and time
                self.probid = header.get_string(19)[0]  # problem id string
                self.aid = header.get_string(80)[0]     # title card of initial run
                self.knod = header.get_int()[0]        # dump number
            elif '2.7.0' in self.ver:
                self.loddat = header.get_string(28)[0]  # code version date
                self.idtm = header.get_string(19)[0]    # current date and time
                self.probid = header.get_string(19)[0]  # problem id string
                self.aid = header.get_string(80)[0]     # title card of initial run
                self.knod = header.get_long()[0]        # dump number
            elif '5    ' in self.ver:
                self.loddat = header.get_string(8)[0]  # code version date
                self.idtm = header.get_string(19)[0]    # current date and time
                self.probid = header.get_string(19)[0]  # problem id string
                self.aid = header.get_string(80)[0]     # title card of initial run
                self.knod = header.get_long()[0]        # dump number
            else:
                raise NotImplementedError("MCNP5/X Version:" +
                    self.ver.rstrip() + " not supported")

            # read table 1 record; various counts and sizes
            tablelengths = self.get_fortran_record()

            if '2.7.0' in self.ver:
            	self.np1  = tablelengths.get_long()[0]       # hist used to gen.source
            	self.nrss = tablelengths.get_long()[0]      # tracks writ. to surf.src
            	self.ncrd = tablelengths.get_long()[0]      # histories to surf.src
            	self.njsw = tablelengths.get_long()[0]      # number of surfaces
            	self.niss = tablelengths.get_long()[0]      # histories to surf.src
                #print self.np1, self.nrss, self.ncrd, self.njsw, self.niss
            	self.table1extra = list()
            	while tablelengths.num_bytes > tablelengths.pos:
            	    self.table1extra += tablelengths.get_int()	
            else:
            	# interpret table lengths
            	if '2.6.0' in self.ver:
            	    self.np1 = tablelengths.get_int()[0]    # hist used to gen. src
            	    self.nrss = tablelengths.get_int()[0]   # #tracks to surf src
            	else:
            	    self.np1 = tablelengths.get_long()[0]   # hist used to gen. src
            	    self.nrss = tablelengths.get_long()[0]  # #tracks to surf src
            	self.ncrd = tablelengths.get_int()[0]  # #values in surf src record
            	                                       # 6 for a spherical source
            	                                       # 11 otherwise
            	self.njsw = tablelengths.get_int()[0]  # number of surfaces
            	self.niss = tablelengths.get_int()[0]  # #histories to surf src
            	self.table1extra = list()
            	while tablelengths.num_bytes > tablelengths.pos:
            	    self.table1extra += tablelengths.get_int()
        if 'SF_00001' in self.kod:
            header = self.get_fortran_record()
            self.ver = header.get_string(12)[0]     # code version identifier
            self.loddat = header.get_string(9)[0]   # code version date
            self.idtm = header.get_string(19)[0]    # current date and time
            self.probid = header.get_string(19)[0]  # problem id string
            self.aid = header.get_string(80)[0]     # title card of initial run
            self.knod = header.get_int()[0]         # dump number
            # read table 1 record; various counts and sizes
            tablelengths = self.get_fortran_record()
            # interpret table lengths
            self.np1 = tablelengths.get_int()[0]     # hist used to gen.source
            if self.np1 > 0:
            	self.np1 = self.np1 * -1
            self.notsure0 = tablelengths.get_int()[0]  # vals in surf src rec.
            self.nrss = tablelengths.get_int()[0]    # tracks writ. to surf.src
            self.notsure1 = tablelengths.get_int()[0]  # number of surfaces
            self.ncrd = tablelengths.get_int()[0]      # histories to surf.src
            self.njsw = tablelengths.get_int()[0]      # number of surfaces
            self.niss = tablelengths.get_int()[0]      # histories to surf.src
            self.table1extra = list()
            while tablelengths.num_bytes > tablelengths.pos:
                self.table1extra += tablelengths.get_int()
        if self.np1 < 0:
            # read table 2 record; more size info
            tablelengths = self.get_fortran_record()
            self.table2record = copy.deepcopy(tablelengths)  # copy entire record as is since values aren't changed
            self.niwr  = tablelengths.get_int()[0]   # #cells in surf.src card
            self.mipts = tablelengths.get_int()[0]   # source particle type
            self.kjaq  = tablelengths.get_int()[0]   # macrobody facet flag
            self.table2extra = list()
            while tablelengths.num_bytes > tablelengths.pos:
                self.table2extra += tablelengths.get_int()
        else:
            pass
        # Since np1 can be negative, preserve the actual np1 value while
        # taking the absolute value so that np1 can be used mathematically
        self.orignp1 = self.np1
        self.np1 = abs(self.np1)
        # get info for each surface
        self.surflist = list()
        self.surfrecordlist = list()
        if '2.7.0' in self.ver:
            for j in range(self.njsw):
                # read next surface info record
                self.surfaceinfo = self.get_fortran_record()
                self.surfrecordlist.append(self.surfaceinfo)
                surfinfo = SourceSurf()
                surfinfo.id = self.surfaceinfo.get_long()            # surface ID
                if self.kjaq == 1:
                    surfinfo.facet_id = self.surfaceinfo.get_long()  # facet ID
                else:
                    surfinfo.facet_id = -1                           # dummy facet ID
                surfinfo.type = self.surfaceinfo.get_long()           # surface type
                surfinfo.num_params = self.surfaceinfo.get_long()[0]  # #surface prm
                surfinfo.surf_params = \
                    self.surfaceinfo.get_double(surfinfo.num_params)
                self.surflist.append(surfinfo)
                #print surfinfo.id, surfinfo.facet_id, surfinfo.type, surfinfo.num_params, surfinfo.surf_params
            # we read any extra records as determined by njsw+niwr...
            # no known case of their actual utility is known currently
            for j in range(self.njsw, self.njsw+self.niwr):
                self.get_fortran_record()
                warn("Extra info in header not handled: {0}".format(j),
                     RuntimeWarning)
            # read summary table record
            summary_info = self.get_fortran_record()
            self.summaryrecord=copy.deepcopy(summary_info)
            self.summary_vec = []
            for i in range(0,summary_info.num_bytes/8):
                self.summary_vec.append(summary_info.get_long()[0])
                #print self.summary_vec[i]
            self.summary_vec=numpy.array(self.summary_vec)
            summary_info.reset()
            self.summary_table = summary_info.get_long(
                (2+4*self.mipts)*(self.njsw+self.niwr)+1)
            self.summary_extra = list()
            while summary_info.num_bytes > summary_info.pos:
                self.summary_extra += summary_info.get_long()
        else:
            for j in range(self.njsw):
                # read next surface info record
                self.surfaceinfo = self.get_fortran_record()
                self.surfrecordlist.append(self.surfaceinfo)
                surfinfo = SourceSurf()
                surfinfo.id = self.surfaceinfo.get_int()            # surface ID
                if self.kjaq == 1:
                    surfinfo.facet_id = self.surfaceinfo.get_int()  # facet ID
                else:
                    surfinfo.facet_id = -1                           # dummy facet ID
                surfinfo.type = self.surfaceinfo.get_int()           # surface type
                surfinfo.num_params = self.surfaceinfo.get_int()[0]  # #surface prm
                surfinfo.surf_params = \
                    self.surfaceinfo.get_double(surfinfo.num_params)
                self.surflist.append(surfinfo)
                print surfinfo.id, surfinfo.facet_id, surfinfo.type, surfinfo.num_params, surfinfo.surf_params
            # we read any extra records as determined by njsw+niwr...
            # no known case of their actual utility is known currently
            for j in range(self.njsw, self.njsw+self.niwr):
                self.get_fortran_record()
                warn("Extra info in header not handled: {0}".format(j),
                     RuntimeWarning)
            # read summary table record
            summary_info = self.get_fortran_record()
            self.summaryrecord=copy.deepcopy(summary_info)
            self.summary_table = summary_info.get_int(
                (2+4*self.mipts)*(self.njsw+self.niwr)+1)
            self.summary_extra = list()
            while summary_info.num_bytes > summary_info.pos:
                self.summary_extra += summary_info.get_int()

    def put_header(self):
            """Write the header part of the header to the surface source file"""
            if 'SF_00001' in self.kod:
                rec = [self.kod]
                joinrec = "".join(rec)
                newrecord = _FortranRecord(joinrec, len(joinrec))
                self.put_fortran_record(newrecord)
    
                rec = [self.ver, self.loddat, self.idtm, self.probid, self.aid]
                joinrec = "".join(rec)
                newrecord = _FortranRecord(joinrec, len(joinrec))
                newrecord.put_int([self.knod])
                self.put_fortran_record(newrecord)
            elif '2.7.0' in self.ver:
                rec = [self.kod, self.ver, self.loddat, 
                        self.idtm, self.probid, self.aid]

                joinrec = "".join(rec)
                newrecord = _FortranRecord(joinrec, len(joinrec))
                newrecord.put_long([self.knod])
                self.put_fortran_record(newrecord)
            else:
                rec = [self.kod, self.ver, self.loddat,
                       self.idtm, self.probid, self.aid]
    
                joinrec = "".join(rec)
                newrecord = _FortranRecord(joinrec, len(joinrec))
                newrecord.put_int([self.knod])
                self.put_fortran_record(newrecord)
            return

    def put_table_1(self):
        """Write the table1 part of the header to the surface source file"""
        newrecord = _FortranRecord("", 0)
        if '2.7.0' in self.ver:
            newrecord.put_long([self.orignp1 ]) 
            newrecord.put_long([self.nrss    ]) 
            newrecord.put_long([self.ncrd    ]) 
            newrecord.put_long([self.njsw    ]) 
            newrecord.put_long([self.niss    ]) 
            newrecord.put_long(self.table1extra)
            self.put_fortran_record(newrecord)
        else:
            if '2.6.0' in self.ver:
                newrecord.put_int([self.np1])
                newrecord.put_int([self.nrss])
            else:
                newrecord.put_long([self.np1])
                newrecord.put_long([self.nrss])
    
            newrecord.put_int([self.ncrd])
            newrecord.put_int([self.njsw])
            newrecord.put_int([self.niss])  # MCNP needs 'int', could be 'long' ?
            newrecord.put_int(self.table1extra)
            self.put_fortran_record(newrecord)

        return

    def put_table_2(self):
        """Write the table2 part of the header to the surface source file"""
        if '2.7.0' in self.ver:
            self.put_fortran_record(self.table2record)
        else:
            newrecord = _FortranRecord("", 0)
            newrecord.put_int([self.niwr])
            newrecord.put_int([self.mipts])
            newrecord.put_int([self.kjaq])
            newrecord.put_int(self.table2extra)
            self.put_fortran_record(newrecord)
        return

    def put_surface_info(self):
        """Write the record for each surface to the surface source file"""

        if '2.7.0' in self.ver:
            for cnt, s in enumerate(self.surflist):
                self.put_fortran_record(self.surfrecordlist[cnt])
        else:
            for cnt, s in enumerate(self.surflist):
                newrecord = _FortranRecord("", 0)
                newrecord.put_int(s.id)
                if self.kjaq == 1:
                    newrecord.put_int(s.facet_id)  # don't add a 'dummy facet ID'
                # else no macrobody flag byte in the record
    
                newrecord.put_int(s.type)
                newrecord.put_int(s.num_params)
                newrecord.put_double(s.surf_params)
    
                self.put_fortran_record(newrecord)
        return

    def put_summary(self):
        """Write the summary part of the header to the surface source file"""
        if '2.7.0' in self.ver:
            newrecord = _FortranRecord("", 0)
            newrecord.put_long(self.summary_vec)
            self.put_fortran_record(newrecord)
            #self.put_fortran_record(self.summaryrecord)
        else:
            newrecord = _FortranRecord("", 0)
            newrecord.put_int(list(self.summary_table))
            newrecord.put_int(list(self.summary_extra))
            self.put_fortran_record(newrecord)
        return

    def write_header(self):
        """Write the first part of the MCNP surface source file. The header content
        comprises five parts shown below.
        """
        self.put_header()
        self.put_table_1()
        self.put_table_2()
        self.put_surface_info()
        self.put_summary()

    def write_tracklist(self):
        """Write track records for individual particles. Second part of the MCNP
        surface source file.  Tracklist is also known as a 'phase space'.
        """

        progress = progressbar.ProgressBar()
        for j in progress(range(self.nrss)):  # nrss is the size of tracklist
            newrecord = _FortranRecord("", 0)
            # 11 records comprising particle information
            newrecord.put_double(self.tracklist[j].nps)
            newrecord.put_double(self.tracklist[j].bitarray)
            newrecord.put_double(self.tracklist[j].wgt)
            newrecord.put_double(self.tracklist[j].erg)
            newrecord.put_double(self.tracklist[j].tme)
            newrecord.put_double(self.tracklist[j].x)
            newrecord.put_double(self.tracklist[j].y)
            newrecord.put_double(self.tracklist[j].z)
            newrecord.put_double(self.tracklist[j].u)
            newrecord.put_double(self.tracklist[j].v)
            newrecord.put_double(self.tracklist[j].cs)
            self.put_fortran_record(newrecord)
        return

    def update_tracklist(self, surf_src):
        """ Update tracklist from another surface source.
        This updates the surface source in-place.
        """

        # Catch for improper non-SurfSrc type
        if type(surf_src) != SurfSrc:
            raise TypeError('Surface Source is not of type SurfSrc')

        # Because 'kod' is the first header attribute
        elif not hasattr(surf_src, 'kod'):
            raise AttributeError(
                'No header attributes for surface source argument')
        elif not hasattr(self, 'kod'):
            raise AttributeError(
                'No header attributes read for surface source')

        # Because 'tracklist' forms the non-header portion
        elif not hasattr(surf_src, 'tracklist'):
            raise AttributeError(
                'No tracklist read for surface source argument')
        elif not hasattr(self, 'tracklist'):
            raise AttributeError(
                'No tracklist read for surface source')

        # No point in updating with self
        elif self == surf_src:
            raise ValueError('Tracklist cannot be updated with itself')

        self.tracklist = surf_src.tracklist
        self.nrss = surf_src.nrss

    def __del__(self):
        """Destructor. The only thing to do is close the file."""
        self.f.close()

def make_equi_str(theta_0,N):
	import numpy
	out = [0.0,theta_0]
	theta_minus1 = theta_0
	omega = 2.0*numpy.pi*( 1.0 - numpy.cos(theta_0) )
	for i in range(0,N):
		out.append(  numpy.arccos( numpy.cos(theta_minus1) - omega/(2.0*numpy.pi) )  )
		theta_minus1 = out[-1]
	#check
	for i in range(1,N):
		this_sa = 2.0*numpy.pi * ( numpy.cos(out[i-1]) - numpy.cos(out[i]) )
		if (this_sa-omega)/omega > 1e-8:
			print 'Generated theta bin not equally spaced in sold angle! (bin omega , fixed omega) ',this_sa,omega
	return numpy.array(out)

def rotate_xy(vec,theta,deg=True):
	import numpy
	if deg:
		theta_rad = theta * numpy.pi / 180.0
	else:
		theta_rad = theta
	x=vec[0]*numpy.cos(theta_rad) - vec[1]*numpy.sin(theta_rad)
	y=vec[0]*numpy.sin(theta_rad) + vec[1]*numpy.cos(theta_rad)
	return numpy.array([x,y,vec[2]])


#
#    function to fold a fine-binned xs with a coarse spectrum
#
def rebin_xs(xs=0,xs_e=0,spec_e=0):
	# needs to be pointwise, NOT binned
	assert(len(xs_e)==len(xs))
	#print "length of xs",len(xs)
	#print "length of spec bins",len(spec_e)

	# 
	spec_xs=[]
	for i in range(0,len(spec_e)-1):
		# get requested bin widths
		low  = spec_e[i]
		high = spec_e[i+1]
		# do logic on xs E grid
		logic_low  = xs_e < low
		logic_high = xs_e > high
		dex_low  = numpy.nonzero(numpy.diff(logic_low))[0]
		dex_high = numpy.nonzero(numpy.diff(logic_high))[0]
		# figure out edge cases
		if len(dex_low) == 0:
			if logic_low[0]:	# all ones, low is above last point
				dex_low = len(xs_e)-1
			else:				# all zeros, low is below first point
				dex_low = 0
		else:
			dex_low = dex_low[0]
		if len(dex_high) == 0:
			if logic_high[0]:   # all ones, high is below first point
				dex_high = 0
			else:				# all zeros, high is above last point
				dex_high = len(xs_e)-1
		else:
			dex_high = dex_high[0]
		#print dex_low,dex_high
		# average the pointwise data 
		if dex_low == dex_high:  # bin is within two xs points
			if dex_high == len(xs_e)-1:
				e_l  = xs_e[dex_high]
				e_h  = xs_e[dex_high]
				xs_l = xs[  dex_high]
				xs_h = xs[  dex_high]
				a = 0.0
			else:
				e_l  = xs_e[dex_low]
				e_h  = xs_e[dex_high+1]
				xs_l = xs[  dex_low]
				xs_h = xs[  dex_high+1]
				a = (xs_h-xs_l)/(e_h-e_l)
			b = xs_l - a*e_l
			avg = (a/2.0)*(high*high-low*low)/(high-low)+b
		else:
			avg_vals=[]
			avg_widths=[]
			#do first bin
			e_l  = xs_e[dex_low]
			e_h  = xs_e[dex_low+1]
			xs_l = xs[  dex_low]
			xs_h = xs[  dex_low+1]
			a = (xs_h-xs_l)/(e_h-e_l)
			b = xs_l - a*e_l
			avg_vals.append( (a/2.0)*(e_h*e_h-low*low)/(e_h-low)+b )
			avg_widths.append(e_h-low)
			#do middle bins
			for i in range(dex_low,dex_high-1):
				e_l  = xs_e[i]
				e_h  = xs_e[i+1]
				xs_l = xs[  i]
				xs_h = xs[  i+1]
				a = (xs_h-xs_l)/(e_h-e_l)
				b = xs_l - a*e_l
				avg_vals.append( (a/2.0)*(e_h*e_h-e_l*e_l)/(e_h-e_l)+b )
				avg_widths.append(e_h-e_l)
			#do last bin
			if dex_high == len(xs_e)-1:
				e_l  = xs_e[dex_high]
				e_h  = xs_e[dex_high]
				xs_l = xs[  dex_high]
				xs_h = xs[  dex_high]
				a=0.0
			else:
				e_l  = xs_e[dex_high]
				e_h  = xs_e[dex_high+1]
				xs_l = xs[  dex_high]
				xs_h = xs[  dex_high+1]
				a = (xs_h-xs_l)/(e_h-e_l)
			b = xs_l - a*e_l
			avg_vals.append( (a/2.0)*(high*high-e_l*e_l)/(high-e_l)+b )
			avg_widths.append(high-e_l)
			#avg by bin width and append value
			avg_widths = numpy.array(avg_widths) # normalize
			avg = numpy.average(avg_vals,weights=avg_widths)
		spec_xs.append(avg)
	# return array
	return numpy.array(spec_xs)

def coarsen(values,bins,bin_red=2):
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


def make_steps(ax,bins_in,avg_in,values_in,options=['log'],color=None,label='',ylim=False,linewidth=1):
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
			ax.semilogy(x,y,color=color,label=label,linewidth=linewidth)
		else:
			ax.plot(x,y,color=color,label=label,linewidth=linewidth)
	else:   #default to log if lin not present
		if 'logy' in options:
			ax.loglog(x,y,color=color,label=label,linewidth=linewidth)
		else:
			ax.semilogx(x,y,color=color,label=label,linewidth=linewidth)


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


#
#
#
#
#
#  START OF TASKS
#
#
#
#
#
charge_per_amp = 6.241e18
charge_per_milliamp = charge_per_amp/1000.0

filename = sys.argv[1]
phi_bin = int(sys.argv[2])
theta_bin = int(sys.argv[3])
#E_bin = int(sys.argv[4])
obj_bin = 1

printflag = True
errorflag = False#True
sphere = False
max_wgt = 1e99

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
	ss = SurfSrc(filename)
	ss.read_header()
	#ss.read_tracklist()
	print ss.print_header()
elif typeflag == 2:
	f=open(filename,'r')
	ss = cPickle.load(f)
		
else:
	f=open(filename,'r')
	d = cPickle.load(f)
	f.close()

if printflag:
	print "Done."

this_sc = int(sys.argv[4])
type_in = sys.argv[5]
print type_in
if 'flux' in type_in:
    fluxflag=True
else:
    fluxflag=False

print fluxflag

### init
if typeflag:
	if this_sc == 81233:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 1e-6, 600])
		#x_bins   = numpy.linspace(-10,10,41)
		#y_bins   = numpy.linspace(-15,25,81)
		x_bins   = numpy.array([-1.5,1.5])
		y_bins   = numpy.array([-9.0,-6.0,-3.0,0.0,3.0,6.0,9.0])
		theta_bins = numpy.array([0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist	 = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane	= numpy.array([4.3837115E-01 , -8.9879405E-01 ,  0.0000000E+00  , 8.1346130E+02  ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 379.190607512  , -720.115 ,     -18.5            ])   # global again
		surface_normal 	= numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]])  
		surface_vec1    = numpy.array([-surface_plane[1], surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 81202:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 1e-6, 600])
		#x_bins   = numpy.linspace(-4.75,4.75,21)
		x_bins   = numpy.linspace(-4.75,4.75,2)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff)
		#y_bins   = numpy.linspace(-8.5,8.5,41)
		y_bins   = numpy.linspace(-8.5,8.5,2)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		theta_bins = numpy.array([0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist	 = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters 
		surface_plane	= numpy.array([4.3837115E-01 , -8.9879405E-01 ,  0.0000000E+00 ,  2.1106130E+02  ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([115.105, -178.686751185 ,     -18.5            ])   # global again
		surface_normal 	= numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]])  
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])   # why negative?! - because normal is OUTWARDS away from target
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
	elif this_sc == 20359:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 1e-6 ,600])
		#x_bins   = numpy.linspace(-7,7,41)
		x_bins   = numpy.linspace(-7,7,29)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-13.5,13.5,81)
		y_bins   = numpy.linspace(-13.5,13.5,55)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins	 = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		theta_bins = numpy.array([0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist	 = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		#surface_plane	= numpy.array([-4.0673664E-01 ,  9.1354546E-01 ,  0.0000000E+00 , -3.0003472E+00  ])   # plane, GLOBAL coordinates
		surface_plane	= numpy.array([-4.0673664E-01 ,  9.1354546E-01 ,  0.0000000E+00 , -5.0003472E+00])
		surface_center  = numpy.array([ 24.095 ,  7.443876237  ,     -16.            ])   # global again
		surface_normal 	= numpy.array([-surface_plane[0],-surface_plane[1],-surface_plane[2]])   # SS written for -20359!  normal is flipped
		surface_vec1    = numpy.array([ surface_plane[1],-surface_plane[0] ,  0.0])               # why negative?! - because normal is OUTWARDS away from target
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
	elif this_sc == 10146:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 1e-6 ,60])
		#x_bins   = numpy.linspace(-7,7,21)
		x_bins   = numpy.linspace(-2.5,2.5,11)
		diff     = x_bins[1]-x_bins[0]
		x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-13.5,13.5,41)
		y_bins   = numpy.linspace(-6,6,25)
		diff     = y_bins[1]-y_bins[0]
		y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins  = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		theta_bins = numpy.array([0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([0.99863,  -0.052336 , 0.0 , 623.0  ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 623.5654 ,  -5.52  ,    0.            ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 4:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 1e-6 ,60])
		x_bins   = numpy.linspace(-15,15,81)
		diff     = x_bins[1]-x_bins[0]
		x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-15,15,81)
		diff     = y_bins[1]-y_bins[0]
		y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins  = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		theta_bins = numpy.array([0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([   1,  0.0 , 0.0 , 148  ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 148 ,  0  ,    0.            ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([surface_plane[1], -surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10150:
		#  bin parameters
		E_bins   = numpy.array([0,  to_energy(3)])  # 2.27e-9 = 6 A, 9.09e-9 = 3 A ,1e-6 = 0.3 A
		#E_bins   = to_energy(numpy.linspace(1,13,121))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-1,2,4)
		x_bins   = numpy.linspace(-15,15,61)
		diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-4,1,6)
		y_bins   = numpy.linspace(-15,15,61)
		diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins  = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		#theta_bins = numpy.array([0,0.25,0.5,0.75,1.0,1.25,1.50,1.75,2.0,2.25,2.5,2.75,3.0,3.25,3.5,3.75,4.0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,2.0])*numpy.pi/180.0
		#theta_bins  = make_equi_str(0.5*numpy.pi/180.0,64)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		# surface_plane   = numpy.array([   0.99961, 0.0279216, 0.0, 159.543  ])   # plane, GLOBAL coordinates
		surface_plane   = numpy.array([  0.99863 ,0.052336 ,0.0 , 159.543  ])
		#surface_center  = numpy.array([ 160.5432 ,  -33.58  ,    0.            ])   # global again
		# centered on AMOR guide
		surface_center  = numpy.array([ 160.436237733 ,  -29.75  ,    0.            ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10156:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 1e-6 ,600])
		x_bins   = numpy.linspace(-25,25,81)
		diff     = x_bins[1]-x_bins[0]
		x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-20,20,81)
		diff     = y_bins[1]-y_bins[0]
		y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins  = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		theta_bins = numpy.array([0,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  0.990268 , -0.1391730 , 0.0, 165.728  ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 159.0746496,  -58.93  ,    0.            ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10110:
		#  bin parameters
		E_bins   = numpy.array([1e-12, 5e-9, 1e-6 ,600])  # 5e-9 = 4 A, 1e-6 = 0.3 A
		x_bins   = numpy.linspace(-2.5,2.5,11)
		diff     = x_bins[1]-x_bins[0]
		x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-6,6,25)
		diff     = y_bins[1]-y_bins[0]
		y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins  = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		theta_bins = numpy.array([0,0.125,2,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([   0.99863 ,  0.052336 , 0.0 , 159.573 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  161.3210058 , -29.75  ,    0.            ])   # global again
		#surface_plane   = numpy.array([   0.99961, 0.0279216, 0.0, 159.573 ])   # plane, GLOBAL coordinates
		#surface_center  = numpy.array([ 160.5432 ,  -33.58  ,    0.            ])   # global again
		# centered on AMOR guide
		#surface_center  = numpy.array([ 160.436237733 ,  -29.75  ,    0.            ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10160:
		#  bin parameters
		E_bins   = numpy.array([1e-12,600])  # 5e-9 = 4 A, 1e-6 = 0.3 A
		x_bins   = numpy.linspace(-2.0,2.0,11)
		diff     = x_bins[1]-x_bins[0]
		x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-6,6,25)
		diff     = y_bins[1]-y_bins[0]
		y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#E_bins  = to_energy(numpy.array([0,0.01,0.1,0.5,1,2,3,4,5,6,7,8,9,10]))
		#E_bins   = E_bins[::-1]
		#x_bins   = numpy.linspace(-7,7,5)
		#y_bins   = numpy.linspace(-13.5,13.5,5)
		theta_bins = numpy.array([0,0.125,2,90,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([   0.999994 , 0.00349065 , 0.0 , 161.0 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  161.132250181, -37.61  ,    0.            ])   # global again
		#surface_plane   = numpy.array([   0.99961, 0.0279216, 0.0, 159.573 ])   # plane, GLOBAL coordinates
		#surface_center  = numpy.array([ 160.5432 ,  -33.58  ,    0.            ])   # global again
		# centered on AMOR guide
		#surface_center  = numpy.array([ 160.436237733 ,  -29.75  ,    0.            ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10010:
		#  bin parameters
		#E_bins   = numpy.array([1e-12,9.09e-9,1e-6,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		E_bins   = numpy.array([1e-12,600])
		x_bins   = numpy.linspace(-2.5,2.5,21)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-2.5,2.5,21)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#theta_bins = numpy.array([0,90])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins  = make_equi_str(10.0*numpy.pi/180.0,32)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([   9.9862953E-01 , -5.2335956E-02  , 0.0000000E+00  , 1.6486150E+01 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  14.48, -38.71  ,    0.            ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10171:
		#  bin parameters
		E_bins   = numpy.array([1e-12,9.09e-9,1e-6,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		#E_bins    = numpy.array([8.5124057517656764e-09,9.7270177496394964e-09])
		x_bins   = numpy.linspace(-12,12,49)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-12,12,49)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#theta_bins = numpy.array([0,0.25,0.5,0.75,1.0,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,90])*numpy.pi/180.0 
		#theta_bins  = make_equi_str(1.0*numpy.pi/180.0,10)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  0.99863 , -0.052336 , 0.0 , 130.2001 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  128.5874203,  -34.18,   0.  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = rotate_xy(surface_normal,3.0)
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10172:
		#  bin parameters
		E_bins   = numpy.array([1e-12,1e-6,1.0,600])
		#x_bins   = numpy.linspace(-45,45,181)
		#x_bins   = numpy.linspace(-20,20,41)
		#x_bins   = numpy.linspace(-6.76,-1.76,11)
		x_bins   = numpy.linspace(-11,11,45)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-45,45,181)
		#y_bins   = numpy.linspace(-10,10,21)
		y_bins   = numpy.linspace(-7,7,29)
		#theta_bins = numpy.array([0,0.25,0.5,0.75,1.0,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0.00,0.15,0.30,0.60,1.00,1.50,2.0,2.5,3.0])*numpy.pi/180.0 
		#theta_bins = numpy.array([0.00,0.60,1.00,1.50,2.0,2.5,3.0])*numpy.pi/180.0 
		#theta_bins  = make_equi_str(1.0*numpy.pi/180.0,10)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 0.99863 , -0.052336 , 0.0 , 130.2002])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  127.5438191,  -54.095,   0.  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees = -6.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees)  # FOCUS is -6 degrees off plane
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees)  # FOCUS is -6 degrees off plane
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees)  # FOCUS is -6 degrees off plane
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10177:
		#  bin parameters
		E_bins   = numpy.array([1e-12,9.09e-9,1e-6,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		x_bins   = numpy.linspace(-3,3,13)
		diff     = x_bins[1]-x_bins[0]
		x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-7,7,29)
		diff     = y_bins[1]-y_bins[0]
		y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#theta_bins = numpy.array([0,0.25,0.5,0.75,1.0,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins = numpy.array([0,90])*numpy.pi/180.0 
		theta_bins  = make_equi_str(1.0*numpy.pi/180.0,3)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  0.999994  , 0.00349065  ,  0.0 , 160.604 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  160.7362478 , -37.61 ,   0.  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10113:
		#  bin parameters
		#expon = numpy.linspace(-11,3,1025)
		#E_bins   =   numpy.power(10.0,expon) 
		#E_bins   = numpy.array([1e-12,1e-6,10,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		E_bins   = numpy.array([1e-11,1e-6,1,600])
		#x_bins   = numpy.linspace(-26,26,14)
		x_bins   = numpy.linspace(-26,26,209)
		#y_bins   = numpy.linspace(-10,10,6)
		y_bins   = numpy.linspace(-10,10,81)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#theta_bins = numpy.array([0,20.0])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins  = make_equi_str(5*numpy.pi/180.0,16)
		theta_bins = numpy.linspace(0.0,10.0,21)*numpy.pi/180.0
		#theta_bins = numpy.array([0.0,2.0,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  0.99863,  -0.052336,  0.0,  130.11 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  128.007636,  -43.52137 ,    0. ])
		#surface_center  = numpy.array([  128.059972,  -42.52274 ,    0.      ])
		#surface_center  = numpy.array([  127.9553,  -44.52,  0  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10175:
		#  bin parameters
		#expon = numpy.linspace(-11,3,1025)
		#E_bins   =   numpy.power(10.0,expon) 
		E_bins   = numpy.array([1e-12,2.27e-9,9.09e-9,1e-6,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A, 2.27e-9 = 6 A, 9.09e-9 = 3 A ,1e-6 = 0.3 A
		x_bins   = numpy.linspace(-3,3,25)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-7,7,57)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		theta_bins = numpy.array([0,90])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins  = make_equi_str(10.0*numpy.pi/180.0,32)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  0.99863,  0.052336,  0.0,  158.746 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  160.5229124, -29.75, 0.0 ])
		#surface_center  = numpy.array([  128.059972,  -42.52274 ,    0.      ])
		#surface_center  = numpy.array([  127.9553,  -44.52,  0  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10189:
		#  bin parameters
		#expon = numpy.linspace(-11,3,1025)
		#E_bins   =   numpy.power(10.0,expon) 
		E_bins   = numpy.array([1e-12,2.27e-9,9.09e-9,1e-6,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A, 2.27e-9 = 6 A, 9.09e-9 = 3 A ,1e-6 = 0.3 A
		x_bins   = numpy.linspace(-3,3,25)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		y_bins   = numpy.linspace(-7,7,57)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		theta_bins = numpy.array([0,90])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins  = make_equi_str(10.0*numpy.pi/180.0,32)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  0.99863,  0.052336,  0.0,  622.746 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  623.8867411, -5.465, 0.0 ])
		#surface_center  = numpy.array([  128.059972,  -42.52274 ,    0.      ])
		#surface_center  = numpy.array([  127.9553,  -44.52,  0  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == -51030:
		#  bin parameters
		E_bins   = numpy.array([1e-12,1e-6,1.0,600])
		#x_bins   = numpy.linspace(-45,45,181)
		#x_bins   = numpy.linspace(-20,20,41)
		#x_bins   = numpy.linspace(-6.76,-1.76,11)
		x_bins   = numpy.linspace(-6,6,25)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-45,45,181)
		#y_bins   = numpy.linspace(-10,10,21)
		y_bins   = numpy.linspace(-8,8,33)
		#theta_bins = numpy.array([0,0.25,0.5,0.75,1.0,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0.0,2.0,10.0,80.0])*numpy.pi/180.0 
		#theta_bins = numpy.array([0.00,0.60,1.00,1.50,2.0,2.5,3.0])*numpy.pi/180.0 
		#theta_bins  = make_equi_str(1.0*numpy.pi/180.0,10)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([0.970295727808 , -0.241921898123, 0.0 ,-498.288785066 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  -492.3353727, 85.06,  0.0  ])   # global again
		surface_normal  = -numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = -numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == -51302:
		#  bin parameters
		E_bins   = numpy.array([1e-12,1e-6,1.0,600])
		#x_bins   = numpy.linspace(-45,45,181)
		#x_bins   = numpy.linspace(-20,20,41)
		#x_bins   = numpy.linspace(-6.76,-1.76,11)
		x_bins   = numpy.linspace(-8,8,257)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-45,45,181)
		#y_bins   = numpy.linspace(-10,10,21)
		y_bins   = numpy.linspace(-8,8,257)
		#theta_bins = numpy.array([0,0.25,0.5,0.75,1.0,180])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0.0,2.0,10.0,80.0])*numpy.pi/180.0 
		#theta_bins = numpy.array([0.00,0.60,1.00,1.50,2.0,2.5,3.0])*numpy.pi/180.0 
		#theta_bins  = make_equi_str(1.0*numpy.pi/180.0,10)
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([0.970295727808, -0.241921898123, 0.0, -662.854375066])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  -651.358678, 127.495,  0.0  ])   # global again
		surface_normal  = -numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_vec1    = -numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10541:
		# sphere flag
		sphere = True
		#  bin parameters
		E_bins   = numpy.array([1e-12,1e-6,1.0,600])
		x_bins   = numpy.linspace(0,2.0*numpy.pi,17)  # azimuthal phi
		y_bins   = numpy.linspace(0,1.0*numpy.pi,17)  # polar theta
		#theta_bins = (numpy.pi - make_equi_str(1.0*numpy.pi/180.0,10) )#*numpy.pi/180.0
		#theta_bins = (180.0    - numpy.array([0.0,2.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.,90.0,180.0]))*numpy.pi/180.0 
		#theta_bins = (180.0    - numpy.array([0.0,10.0,20.0,40.0,90.0,180.0]))*numpy.pi/180.0 
		theta_bins = (180.0    - numpy.array([0.0,180.0]))*numpy.pi/180.0 
		theta_bins = theta_bins[::-1]
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		sphere_radius = 15.240
		surface_center  =  numpy.array([  744.1382, -80.8976 , 0.0  ])   # sphere center
		surface_plane   =  numpy.array([0.0,0.0,0.0])   # sphere radius
		surface_normal  = -numpy.array([0.0,0.0,0.0]) # null since they are recalculated each time
		surface_vec1    = -numpy.array([0.0,0.0,0.0]) # null since they are recalculated each time
		surface_vec2    =  numpy.array([0.0,0.0,0.0]) # null since they are recalculated each time
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=128.
		surface_area=4.0*numpy.pi*sphere_radius*sphere_radius
		#
		#max_wgt = 1e-7
	elif this_sc == 21:
		# sphere flag
		sphere = False
		#  bin parameters
		E_bins   = numpy.array([1e-12,1e-6,1.0,600])
		x_bins   = numpy.linspace(-6,6,97)  # azimuthal phi
		y_bins   = numpy.linspace(-6,6,97)  # polar theta
		theta_bins = (numpy.linspace(0,numpy.pi,2))
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   =  numpy.array([1.0,0.0,0.0,6.0]) #
		surface_center  =  numpy.array([  6.0 , 0.0 , 0.0 ])   # sphere center
		surface_normal  =  numpy.array([1.0,0.0,0.0]) # null since they are recalculated each time
		surface_vec1    =  numpy.array([0.0,0.0,1.0]) # null since they are recalculated each time
		surface_vec2    =  numpy.array([0.0,1.0,0.0]) # null since they are recalculated each time
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 25:
		# sphere flag
		sphere = False
		#  bin parameters
		E_bins   = numpy.array([1e-12,1e-6,1.0,600])
		x_bins   = numpy.linspace(-6,6,97)  # azimuthal phi
		y_bins   = numpy.linspace(-6,6,97)  # polar theta
		theta_bins = (numpy.linspace(0,numpy.pi,2))
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   =  numpy.array([0.0,0.0,1.0,6.0]) #
		surface_center  =  numpy.array([0.0 , 0.0 , 6.0 ])   # sphere center
		surface_normal  =  numpy.array([0.0,0.0,1.0]) # null since they are recalculated each time
		surface_vec1    =  numpy.array([1.0,0.0,0.0]) # null since they are recalculated each time
		surface_vec2    =  numpy.array([0.0,1.0,0.0]) # null since they are recalculated each time
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 2232:
		# sphere flag
		sphere = False
		#  bin parameters
		#expon = numpy.linspace(-11,3,1025)
		#E_bins   =   numpy.power(10.0,expon) 
		#E_bins   = numpy.array([1e-12,1e-6,10,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		E_bins   = numpy.array([1e-11,1e-6,2e-6,600])
		#x_bins   = numpy.linspace(-45,45,181)
		#x_bins   = numpy.linspace(-20,20,41)
		#x_bins   = numpy.linspace(-19.1,-14.1,11)
		x_bins   = numpy.linspace(-0.707,0.707,9)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-45,45,181)
		#y_bins   = numpy.linspace(-10,10,21)
		y_bins   = numpy.linspace(-0.707,0.707,9) # to fit in circle radius 1
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		theta_bins = numpy.array([0,3.0])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins  = make_equi_str(1*numpy.pi/180.0,8)
		#theta_bins = numpy.linspace(0,15,5)*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 5.5919290E-01  , 8.2903757E-01 ,  0.0000000E+00  , 2.5706860E+02])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  123.835,  226.5529984 ,    5. ])
		#surface_center  = numpy.array([  128.059972,  -42.52274 ,    0.      ])
		#surface_center  = numpy.array([  127.9553,  -44.52,  0  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=128.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 51001:
		# sphere flag
		sphere = False
		#  bin parameters
		#expon = numpy.linspace(-11,3,1025)
		#E_bins   =   numpy.power(10.0,expon) 
		#E_bins   = numpy.array([1e-12,1e-6,10,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		E_bins   = numpy.array([1e-11,1e-6,2e-6,600])
		#x_bins   = numpy.linspace(-45,45,181)
		#x_bins   = numpy.linspace(-20,20,41)
		#x_bins   = numpy.linspace(-19.1,-14.1,11)
		x_bins   = numpy.linspace(-5,5,21)
		#diff     = x_bins[1]-x_bins[0]
		#x_bins   = numpy.insert(x_bins,0,x_bins[0] -diff)
		#x_bins   = numpy.append(x_bins,  x_bins[-1]+diff) 
		#y_bins   = numpy.linspace(-45,45,181)
		#y_bins   = numpy.linspace(-10,10,21)
		y_bins   = numpy.linspace(-8.5,8.5,35) # to fit in circle radius 1
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		theta_bins = numpy.array([0,1,2,3,4,5])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins  = make_equi_str(1*numpy.pi/180.0,8)
		#theta_bins = numpy.linspace(0,15,5)*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ -0.97029573, 0.2419219, 0.0,  193.46138])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  -196.5652811, 11.305, 0.0 ])
		#surface_center  = numpy.array([  128.059972,  -42.52274 ,    0.      ])
		#surface_center  = numpy.array([  127.9553,  -44.52,  0  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 51503:
		# sphere flag
		sphere = False
		#  bin parameters
		E_bins   = numpy.array([1e-11,1e-6,2e-6,1,600])
		x_bins   = numpy.linspace(-5,5,21)
		y_bins   = numpy.linspace(-10,10,41)
		theta_bins = numpy.array([0,1,2,3,4,5])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ -.96420539, 0.26515648, 0.0, 815.79419])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  -799.6317678, 168.9, 0.0 ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 1601:
		# sphere flag
		sphere = False
		#  bin parameters
		#E_bins   = numpy.array([1e-11,1e-6,1,600])
		E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# for high stats
		x_bins   = numpy.linspace(-70,70,1121)
		y_bins   = numpy.linspace(-20,20,321)
		# for low stats
		#x_bins   = numpy.linspace(-70,70,281)
		#y_bins   = numpy.linspace(-20,20,81)
		# for just AMOR/SANS
		#x_bins   = numpy.linspace( 60,70,81)
		#y_bins   = numpy.linspace(-20,20,321)
		#theta_bins = numpy.array([0,1,2,3,4,5,10,20])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,1,2,3,4,5,6,7,8,9,10,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 0.998333761, -0.057703567, 0.0, 620.4684655])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 617.5670016, -68.115 , 0.0 ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 19990:
		#  bin parameters
		#expon = numpy.linspace(-11,3,1025)
		#E_bins   =   numpy.power(10.0,expon) 
		#E_bins   = numpy.array([1e-12,1e-6,10,600])  # 5e-9 = 4 A, 9.09e-9 = 3A, 1e-6 = 0.3 A
		E_bins   = numpy.array([1e-11,1e-6,1,600])
		#x_bins   = numpy.linspace(-26,26,14)
		x_bins   = numpy.linspace(-4,4,17)
		#y_bins   = numpy.linspace(-10,10,6)
		y_bins   = numpy.linspace(-7,7,29)
		#diff     = y_bins[1]-y_bins[0]
		#y_bins   = numpy.insert(y_bins,0,y_bins[0] -diff)
		#y_bins   = numpy.append(y_bins,  y_bins[-1]+diff)
		#theta_bins = numpy.array([0,20.0])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		#theta_bins  = make_equi_str(5*numpy.pi/180.0,16)
		theta_bins = numpy.linspace(0.0,10.0,21)*numpy.pi/180.0
		#theta_bins = numpy.array([0.0,2.0,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([  .99862953, 0.052335956, 0.0, 158.59979 ])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  160.376838,  -29.755 ,    0. ])
		#surface_center  = numpy.array([  128.059972,  -42.52274 ,    0.      ])
		#surface_center  = numpy.array([  127.9553,  -44.52,  0  ])   # global again
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10304:
		# sphere flag
		sphere = False
		#  bin parameters
		#E_bins   = numpy.array([1e-11,1e-6,1,600])
		E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# for high stats
		x_bins   = numpy.linspace(-425,425,1701)
		y_bins   = numpy.linspace(-153.5,286.0,880)
		# for low stats
		#x_bins   = numpy.linspace(-70,70,281)
		#y_bins   = numpy.linspace(-20,20,81)
		# for just AMOR/SANS
		#x_bins   = numpy.linspace( 60,70,81)
		#y_bins   = numpy.linspace(-20,20,321)
		#theta_bins = numpy.array([0,1,2,3,4,5,10,20])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 1.0, 0.0, 0.0, 1165.0734])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 1165.0734, -226.3105 , 0.0 ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 10307:
		# sphere flag
		sphere = False
		#  bin parameters
		#E_bins   = numpy.array([1e-11,1e-6,1,600])
		E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# for high stats
		#x_bins   = numpy.linspace(-425,425,1701)
		#y_bins   = numpy.linspace(-153.5,286.0,880)
		# AMOR
		x_bins   = numpy.linspace(383,433,2)
		y_bins   = numpy.linspace(15,93,2)
		# for low stats
		#x_bins   = numpy.linspace(-70,70,281)
		#y_bins   = numpy.linspace(-20,20,81)
		# for just AMOR/SANS
		#x_bins   = numpy.linspace( 60,70,81)
		#y_bins   = numpy.linspace(-20,20,321)
		theta_bins = numpy.array([0,1,2,3,4,5,6,10])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 1.0, 0.0, 0.0, 2.9847115E+03])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 2.9847115E+03, -226.3105 , 0.0 ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 19921:
		# sphere flag
		sphere = False
		#  bin parameters
		E_bins   = numpy.array([1e-11,1e-6,1,600])
		# E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# for high stats
		x_bins   = numpy.linspace(-3,3,25)
		y_bins   = numpy.linspace(-3,3,25)
		# for low stats
		#x_bins   = numpy.linspace(-70,70,281)
		#y_bins   = numpy.linspace(-20,20,81)
		# for just AMOR/SANS
		#x_bins   = numpy.linspace( 60,70,81)
		#y_bins   = numpy.linspace(-20,20,321)
		#theta_bins = numpy.array([0,1,2,3,4,5,10,20])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 0.999271498664505 , 0.038163751869997 , 0.0 , 2919.054060375774500])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 2917.492265, 96.615, 3.5 ])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 19920:
		# sphere flag
		sphere = False
		#  bin parameters
		E_bins   = numpy.array([1e-11,1e-6,1,600])
		# E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# for high stats
		x_bins   = numpy.linspace(-3,3,25)
		y_bins   = numpy.linspace(-3,3,25)
		# for low stats
		#x_bins   = numpy.linspace(-70,70,281)
		#y_bins   = numpy.linspace(-20,20,81)
		# for just AMOR/SANS
		#x_bins   = numpy.linspace( 60,70,81)
		#y_bins   = numpy.linspace(-20,20,321)
		#theta_bins = numpy.array([0,1,2,3,4,5,10,20])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 0.999271498664505 , 0.038163751869997 , 0.0 , 2955.054060373856400])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([  2953.46603895,    97.98889507,    3.5])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec2    = numpy.array([0.0,0.0,1.0])
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	elif this_sc == 19940:
		# sphere flag
		sphere = False
		#  bin parameters
		E_bins   = numpy.array([1e-11,1e-6,1,600])
		# E_bins   = numpy.array([1e-11,to_energy(2.0),600])
		# for high stats
		x_bins   = numpy.linspace(-3,3,25)
		y_bins   = numpy.linspace(-3,3,25)
		# for low stats
		#x_bins   = numpy.linspace(-70,70,281)
		#y_bins   = numpy.linspace(-20,20,81)
		# for just AMOR/SANS
		#x_bins   = numpy.linspace( 60,70,81)
		#y_bins   = numpy.linspace(-20,20,321)
		#theta_bins = numpy.array([0,1,2,3,4,5,10,20])*numpy.pi/180.0   # 90 included as sanity check, ss should only write tracks in normal dir
		theta_bins = numpy.array([0,90])*numpy.pi/180.0
		phi_bins = numpy.linspace(0,2*numpy.pi,2) 
		dist     = numpy.zeros((  len(E_bins)-1 , len(theta_bins)-1 , len(phi_bins)-1 , len(y_bins)-1 , len(x_bins)-1 ),dtype=numpy.float64)
		#  surface plane parameters
		surface_plane   = numpy.array([ 9.9491877E-01 ,  9.3828069E-02 ,  3.6509316E-02  , 2.0678812E+03])   # plane, GLOBAL coordinates
		surface_center  = numpy.array([ 2065.759820, 134.48, 0.0])
		surface_normal  = numpy.array([surface_plane[0],surface_plane[1],surface_plane[2]]) 
		surface_normal_rot = surface_normal 
		surface_vec1    = numpy.array([-surface_plane[1],surface_plane[0] ,  0.0])
		surface_vec1    = surface_vec1 / numpy.sqrt(numpy.dot(surface_vec1,surface_vec1))
		surface_vec2    = -numpy.cross(surface_vec1,surface_normal)
		yz_rotation_degrees =  0.0
		xy_rotation_degrees =  0.0
		surface_normal_rot  = rotate_xy(surface_normal,xy_rotation_degrees) 
		surface_vec1_rot    = rotate_xy(surface_vec1,  xy_rotation_degrees) 
		surface_vec2_rot    = rotate_xy(surface_vec2,  xy_rotation_degrees) 
		# spectrum plot
		spec_res=256.
		surface_area=(x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
else:
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
	if 'max_wgt' in d:
		max_wgt             = d['max_wgt']
	if 'sphere' in d:
		sphere_radius	= d['sphere_radius']
		sphere			= d['sphere']
		surface_area 	= 4.0*numpy.pi*sphere_radius*sphere_radius
	else:
		surface_area 	= (x_bins[-1]-x_bins[0])*(y_bins[-1]-y_bins[0])
	print "average weight per track ",total_weight/total_tracks

### print some details
if printflag:
	print "\n============================\n"

	if typeflag == 1:
		print "Binning '"+filename+"' according to:\n"
	else:
		print "Binning in '"+filename+"' done according to:\n"

	print "***NEUTRONS ONLY***"
	print ""
	print "Energy bin boundaries (MeV)\n",E_bins 
	print ""
	print "Wavelength bin boundaries (A)\n",to_wavelength(E_bins)
	print "    "
	print "Theta (polar) bin boundaries (degrees)\n", theta_bins*180.0/numpy.pi
	print "    "
	print "Theta (polar) bin boundaries (radians)\n", theta_bins
	print "    "
	print "Theta (polar) bin boundaries (cosines, reversed order)\n", numpy.cos(theta_bins)[::-1]
	print "    "
	print "Phi (azimuthal) bin boundaries (degrees)\n", phi_bins*180.0/numpy.pi
	print "    "
	if sphere:
		print "Y (polar) bin boundaries (radians)\n", y_bins
		print "    "
		print "X (azimuthal) bin boundaries (radians)\n", x_bins
	else:
		print "Y bin boundaries (cm)\n", y_bins
		print "    "
		print "X bin boundaries (cm)\n", x_bins
	print "    "
	print "NORMAL HAS BEEN ROTATED (only for angular variable calculations, not position!):\n",
	print "   X-Y:  % 4.2f degrees" % xy_rotation_degrees
	print "   Y-Z:  % 4.2f degrees" % yz_rotation_degrees
	print "    "

### check to make sure surface basis vectors are orthogonal
assert( numpy.abs(numpy.dot(surface_vec1,surface_vec2)  ) <= 1.e-8 )
assert( numpy.abs(numpy.dot(surface_vec1,surface_normal)) <= 1.e-8 )
assert( numpy.abs(numpy.dot(surface_vec2,surface_normal)) <= 1.e-8 )

### plot positions and vectors to make sure everything is OK

# 3d plot objects
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# origin
ax.scatter([0.0],[0.0],[0.0],'o',color='r')
# center
ax.scatter(surface_center[0],surface_center[1],surface_center[2],'o',color='b')


if sphere:
	#draw sphere
	u, v = numpy.mgrid[0:2*numpy.pi:20j, 0:numpy.pi:10j]
	x=numpy.cos(u)*numpy.sin(v)
	y=numpy.sin(u)*numpy.sin(v)
	z=numpy.cos(v)
	ax.plot_wireframe(sphere_radius*x+surface_center[0], sphere_radius*y+surface_center[1], sphere_radius*z+surface_center[2], color="r")
else:
	# plane lines
	plane_size = 0.3*numpy.linalg.norm(surface_center)
	p1 = surface_center + surface_vec2*plane_size - surface_vec1*plane_size
	p2 = surface_center + surface_vec2*plane_size + surface_vec1*plane_size
	p3 = surface_center - surface_vec2*plane_size + surface_vec1*plane_size
	p4 = surface_center - surface_vec2*plane_size - surface_vec1*plane_size
	pts=numpy.vstack((p1,p2,p3,p4,p1))
	ax.plot(pts[:,0],pts[:,1],pts[:,2],color='b')
	# 
	# print surface_normal
	# print surface_plane[0:3]
	# print numpy.cross(surface_plane[0:3],surface_normal)
	# print pts
	#
	# normal
	ax.quiver(surface_center[0],surface_center[1],surface_center[2],surface_normal[0],surface_normal[1],surface_normal[2],            color='b',pivot='tail',length=plane_size)
	ax.quiver(surface_center[0],surface_center[1],surface_center[2],  surface_vec1[0],  surface_vec1[1],  surface_vec1[2],            color='b',pivot='tail',length=plane_size)
	ax.quiver(surface_center[0],surface_center[1],surface_center[2],  surface_vec2[0],  surface_vec2[1],  surface_vec2[2],            color='b',pivot='tail',length=plane_size)
	# rotated normal
	ax.quiver(surface_center[0],surface_center[1],surface_center[2],surface_normal_rot[0],surface_normal_rot[1],surface_normal_rot[2],color='r',pivot='tail',length=plane_size)
	ax.quiver(surface_center[0],surface_center[1],surface_center[2],  surface_vec1_rot[0],  surface_vec1_rot[1],  surface_vec1_rot[2],color='r',pivot='tail',length=plane_size)
	ax.quiver(surface_center[0],surface_center[1],surface_center[2],  surface_vec2_rot[0],  surface_vec2_rot[1],  surface_vec2_rot[2],color='r',pivot='tail',length=plane_size)
# make sure equal so no distortions, can be done better I'm sure
xlim = ax.get_xlim()
ylim = ax.get_ylim()
zlim = ax.get_zlim()
newlims=[numpy.min(numpy.hstack((xlim,ylim,zlim))),numpy.max(numpy.hstack((xlim,ylim,zlim)))]
ax.set_xlim(newlims)
ax.set_ylim(newlims)
ax.set_zlim(newlims)
# show 
plt.show()

### make bins for tally-like histograms
#logE bins
#finebins=[]
#Emin=E_bins[0]
#Emax=E_bins[-1]
#for j in range(0,int(spec_res)+1):
#	finebins.append(Emin*numpy.power(Emax/Emin, j/spec_res))
#finebins = numpy.array(finebins)

# options
brightness = True#False
wavelength = False

# wavelength bins
if wavelength:
	finebins = to_energy(  numpy.linspace( to_wavelength(600) ,20, spec_res+1)  )
	finebins = finebins[::-1]
	avg=(finebins[:-1]+finebins[1:])/2.0
else:
	# log energy bins
	finebins = numpy.power(10.0,numpy.linspace( -11, numpy.log10(600), spec_res+1))
	avg=(finebins[:-1]+finebins[1:])/2.0

### make bins for weight histogram
w_bins=[]
w_min = 1e-20
w_max = 2.0
w_res = 1024.0
for j in range(0,int(w_res)+1):
	w_bins.append(w_min*numpy.power(w_max/w_min, j/w_res))
w_bins = numpy.array(w_bins)



#answer=1
#print "first track:"
#while answer:
#	track = ss.next_track()
#	print 'xyz ',numpy.array([track.x,track.y,track.z]),' wgt ',track.wgt,' erg ',track.erg
#	answer = input('Next track?')
#exit(0)

### scan tracks
if typeflag:

	### init some stuff
	last_nps = 0
	x_avg = 0.
	x_dex_avg = 0
	bitarrays=[]
	histograms_curr=[]
	histograms_flux=[]
	histograms_wght=[]
	wgt_avg = 0.5
	count =1.0
	for i in range(0,len(theta_bins)-1):
		histograms_curr.append(histogram(finebins))
		histograms_flux.append(histogram(finebins))
		histograms_wght.append(histogram(w_bins))

	if printflag:
		print "\n============================\n"
		print "Binning %d tracks... "%min(ss.nrss,int(1e10))
	for i in progress(range(1,min(ss.nrss,int(1e10)))):    #max on BOA-bender 499,672,557?!
		
		### get track global position/direction
		track = ss.next_track()

		### decode bitarray
		b   = abs(track.bitarray)      # sign means what?
		j   = int(b / 2e8)             # collided?  history?
		ipt = int(b / 1e6 - j*2e2)     # particle type (1=n,2=p,3=e,4=mu-,9=proton,20=pi_+)
		nsf = int(b - ipt*1e6 - j*2e8) # surface
		
		### get data
		vec = numpy.array([track.u,track.v,track.w])
		pos = numpy.array([track.x,track.y,track.z])
		this_E 	  = track.erg
		this_wgt  = track.wgt
		
		# transform particle origin
		xfm_pos	= numpy.subtract(pos,surface_center)

		### mcnp6
		if 'SF_00001' in ss.kod:
			nsf=track.cs
			ipt=1  #have manually set, IS NOT READ HERE, SCRIPT WILL ASSUME ALL ARE NEUTRONS

		### calculate sense
		if sphere:
			surface_normal	= xfm_pos / numpy.linalg.norm(xfm_pos)
			D 				= numpy.dot(surface_normal,xfm_pos)
			surface_plane	= numpy.array([surface_normal[0],surface_normal[1],surface_normal[2],D])
			sense = surface_plane[0]*xfm_pos[0] + surface_plane[1]*xfm_pos[1] + surface_plane[2]*xfm_pos[2] - surface_plane[3]  # use sense almost zero for on-plane particles since I don't think mcnpx prints which surface its on!
		else:
			sense = surface_plane[0]*pos[0] + surface_plane[1]*pos[1] + surface_plane[2]*pos[2] - surface_plane[3]  # use sense almost zero for on-plane particles since I don't think mcnpx prints which surface its on!


		if  (ipt==1) and (abs(sense)<=1e-5): # (nsf==this_sc): #

			if sphere:
				surface_vec1	= surface_normal[2]/abs(surface_normal[2]) * numpy.subtract(numpy.array([0.0,0.0,D/surface_normal[2]]),xfm_pos)
				surface_vec1	= surface_vec1 / numpy.linalg.norm(surface_vec1)
				surface_vec2	= numpy.cross(surface_normal,surface_vec1)
				this_theta		= numpy.arccos(numpy.dot(surface_normal,vec))
				this_phi		= numpy.arctan2(numpy.dot(surface_vec2,vec),numpy.dot(surface_vec1,vec))
				sphere_vec1		= numpy.array([1.0,0.0,0.0])
				sphere_vec2		= numpy.array([0.0,1.0,0.0])
				sphere_vec3		= numpy.array([0.0,0.0,1.0])
				sphere_theta	= numpy.arccos(surface_normal[2])
				sphere_phi		= numpy.arctan2(surface_normal[1],surface_normal[0])
				if sphere_phi < 0.0:
					sphere_phi = 2.0*numpy.pi + sphere_phi
				this_pos        = numpy.array([sphere_phi,sphere_theta])
				this_vec = numpy.array([numpy.dot(surface_vec1,vec),numpy.dot(surface_vec2,vec),numpy.dot(surface_normal_rot,vec)])
			else:
				### transform vector to normal system
				this_vec = numpy.array([numpy.dot(surface_vec1,vec),numpy.dot(surface_vec2,vec),numpy.dot(surface_normal_rot,vec)])

				### transform position to surface coordinates using basis vectors specified
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
			if (E_dex < len(E_bins)-1) and (theta_dex < len(theta_bins)-1) and (phi_dex < len(phi_bins)-1) and (y_dex < len(y_bins)-1) and (x_dex < len(x_bins)-1 and this_wgt <= max_wgt) :
				count = count+1
				x_avg = x_avg + x_bins[x_dex]
				x_dex_avg = x_dex_avg + x_dex
				dist[E_dex][theta_dex][phi_dex][y_dex][x_dex] = dist[E_dex][theta_dex][phi_dex][y_dex][x_dex] + this_wgt
				histograms_curr[theta_dex].add(this_E,this_wgt)
				histograms_flux[theta_dex].add(this_E,this_wgt/this_vec[2]/surface_area)
				histograms_wght[theta_dex].add(this_wgt,1)
			else:
				if (E_dex >= len(E_bins)-1 and printflag and errorflag): 
					print "E = %6.4E index %i is outside bin boundaries" % (this_E,E_dex)
				if(theta_dex >= len(theta_bins)-1 and printflag and errorflag): 
					print "theta = %6.4E index %i is outside bin boundaries" % (this_theta,theta_dex)
				if(phi_dex >= len(phi_bins)-1 and printflag and errorflag): 
					print "phi = %6.4E index %i is outside bin boundaries" % (this_phi,phi_dex)
					print pos,vec
				if(y_dex >= len(y_bins)-1 and printflag and errorflag): 
					print "y = %6.4E index %i is outside bin boundaries" % (this_pos[1],y_dex)
					print pos,vec
				if(x_dex >= len(x_bins)-1 and printflag and errorflag):
					print "x = %6.4E index %i is outside bin boundaries" % (this_pos[0],x_dex)
				if(this_wgt > max_wgt and printflag and errorflag):
					print "wgt = %6.4E is greater than maximum specified weight %6.4E" % (this_wgt,max_wgt)
	print "max weight",wgt_avg
	# update the histograms to calculate error, must be done before nps division!
	for i in range(0,len(theta_bins)-1):
		histograms_curr[i].update()
		histograms_flux[i].update()
		histograms_wght[i].update()
	### normalize dist to nps:
	unit_area = (y_bins[1]-y_bins[0])*(x_bins[1]-x_bins[0])
	surface_nps = abs(track.nps)
	total_weight = 0.0
	total_tracks = 0
	# divide by nps
	for i in range(0,len(theta_bins)-1):
		total_tracks = total_tracks + numpy.sum(histograms_curr[i].counts)
		total_weight = total_weight + numpy.sum(histograms_curr[i].values)
		histograms_curr[i].values = histograms_curr[i].values / surface_nps
		histograms_flux[i].values = histograms_flux[i].values / surface_nps
	npstrack_ratio = surface_nps/total_tracks
	# divide dists array
	if fluxflag:
		dist = dist / surface_nps / unit_area
	else:
		dist = dist / surface_nps


	### dump array to file
	if printflag:
		print "\n============================\n"
		print "writing binned array to file 'dist'... "
	f = open('dist','wf')
	d = {}
	d['dist']=dist
	d['E_bins']=E_bins
	d['x_bins']=x_bins
	d['y_bins']=y_bins
	d['theta_bins']=theta_bins
	d['phi_bins']=phi_bins
	d['surface_plane']=surface_plane
	d['surface_center']=surface_center
	d['surface_normal']=surface_normal
	d['surface_vec1']=surface_vec1
	d['surface_vec2']=surface_vec2
	d['surface_normal_rot']=surface_normal_rot
	d['surface_vec1_rot']=surface_vec1_rot
	d['surface_vec2_rot']=surface_vec2_rot
	d['xy_rotation_degrees']=xy_rotation_degrees
	d['yz_rotation_degrees']=yz_rotation_degrees
	d['surface_nps']=surface_nps
	d['total_weight']=total_weight
	d['total_tracks']=total_tracks
	d['npstrack_ratio']=npstrack_ratio
	d['this_sc']=this_sc
	d['histograms_curr']=histograms_curr
	d['histograms_flux']=histograms_flux
	d['histograms_wght']=histograms_wght
	d['spec_res']=spec_res
	d['max_wgt']=max_wgt
	if sphere:
		d['sphere']=sphere
		d['sphere_radius']=sphere_radius

	cPickle.dump(d,f)
	f.flush()
	f.close()
	if printflag:
		print "Done."

if printflag:
	print "\n============================\n"

if typeflag == 1:
	ss.close()


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)

# conversion factors
charge_per_amp = 6.241e18
charge_per_milliamp = charge_per_amp/1e3
charge_per_microamp = charge_per_amp/1e6
Na     = 6.0221409e+23  # number/mol

unit_area = (y_bins[1]-y_bins[0])*(x_bins[1]-x_bins[0])

### images
zap_x1=[-6.6, -19.1, -19.1, -6.6, -6.6]
zap_x2=[4.6,19.1 ,19.1 ,4.6, 4.6]
zap_y=[7.05, 7.05 ,-7.05, -7.05, 7.05]
x_AMOR=[2.5,2.5,-2.5,-2.5,2.5]
y_AMOR=[-6,6,6,-6,-6]
x_FOCUS=[-1.76,-1.76,-6.76,-6.76,-1.76]
y_FOCUS=[-6,6,6,-6,-6]
upper_lim=[5e7,2e6,1e5]
for theta_bin in range(0,len(theta_bins)-1):
	for E_bin in range(0,len(E_bins)-1):
		f = plt.figure()
		ax = f.add_subplot(111)
		if fluxflag:
			imgplot = ax.imshow(dist[E_bin][theta_bin][phi_bin][:][:]/unit_area*charge_per_milliamp,extent=[x_bins[0],x_bins[-1],y_bins[0],y_bins[-1]],origin='lower',cmap=plt.get_cmap('jet'))
			this_weight = numpy.sum(dist[E_bin][theta_bin][phi_bin][:][:])/((y_bins[-1]-y_bins[0])*(x_bins[-1]-x_bins[0]))*charge_per_milliamp
		else:
			imgplot = ax.imshow(dist[E_bin][theta_bin][phi_bin][:][:]*charge_per_milliamp          ,extent=[x_bins[0],x_bins[-1],y_bins[0],y_bins[-1]],origin='lower',cmap=plt.get_cmap('jet'),norm=LogNorm(vmin=1e3, vmax=upper_lim[E_bin]))
			this_weight = numpy.sum(dist[E_bin][theta_bin][phi_bin][:][:]*charge_per_milliamp)
		imgplot.set_interpolation('nearest')
		theta_deg = theta_bins[theta_bin:theta_bin+2]*180.0/numpy.pi
		phi_deg = phi_bins[phi_bin:phi_bin+2]*180.0/numpy.pi
		E_meV   = E_bins[E_bin:E_bin+2]*1.0e9
		E_eV   = E_bins[E_bin:E_bin+2]*1.0e6
		if sphere:
			ax.set_ylabel(r'Spherical Polar $\theta$ (rad.)')
			ax.set_xlabel(r'Spherical Azimuthal $\phi$ (rad.)')
		else:
			ax.set_ylabel(r'y (cm)')
			ax.set_xlabel(r'x (cm)')
		#ax.plot(x_FOCUS,y_FOCUS,'0.5',linewidth=4,linestyle='--')
		#ax.set_title(r'Energies %4.2f - %4.2f meV \\       $\theta$ %4.2f - %4.2f $^{\circ}$, $\phi$ %4.2f - %4.2f $^{\circ}$ \\ nps %d tracks %d \\ total weight/nps %4.2E' % (E_meV[0],E_meV[1],theta_deg[0],theta_deg[1],phi_deg[0],phi_deg[1],int(surface_nps),int(track_count[E_bin]),this_weight))
		ax.grid()
		cbar=pylab.colorbar(imgplot)
		if fluxflag:
			#cbar.set_label(r"n p$^{-1}$ cm$^{-2}$")
			ax.set_title(r'Energies %4.2E - %4.2E eV \\       $\theta$ %4.2f - %4.2f $^{\circ}$, $\phi$ %4.2f - %4.2f $^{\circ}$ \\ Total weight/mAs/cm$^2$ %4.2E' % (E_eV[0],E_eV[1],theta_deg[0],theta_deg[1],phi_deg[0],phi_deg[1],this_weight))
			cbar.set_label(r"n mAs$^{-1}$ cm$^{-2}$")
		else:
			#cbar.set_label(r"n p$^{-1}$")
			ax.set_title(r'Energies %4.2E - %4.2E eV \\       $\theta$ %4.2f - %4.2f $^{\circ}$, $\phi$ %4.2f - %4.2f $^{\circ}$ \\ Total weight/mAs %4.2E' % (E_eV[0],E_eV[1],theta_deg[0],theta_deg[1],phi_deg[0],phi_deg[1],this_weight))
			cbar.set_label(r"n mAs$^{-1}$")
#		ax.plot(zap_x1,zap_y,color=[0.5,0.5,0.5],linewidth=3,linestyle='--')
#		ax.plot(zap_x2,zap_y,color=[0.5,0.5,0.5],linewidth=3,linestyle='--')
		ax.set_xlim([x_bins[0],x_bins[-1]])
		ax.set_ylim([y_bins[0],y_bins[-1]])
		#cbar.set_clim(0, 3e-10)
		#
		# 10
#		#
#		if   theta_bin ==0 and E_bin == 0:
#			cbar.set_clim(0, 1.5e-5) #5e-6)
#		elif theta_bin ==0 and E_bin == 1:
#			cbar.set_clim(0, 7.2e-6)
		#
		# 90
		#
#		if   theta_bin ==0 and E_bin == 0:
#			cbar.set_clim(2.1e-4, 4.1e-4) #5e-6)
#		elif theta_bin ==0 and E_bin == 1:
#			cbar.set_clim(0, 2.6e-4)
#		elif theta_bin ==0 and E_bin == 2:
#			cbar.set_clim(0, 2e-6)
		#cbar.formatter.set_powerlimits((0, 0))
		#cbar.update_ticks()
		f.savefig('dist_e%d_theta%d'%(E_bin,theta_bin))
		pylab.show()
		#
		#
		# plot weight histogram
		f2 = plt.figure()
		ax2 = f2.add_subplot(111)
		make_steps(ax2,histograms_wght[theta_bin].bins,[0],histograms_wght[theta_bin].values,linewidth=1,label='',options=['log'])
		ax2.set_ylabel(r'Number')
		ax2.set_xlabel(r'Weight')
		ax2.grid(1)
		plt.show()

#
#
#
#
#
#
#   COLD/ELSE RATIO PLOT
#
#
#
E_bin=0
surface_area = (x_bins[1]-x_bins[0])*(y_bins[1]-y_bins[0])
print surface_area
ratio_plot=numpy.divide(dist[E_bin][theta_bin][phi_bin][:][:],surface_area/charge_per_milliamp)
#ratio_plot=numpy.divide(dist[E_bin][theta_bin][phi_bin][:][:],dist[E_bin+1][theta_bin][phi_bin][:][:])

#  calculate SANS-I and AMOR average values
S_x=[60.125,65.125]
S_y=[1.0,6.0]
A_x=[63.125,64.125]
A_y=[-6.0,-5]
S_xrange=numpy.multiply(x_bins > S_x[0] ,x_bins < S_x[1])
S_yrange=numpy.multiply(y_bins > S_y[0] ,y_bins < S_y[1])
A_xrange=numpy.multiply(x_bins > A_x[0] ,x_bins < A_x[1])
A_yrange=numpy.multiply(y_bins > A_y[0] ,y_bins < A_y[1])

S_x0=numpy.nonzero(S_xrange)[0][0]
S_x1=numpy.nonzero(S_xrange)[0][-1]
S_y0=numpy.nonzero(S_yrange)[0][0]
S_y1=numpy.nonzero(S_yrange)[0][-1]
A_x0=numpy.nonzero(A_xrange)[0][0]
A_x1=numpy.nonzero(A_xrange)[0][-1]
A_y0=numpy.nonzero(A_yrange)[0][0]
A_y1=numpy.nonzero(A_yrange)[0][-1]

SANS_average=0.0
AMOR_average=0.0
AMOR_n=0
SANS_n=0
print A_x0, A_x1, A_y0, A_y1
print S_x0, S_x1, S_y0, S_y1
for y in range(0,len(y_bins)):
	for x in range(0,len(x_bins)):
		if x>=A_x0 and x<A_x1 and y>=A_y0 and y<A_y1:
			AMOR_average=AMOR_average+ratio_plot[y][x]
			AMOR_n=AMOR_n+1
		if x>=S_x0 and x<S_x1 and y>=S_y0 and y<S_y1:
			SANS_average=SANS_average+ratio_plot[y][x]
			SANS_n=SANS_n+1

SANS_average=SANS_average/SANS_n
AMOR_average=AMOR_average/AMOR_n

print "SANS average",SANS_average
print "AMOR average",AMOR_average

A_xx=[A_x[1],A_x[1],A_x[0],A_x[0],A_x[1]]
A_yy=[A_y[0],A_y[1],A_y[1],A_y[0],A_y[0]]

S_xx=[S_x[1],S_x[1],S_x[0],S_x[0],S_x[1]]
S_yy=[S_y[0],S_y[1],S_y[1],S_y[0],S_y[0]]


# plot
f = plt.figure()
ax = f.add_subplot(111)
imgplot = ax.imshow(ratio_plot ,extent=[x_bins[0],x_bins[-1],y_bins[0],y_bins[-1]],origin='lower',cmap=plt.get_cmap('jet'))#,vmin=0.0,vmax=10.0)
this_weight = numpy.sum(dist[E_bin][theta_bin][phi_bin][:][:]*charge_per_milliamp)
imgplot.set_interpolation('nearest')
theta_deg = theta_bins[theta_bin:theta_bin+2]*180.0/numpy.pi
phi_deg = phi_bins[phi_bin:phi_bin+2]*180.0/numpy.pi
E_meV   = E_bins[E_bin:E_bin+2]*1.0e9
E_eV   = E_bins[E_bin:E_bin+2]*1.0e6
ax.set_ylabel(r'y (cm)')
ax.set_xlabel(r'x (cm)')
ax.grid()
cbar=pylab.colorbar(imgplot)
#ax.set_title(r'\begin{center} Ratio of neutrons $>2\AA$ to neutrons $<2\AA$ at the 6m position \\ AMOR=%1.2E $\bullet$ SANS-I=%1.2E $\bullet$ AMOR/SANS-I=%1.2f \end{center}'%(AMOR_average,SANS_average,AMOR_average/SANS_average))
ax.set_title(r'\begin{center} Neutrons at the 6m position \\ AMOR=%1.2E $\bullet$ SANS-I=%1.2E $\bullet$ AMOR/SANS-I=%1.2f \end{center}'%(AMOR_average,SANS_average,AMOR_average/SANS_average))
cbar.set_label(r"n / cm$^2$ / mA")
ax.plot(zap_x1,zap_y,color=[0.5,0.5,0.5],linewidth=3,linestyle='--')
ax.plot(zap_x2,zap_y,color=[0.5,0.5,0.5],linewidth=3,linestyle='--')
ax.plot(A_xx,A_yy,color=numpy.array([218., 20., 255.])/255.0,linewidth=3,linestyle='--')
ax.plot(S_xx,S_yy,color=numpy.array([218., 20., 255.])/255.0,linewidth=3,linestyle='--')
ax.set_xlim([x_bins[0],x_bins[-1]])
ax.set_ylim([y_bins[0],y_bins[-1]])
pylab.show()




plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)


# load experimental data
if this_sc == 2232:
	g=open('experimental.dat','r')
	exp_wvl = []
	exp_val = []
	for line in g:
	    sline = line.split()
	    exp_wvl.append(float(sline[0]))
	    exp_val.append(float(sline[1]))
	exp_wvl = numpy.array(exp_wvl)
	exp_val = numpy.array(exp_val)
	g.close()


### spectrum plots 
fig  = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
cm  = plt.get_cmap('jet') 
cNorm  = colors.Normalize(vmin=0, vmax=len(theta_bins)-1)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
spec_total = numpy.zeros(histograms_curr[0].values.shape)
err_total  = numpy.zeros(histograms_curr[0].err.shape)
counts_total  = numpy.zeros(histograms_curr[0].values.shape)
for i in range(0,len(theta_bins)-1):
	#if fluxflag:
	#	h = histograms_flux[i].values
	#else:
	h = histograms_curr[i].values
	if wavelength:
		avg    = (to_wavelength(histograms_curr[i].bins[:-1])+to_wavelength(histograms_curr[i].bins[1:]))/2.0
		widths = -numpy.diff(to_wavelength(histograms_curr[i].bins))
		spec = numpy.divide(h,widths)
	else:
		avg    = (histograms_curr[i].bins[:-1]+histograms_curr[i].bins[1:])/2.0
		widths = numpy.diff(histograms_curr[i].bins)
		spec = numpy.divide(h,widths)
		spec = numpy.multiply(spec,avg)
	spec = spec * charge_per_milliamp
	if brightness:
		sa = 2.0 * numpy.pi * ( numpy.cos(theta_bins[i]) - numpy.cos(theta_bins[i+1]) ) 
		spec = spec / sa
	else:
		sa = 1.0
	if fluxflag:
		spec = spec / surface_area
		if sphere:
			spec = spec * 2.0
	else:
		area_total = 1.0
	# accumulate
	spec_total = numpy.add(spec_total,spec*sa)
	counts_total = numpy.add(counts_total,histograms_curr[i].counts)
	err_total  = numpy.add(err_total,numpy.multiply(spec*sa,1.0+histograms_curr[i].err))
	# plot
	colorVal = scalarMap.to_rgba(i)
	if wavelength:
		make_steps(ax1,to_wavelength(histograms_curr[i].bins),[0],spec,options=['lin'],color=colorVal,label=r'$\theta$ = %4.2f - %4.2f (%4.2E sr)'%(theta_bins[i]*180.0/numpy.pi,theta_bins[i+1]*180.0/numpy.pi,2.0 * numpy.pi * ( numpy.cos(theta_bins[i]) - numpy.cos(theta_bins[i+1]) )),linewidth=2)
	else:
		make_steps(ax1,histograms_curr[i].bins,               [0],spec,options=['log'],color=colorVal,label=r'$\theta$ = %4.2f - %4.2f (%4.2E sr)'%(theta_bins[i]*180.0/numpy.pi,theta_bins[i+1]*180.0/numpy.pi,2.0 * numpy.pi * ( numpy.cos(theta_bins[i]) - numpy.cos(theta_bins[i+1]) )),linewidth=2)
#
# total spec
#
# calc error
for j in range(0,len(err_total)-1):
	if spec_total[j] > 0:
		err_total[j]  = (err_total[j]-spec_total[j]) / spec_total[j] 
	else:
		err_total[j] = 0.0
# renomalize to total str
if brightness:
	sa = 2.0 * numpy.pi * ( numpy.cos(theta_bins[0]) - numpy.cos(theta_bins[-1]) )
else:
	sa = 1.0
spec_total = spec_total / sa
# plot
if wavelength:
	make_steps(ax2,to_wavelength(histograms_curr[0].bins),[0],spec_total,options=['lin'],color='b',label=r'$\theta$ = %4.2f - %4.2f (%4.2E sr)'%(theta_bins[0]*180.0/numpy.pi,theta_bins[-1]*180.0/numpy.pi,2.0 * numpy.pi * ( numpy.cos(theta_bins[i]) - numpy.cos(theta_bins[i+1]) )),linewidth=2)
	if this_sc == 2232: 
		ax2.plot(exp_wvl,exp_val*max(spec_total[:-2]),color='r',linewidth=2,drawstyle='steps-mid',label='Experimental')
else:
	#print histograms_curr[0].bins
	make_steps(ax2,histograms_curr[0].bins,               [0],spec_total,options=['log'],color='b',label=r'$\theta$ = %4.2f - %4.2f (%4.2E sr)'%(theta_bins[0]*180.0/numpy.pi,theta_bins[-1]*180.0/numpy.pi,2.0 * numpy.pi * ( numpy.cos(theta_bins[i]) - numpy.cos(theta_bins[i+1]) )),linewidth=2)
	avg = (histograms_curr[i].bins[:-1]+histograms_curr[i].bins[1:])/2.0
	ax2.errorbar(avg,spec_total,yerr=numpy.multiply(err_total,spec_total),linestyle='None',alpha=1.0,color='r')
	if this_sc == 2232: 
		exp_ene = to_energy(exp_wvl)
		diff = -numpy.diff(exp_ene)
		diff = numpy.hstack((diff[0],diff))
		exp_val = numpy.divide(exp_val*0.009398971,diff) # wavelength bin width, constant
		exp_val = numpy.multiply(exp_val,exp_ene)
		exp_val = exp_val / numpy.max(exp_val)
		# integrate the experimental spectrum
		calc_total = integrate_spec_bins(histograms_curr[0].bins,spec_total,[exp_ene[-1],exp_ene[0]])
		# integrate the calculated spectrum over the same interval
		exp_total = integrate_spec_points(exp_ene[::-1],exp_val[::-1],[exp_ene[-1],exp_ene[0]])
		# renormalize
		exp_val = exp_val * calc_total / exp_total
		# plot
		ax2.plot(exp_ene,exp_val,color='r',linewidth=2,drawstyle='steps-mid',label='Experimental')

#
# print sums
#
# undo normalization
spec_total = numpy.multiply(spec_total,widths)
spec_total = numpy.divide(spec_total,avg)
#
print spec_total
print err_total
print counts_total
range1=[0.0,600.0]
this_sum=sum_spec_bins(histograms_curr[0].bins,spec_total,range1)
err_sum=sum_spec_bins(histograms_curr[0].bins,numpy.multiply(spec_total,1.0+err_total),range1)
print "Neutron Population %6.4E - %6.4E MeV = %6.4E [%6.4E]" %  (range1[0],range1[1],this_sum,(err_sum-this_sum)/this_sum)

range1=[0.0,1e-6]
this_sum=sum_spec_bins(histograms_curr[0].bins,spec_total,range1)
err_sum=sum_spec_bins(histograms_curr[0].bins,numpy.multiply(spec_total,1.0+err_total),range1)
print "Neutron Population %6.4E - %6.4E MeV = %6.4E [%6.4E]" %  (range1[0],range1[1],this_sum,(err_sum-this_sum)/this_sum)


range1=[1e-6,600.0]
this_sum=sum_spec_bins(histograms_curr[0].bins,spec_total,range1)
err_sum=sum_spec_bins(histograms_curr[0].bins,numpy.multiply(spec_total,1.0+err_total),range1)
print "Neutron Population %6.4E - %6.4E MeV = %6.4E [%6.4E]" %  (range1[0],range1[1],this_sum,(err_sum-this_sum)/this_sum)


range1=[0.01,600.0]
this_sum=sum_spec_bins(histograms_curr[0].bins,spec_total,range1)
err_sum=sum_spec_bins(histograms_curr[0].bins,numpy.multiply(spec_total,1.0+err_total),range1)
print "Neutron Population %6.4E - %6.4E MeV = %6.4E [%6.4E]" %  (range1[0],range1[1],this_sum,(err_sum-this_sum)/this_sum)


range1=[0.1,600.0]
this_sum=sum_spec_bins(histograms_curr[0].bins,spec_total,range1)
err_sum=sum_spec_bins(histograms_curr[0].bins,numpy.multiply(spec_total,1.0+err_total),range1)
print "Neutron Population %6.4E - %6.4E MeV = %6.4E [%6.4E]" %  (range1[0],range1[1],this_sum,(err_sum-this_sum)/this_sum)





#
#  spectrua plot labels
#
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles,labels,loc=1,prop={'size':12}, ncol=2, bbox_to_anchor=(1.0, 1.1))

handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles,labels,loc=1,prop={'size':12}, ncol=2, bbox_to_anchor=(1.0, 1.1))

if fluxflag and brightness and wavelength:
	label_string = r'Brightness (n mAs$^{-1}$ cm$^{-2}$ \AA$^{-1}$ Str$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
elif fluxflag and brightness:
	label_string = r'Brightness (n mAs$^{-1}$ cm$^{-2}$ log(MeV)$^{-1}$ Str$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
elif fluxflag and wavelength:
	label_string = r'Flux (n mAs$^{-1}$ cm$^{-2}$ \AA$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
elif brightness and wavelength:
	label_string = r'Current (n mAs$^{-1}$ \AA$^{-1}$) Str$^{-1}$'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
elif fluxflag:
	label_string = r'Flux (n mAs$^{-1}$ cm$^{-2}$ log(MeV)$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
elif brightness:
	label_string = r'Current (n mAs$^{-1}$ log(MeV)$^{-1}$ Str$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
elif wavelength:
	label_string = r'Current (n mAs$^{-1}$ cm$^{-2}$ \AA$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
else:
	label_string = r'Current (n mAs$^{-1}$ log(MeV)$^{-1}$)'
	ax1.set_ylabel(label_string)
	ax2.set_ylabel(label_string)
if wavelength:
	xlabel_string = r'Wavelength (\AA)'
	ax1.set_xlabel(xlabel_string)
	ax2.set_xlabel(xlabel_string)
else:
	xlabel_string = r'Energy (MeV)'
	ax1.set_xlabel(xlabel_string)
	ax2.set_xlabel(xlabel_string)
ax1.grid()
ax2.grid()

#if wavelength:
#	ax1.set_xlim([0,20])
#	ax2.set_xlim([0,20])
#else:
#	ax1.set_xlim([1e-10,1e-4])
#	ax2.set_xlim([1e-10,1e-4])
#
#ax2.set_ylim(ax1.get_ylim())


pylab.show()

#
#  make total spatial plot
#
phi_bin = 0
dist_total = numpy.zeros(dist[0][0][0][:][:].shape)
for e in range(0,len(E_bins)-1):
	for t in range(0,len(theta_bins)-1):
		dist_total = numpy.add(dist_total,dist[e][t][phi_bin][:][:])
# make correlated distributions
dist_z=numpy.sum(dist_total,axis=1)  # sum columns [row][column], makes totals for each row 
assert(len(dist_z)==len(y_bins)-1)
# plot
f = plt.figure()
ax = f.add_subplot(111)
if fluxflag:
	imgplot = ax.imshow(dist_total/surface_area,extent=[x_bins[0],x_bins[-1],y_bins[0],y_bins[-1]],origin='lower',cmap=plt.get_cmap('jet'))
else:
	imgplot = ax.imshow(dist_total           ,extent=[x_bins[0],x_bins[-1],y_bins[0],y_bins[-1]],origin='lower',cmap=plt.get_cmap('jet'))
this_weight = numpy.sum(dist_total)#/surface_nps
imgplot.set_interpolation('nearest')
theta_deg = numpy.array([theta_bins[0],theta_bins[-1]])*180.0/numpy.pi
phi_deg = phi_bins[phi_bin:phi_bin+2]*180.0/numpy.pi
E_meV   = numpy.array([E_bins[0],E_bins[-1]])*1.0e9
E_eV   =  numpy.array([E_bins[0],E_bins[-1]])*1.0e6
if sphere:
	ax.set_ylabel(r'Spherical Polar $\theta$ (rad.)')
	ax.set_xlabel(r'Spherical Azimuthal $\phi$ (rad.)')
else:
	ax.set_ylabel(r'y (cm)')
	ax.set_xlabel(r'x (cm)')
ax.set_title(r'Energies %4.2E - %4.2E eV \\       $\theta$ %4.2f - %4.2f $^{\circ}$, $\phi$ %4.2f - %4.2f $^{\circ}$ \\ Total weight/nps %4.2E' % (E_eV[0],E_eV[1],theta_deg[0],theta_deg[1],phi_deg[0],phi_deg[1],this_weight))
ax.grid()
cbar=pylab.colorbar(imgplot)
if fluxflag:
	cbar.set_label(r"n p$^{-1}$ cm$^{-2}$")
else:
	cbar.set_label(r"n p$^{-1}$")
#ax.plot(zap_x1,zap_y,color=[0.5,0.5,0.5],linewidth=3,linestyle='--')
#ax.plot(zap_x2,zap_y,color=[0.5,0.5,0.5],linewidth=3,linestyle='--')
ax.set_xlim([x_bins[0],x_bins[-1]])
ax.set_ylim([y_bins[0],y_bins[-1]])
cbar.formatter.set_powerlimits((0, 0))
cbar.update_ticks()
#f.savefig('dist_e%d_theta%d'%(E_bin,theta_bin))
pylab.show()


#
#  Write CSV files
#


if wavelength:
	name = 'dist_data_wvl.csv'
	print "\nWriting '"+name+"'...\n"
	f=open(name,'w')
	# header
	f.write('UNITS = '+label_string+'\n')
	string = 'Wavelength (A), '
	for k in range(0,len(theta_bins)-1):
		string = string+'      %5.4E - %5.4E deg,'%(theta_bins[k]*180.0/numpy.pi,theta_bins[k+1]*180.0/numpy.pi)
	f.write(string+'\n')
	# data
	for j in range(0,len(histograms_curr[0].bins)-1)[::-1]:
		string = '  %5.4E - %5.4E, '%(to_wavelength(histograms_curr[0].bins[j+1]),to_wavelength(histograms_curr[0].bins[j]))
		for k in range(0,len(theta_bins)-1):
			h = histograms_curr[k]
			avg    =  numpy.sum( to_wavelength(h.bins[j:j+2])) / 2.0
			width  = -numpy.diff(to_wavelength(h.bins[j:j+2]))
			if brightness:
				sa = 2.0 * numpy.pi * ( numpy.cos(theta_bins[k]) - numpy.cos(theta_bins[k+1]) ) 
			else:
				sa = 1.0
			if fluxflag:
				area_total = surface_area
			else:
				area_total = 1.0
			spec = h.values[j]* charge_per_milliamp
			spec = spec / width
			spec = spec / area_total
			spec = spec / sa
			string = string+'     %6.4E,'%(spec)
		f.write(string+'\n')
	f.close()
else:
	name = 'dist_data_ene.csv'
	print "\nWriting '"+name+"'...\n"
	f=open(name,'w')
	# header
	f.write('UNITS = '+label_string+'\n')
	print "surface area ",surface_area
	string = 'Energy (MeV), '
	for k in range(0,len(theta_bins)-1):
		string = string+'      %5.4E- %5.4E deg,'%(theta_bins[k]*180.0/numpy.pi,theta_bins[k+1]*180.0/numpy.pi)
	f.write(string+'\n')
	# data
	for j in range(0,len(histograms_curr[0].bins)-1):
		string = '  %5.4E - %5.4E, '%(histograms_curr[0].bins[j],histograms_curr[0].bins[j+1])
		for k in range(0,len(theta_bins)-1):
			h = histograms_curr[k]
			avg    =  numpy.sum( h.bins[j:j+2]) / 2.0
			width  =  numpy.diff(h.bins[j:j+2])
			if brightness:
				sa = 2.0 * numpy.pi * ( numpy.cos(theta_bins[k]) - numpy.cos(theta_bins[k+1]) ) 
				spec = spec / sa
			else:
				sa = 1.0
			if fluxflag:
				area_total = surface_area 
			else:
				area_total = 1.0
			spec = h.values[j]* charge_per_milliamp
			spec = spec / width
			spec = spec * avg
			spec = spec / area_total
			spec = spec / sa
			if fluxflag and sphere:  # only valid for a *purely absorbing* sphere!
				print "!!!! multiplying spectrum by two for purely absorbing sphere !!!!"
				spec = spec * 2.0
			string = string+'     %6.4E'%(spec)
		f.write(string+'\n')
	f.close()



#
# write mcnp sdef
#

surface_rotation_xy = numpy.arctan(surface_normal[1]/surface_normal[0])*180.0/numpy.pi
#surface_rotation_yz = numpy.arccos(surface_normal[2])  # not implemented yet

offset_factor=-1e-6


# figure out angular probabilities
angular_weight_totals=[]
for k in range(0,len(theta_bins)-1):
    angular_weight_totals.append(numpy.sum(histograms_curr[k].values))
probs = numpy.array(angular_weight_totals)/numpy.sum(angular_weight_totals)
# files
name='dist_data.sdef'
print "\nWriting MCNP SDEF to '"+name+"'..."
if sphere:
	pass
else:
	print "SDEF plane offset by % 3.2E...\n"%offset_factor
f=open(name,'w')
# write easy stuff
f.write('c\n')
f.write('c SDEF from ss2dist.py, '+time.strftime("%d.%m.%Y, %H:%M")+'\n')
f.write('c wssa name = '+filename+'\nc surface = %5d\n'%this_sc)
f.write('c\n')
f.write('sdef    par=n\n')
if sphere:
	f.write('        sur=%5d\n'%this_sc)
	f.write('        axs=0 0 1\n')
	f.write('c        vec=1 0 0\n')
	f.write('c        tr=999\n')
	f.write('        rad=%10.8E\n'%sphere_radius)
else:
	f.write('c        sur=%5d\n'%this_sc)
	f.write('        axs=0 0 1\n')
	f.write('        vec=1 0 0\n')
	f.write('        tr=999\n')
	f.write('        x=0.0\n')
	f.write('        y=fz=d998\n')
	f.write('        z=d997\n')
f.write('        dir=d996\n')
f.write('        erg=fdir=d995\n')
f.write('        wgt=%10.8E\n'%numpy.sum(angular_weight_totals))
f.write('c \n')
f.write('c TRANSFORM\n')
f.write('c \n')
if sphere:
	f.write('c *tr999  % 6.7E  % 6.7E  % 6.7E\n'%(surface_center[0],surface_center[1],surface_center[2]))
	f.write('c         % 6.7E  % 6.7E  % 6.7E\n'%(0,90,90))
	f.write('c         % 6.7E  % 6.7E  % 6.7E\n'%(90,0,90))
	f.write('c         % 6.7E  % 6.7E  % 6.7E\n'%(90,90,0))
else:
	# make vectors for routines
	bins=[]
	values=[]
	for i in range(0,len(y_bins)-1):
		bins.append(  x_bins)
		values.append(dist_total[i][:])  # these bins are linearly spaced, do not need to be divided by width
	# write
	f.write('*tr999  % 6.7E  % 6.7E  % 6.7E\n'%((1.0+offset_factor)*surface_center[0],(1.0+offset_factor)*surface_center[1],(1.0+offset_factor)*surface_center[2]))
	f.write('        % 6.7E  % 6.7E  % 6.7E\n'%(surface_rotation_xy,90-surface_rotation_xy,90))
	f.write('        % 6.7E  % 6.7E  % 6.7E\n'%(90+surface_rotation_xy,surface_rotation_xy,90))
	f.write('        % 6.7E  % 6.7E  % 6.7E\n'%(90,90,0))
	f.write('c \n')
	f.write('c Z\n')
	f.write('c \n')
	make_independent_distribution(f,997,y_bins,dist_z)
	f.write('c \n')
	f.write('c Y, DEPENDENT ON Z\n')
	f.write('c \n')
	make_dependent_distribution(f,998,800,bins,values)
f.write('c \n')
f.write('c ANGULAR DISTRIBUTION\n')
f.write('c \n')
# write angular cards
make_independent_distribution(f,996,numpy.cos(theta_bins)[::-1],probs[::-1])
# write energy cards
f.write('c \n')
f.write('c ENERGY DISTRIBUTIONS, DEPENDS ON DIR\n')
f.write('c \n')
bins=[]
values=[]
for i in range(0,len(histograms_curr))[::-1]:  # must be revered since the cosines are reversed!
	bins.append(  histograms_curr[i].bins  )
	values.append(histograms_curr[i].values)
make_dependent_distribution(f,995,700,bins,values)
f.write('c \n')
f.close()
print "\nDONE.\n"