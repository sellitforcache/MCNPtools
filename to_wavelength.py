def to_wavelength(E_in):
	### assumes MeV, gives Angstrom
	import numpy
	return numpy.divide(0.286014369, numpy.sqrt(numpy.multiply(E_in,1.0e6)))