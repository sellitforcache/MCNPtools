class tally:
	m # tally name number
	i # i>0 particle type, i<0 i=number of particle type, list following
	j # j=type of detector tally (0=none)
	tally_p = []
	comment = 


class mctal:
	### static mappings
	particles={
		1 	: ['neutron' 				, 'n' ],
		-1 	: ['anti-neutron' 			, '-n'],
		2 	: ['photon' 				, 'p' ],
		3	: ['electron' 				, 'e' ],
		-3	: ['positron' 				, '-e'],
		4	: ['muon-' 					, '|' ],
		-4 	: ['anti-muon-' 			, '-|'],
		5 	: ['tau'					, '*' ],
		6 	: ['electron neutrino'		, 'u' ],
		-6 	: ['anti-electron neutrino'	, '-u'],
		7 	: ['muon neutrino'			, 'v' ],
		8 	: ['tau neutrino'			, 'w' ],
		9 	: ['proton' 				, 'h' ],
		-9 	: ['anti-proton' 			, '-h'],
		10 	: ['lambda0' 				, 'l' ],
		11 	: ['sigma+'					, '+' ],
		12 	: ['sigma-'					, '-' ],
		13 	: ['cascade+'				, 'x' ],
		14 	: ['caccade-'				, 'y' ],
		15 	: ['omega-' 				, 'o' ],
		16 	: ['lambda_c+'				, 'c' ],
		17 	: ['cascade_c+'				, '!' ],
		18 	: ['cascade_c0'				, '?' ],
		19 	: ['lambda_b0'				, '<' ],
		20 	: ['pion+' 					, '/' ],
		-20 : ['pion-' 					, '-/'],
		21 	: ['pion0'					, 'z' ],
		22 	: ['kaon+'					, 'k' ],
		-22 : ['kaon-'					, '-k'],
		23 	: ['K0 short'				, '%' ],
		24 	: ['K0 long'				, '^' ],
		25 	: ['D+'						, 'g' ],
		26 	: ['D0'						, '@' ],
		27 	: ['D_s+'					, 'f' ],
		28 	: ['B+'						, '>' ],
		29	: ['B0' 					, 'b' ],
		30	: ['B_s0' 					, 'q' ],
		31	: ['deuteron' 				, 'd' ],
		32	: ['triton' 				, 't' ],
		33	: ['helium-3' 				, 's' ],
		34	: ['helium-4' 				, 'a' ],
		35	: ['heavy ions' 			, '#' ]
	}	
	### mctal data
	kod # the name of the code, MCNPX.
	ver # the version, 2.7.0.
	probid # the date and time when the problem was run and, if it is available, the designator of the machine that was used.
	knod # the dump number.
	nps # the number of histories that were run.
	rnr # the number of pseudorandom numbers that were used.
	title # the input title card
	ntal = 0  # number of tallies
	tally_n = [] # list of tally name numbers
	npert = 0  # number of perturbations
	
