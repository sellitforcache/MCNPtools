from MCNPtools import calculate_materials

# y2o3
# hack to add this :/  should make things a little more general
calculate_materials.z_number['Y2O3']=999000
y2o3=calculate_materials.element('Y2O3')
y2o3.add_isotope_atom(89,88.905848,200.0)
y2o3.add_isotope_atom(16,15.994915,299.271)
y2o3.add_isotope_atom(17,16.999132,0.114)
y2o3.add_isotope_atom(18,17.999160,0.615)
temp = {}
temp[39089] = [y2o3.atom_fractions[999089][0],y2o3.atom_fractions[999089][1]]
temp[8016]  = [y2o3.atom_fractions[999016][0],y2o3.atom_fractions[999016][1]]
temp[8017]  = [y2o3.atom_fractions[999017][0],y2o3.atom_fractions[999017][1]]
temp[8018]  = [y2o3.atom_fractions[999018][0],y2o3.atom_fractions[999018][1]]
y2o3.atom_fractions = copy.deepcopy(temp)
y2o3.finalize()
