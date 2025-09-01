#! $PWD/.venv/bin/python
import random
import ase
import dpdata as dp
import itertools

"""
The goal of this code is to make two methods:

method 1: compute the total number of atoms per sub-species given k 
sub-species and n total atoms. Such that we have "even" distribution of
each species.

method 2: given a dictionary of {atom: num_atoms}, System of size n -> system 
containing randomly replaced with each atom in {atoms: num_atoms}. 

"""

def generate_dictionary(atoms : list, total_num_atoms)-> dict:
    
    result = {}
    initial_occupation = total_num_atoms // len(atoms)

    # step 1 divide atoms into even spread
    for atom in atoms:
        result[atom] = initial_occupation

    # compute the number of sub-groups that need more atoms
    num_over_groups = total_num_atoms % len(atoms)

    if num_over_groups == 0:
        return result

    # randomly select atoms in the list of atoms to become over group
    overloaded_atoms = random.sample(list(result),num_over_groups)

    for atom in overloaded_atoms:
        result[atom] += 1

    return result

def HEA_supercell_replacement(super_cell :dp.System, atom_distributions: dict ) -> dp.System:
    starting_atom = super_cell.get_atom_names()[0]
    for current_atom in atom_distributions:
        if current_atom != starting_atom:
            super_cell.replace(starting_atom,current_atom,atom_distributions[current_atom])

    return super_cell

def list_combinations(atoms: list, k_comb: int) -> list:
    combinations = []
    for comb in itertools.combinations(atoms,k_comb):
        combinations.append(comb)
    return combinations

def print_todo(combinations: list):

    """
    Expects a list of tuples with combinations of size k HEA groups.

    Prints ordered list to std.out
    """
    i = 1
    for comb in combinations:
        print(i,''.join(comb))
        i += 1

