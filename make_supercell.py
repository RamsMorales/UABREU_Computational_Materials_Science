#! $PWD/.venv/bin/python3
from ase.build import bulk
from ase.build.supercells import make_supercell
import dpdata as dp
import numpy as np
import os

### Global vars
starting_atom = 'Fe'
replacement_atom = 'Fe'
crystal_type = 'fcc'
lattice_constant = 3.52
replacement_gradient = [0.5]#[0,0.25,0.5,0.75,1]
perturbation_parameters = [(1e-2,1e-2)]#,(1e-2,1e-2),(5e-2,2e-2),(1e-1,3e-2),(2e-1,5e-2)]
num_perturbations = 1 
super_cell_side_length = 2
num_replacements = 1


### Creating initial system
primitive_crystal = bulk(name=starting_atom,crystalstructure=crystal_type,
                         a=lattice_constant, cubic=True)

### Building super-cell
super_cell = make_supercell(prim=primitive_crystal,P=np.eye(3) * super_cell_side_length)


## Replace atoms randomly
for replacement_percent in replacement_gradient:

    #Making Sub directory for percent replacement
    top_dir_name = f"{replacement_percent}{starting_atom}_{1 - replacement_percent}{replacement_atom}"
    top_output_dir = os.path.join(os.getcwd(),top_dir_name)
    if not os.path.exists(top_output_dir):
        os.mkdir(top_output_dir)
    count = 1
    for perturbation_parameter in perturbation_parameters:

        ## Making TOP directory to store POSCAR files
        sub_dir_name = f"{perturbation_parameter[0]}A-{perturbation_parameter[1]}p"
        output_dir = os.path.join(top_output_dir,sub_dir_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)



        for i in range (num_replacements):
            ### Converting to dpData format
            dp_system = dp.System(super_cell,fmt="ase/structure")

            if replacement_percent != 0:
                dp_system.replace(initial_atom_type=starting_atom
                                  ,end_atom_type=replacement_atom
                                  ,replace_num=int(super_cell.get_global_number_of_atoms() * replacement_percent))

            ## Perturbation
            perturbed_systems = dp_system.perturb(num_perturbations,
                                              perturbation_parameter[0],
                                              perturbation_parameter[1])
            for system in perturbed_systems:
                system_name = "".join([starting_atom,replacement_atom,"_",crystal_type, str(count),".vasp"])
                system.to_poscar(os.path.join(output_dir,system_name))
                count += 1
    #TODO












    ### overwriting offset feature

    ### replace multiple times within



