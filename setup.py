#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

extensions = [
    Extension("MCNPtools.ace", ["src/ace.pyx"],
        include_dirs=[numpy.get_include()])
]
setup(name='MCNPtools',
      version='0.1',
      description='Python scripts that are useful analyzing MCNP results and creating some ww for inputs in new runs.',
      author='Ryan M. Bergmann',
      author_email='ryanmbergmann@gmail.com',
      url='https://github.com/sellitforcache/MCNPtools',   
      py_modules = ['MCNPtools.mctal',
                    'MCNPtools.tally',
                    'MCNPtools.calculate_materials',
                    'MCNPtools.plot',
                    'MCNPtools.to_energy',
                    'MCNPtools.to_wavelength',
                    'MCNPtools.to_temperature',
                    'MCNPtools.ace'
                    ],
      package_dir = {'MCNPtools': 'src'},
      cmdclass = {'build_ext': build_ext},
      include_dirs = [numpy.get_include()],
      ext_modules = extensions
     )