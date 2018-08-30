def to_energy(lambda_in):
	### assumes Angstrom, gives MeV
	import numpy
	#return numpy.multiply(numpy.power(0.286014369/lambda_in,2) , 1.0e-6)
	return numpy.divide( 2.86014369e-4*2.86014369e-4 , numpy.multiply(lambda_in,lambda_in)  )
