the MCNPtools package contains a module called "calculate_materials", which in turn contains a class called "mixtures", which is the base of all the module functionality.  The recommended usage is to import the module and instantiate classes from the module namespace since this gives easier access to the class-wide variables.  The point of the mixture class abstraction is to build mixtures on top of one another.  I.e. once a mixture is made, it can be used in another mixture as one of its bases.  Natural elemental composition are already built when the module is imported.

The class has a global static dictionary that stores references to all instances, so the mixtures can simply be referred to by name [string].

The class also has a method that prints MCNP material definition cards:  ```mixture.print_material_card()```

```python
from MCNPtools import calculate_materials
from MCNPtools import material_collection
from MCNPtools import compounds
#
#  dry air @ 20 degC
#
dryair = calculate_materials.mixture('dry air')   # 'dry air' is the name string that can be used when adding this mixture to another mixture
dryair.mass_density=0.00120479
dryair.add_mixture('C' , 0.000150, mode='atom')
dryair.add_mixture('N' , 0.784431, mode='atom')
dryair.add_mixture('O' , 0.210748, mode='atom')
dryair.add_mixture('Ar', 0.004671, mode='atom')
dryair.finalize()
#
#  light water
#
light_water = calculate_materials.mixture('light water')
light_water.add_mixture( 'O', 1.0, mode='atom')
light_water.add_mixture( 'H', 2.0, mode='atom')
light_water.mass_density=1.0
light_water.finalize()
#
#  45% RH air @ 24 degC
#
air_45RH_24C = calculate_materials.mixture('air 45RH 24C')
air_45RH_24C.mass_density=0.0011935
air_45RH_24C.add_mixture('dry air'     , 0.99172, mode='mass') # using the prescribed name strings to add to the new mixture
air_45RH_24C.add_mixture('light water' , 0.00828, mode='mass') # if a mixture has been made, its name string can be used here
air_45RH_24C.finalize()
#
# print material card for MCNP
#
calculate_materials.print_type='atom' # can also be 'mass' for print mass fractions instead of atom fractions
air_45RH_24C.print_material_card()
```

There is also an exmaple file, _calc_mats.py_, that can simply be executed after the MCNPtools package is installed to show functionality.
