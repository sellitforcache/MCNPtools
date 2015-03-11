def to_energy(lambda_in):
	### assumes Angstrom, gives MeV
	import numpy
	return numpy.multiply(numpy.power(0.286014369/lambda_in,2) , 1.0e-6)
