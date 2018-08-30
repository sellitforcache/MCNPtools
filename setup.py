#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

extensions = [
    Extension("ace", ["MCNPtools/ace.pyx"],
        include_dirs=[numpy.get_include()])
]
setup(name='MCNPtools',
      version='0.1',
      description='Python scripts that are useful analyzing MCNP results and creating some ww for inputs in new runs.',
      author='Ryan M. Bergmann',
      author_email='ryanmbergmann@gmail.com',
      url='https://github.com/sellitforcache/MCNPtools',
      packages=['MCNPtools'],  # include all packages under src
      cmdclass = {'build_ext': build_ext},
      include_dirs = [numpy.get_include()],
      ext_modules = extensions,
      scripts=['MCNPtools/convert2singlefile.py','MCNPtools/'],
      license="BSD3",
     )
