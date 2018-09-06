# MCNPtools
Ryan M. Bergmann, 2018.

Python scripts that are useful for streamlining MCNP runs, managing material definition data, analyzing MCNP results, and creating weight windows from flux maps.

Contains:
* Mctal and Tally classes to parse mctal files.  Mctal class contains a method that can write weight windows based on mesh tally results
* calculate_materials module that provides a Mixture class and useful data to perform general mixing of materials and then print MCNP input cards from the results
* convert2singlefile.py script that inlines all 'read file' lines of a MCNP input file.  It also automatically wraps lines at 80 characters.


## Installation

```
$ python setup.py install
```

This will install the MCNPtools module into your local Python distribution.  It will also install the convert2singlefile.py script into your userbase/bin directory.

## Usage

Usage examples can be found in the _examples_ folder.  Each folder contains its own README.md file.
