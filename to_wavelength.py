def to_wavelength(E_in):
	### assumes MeV, gives Angstrom
	import numpy
	return numpy.divide(2.86014369e-4, numpy.sqrt(numpy.array(E_in)))