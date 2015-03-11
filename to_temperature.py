def to_temperature(E_in):
	### assumes MeV, gives kelvin
	import numpy
	return numpy.multiply(11604.50520 , 1.0e6*E_in)