#! $PWD/.venv/bin/python

import dpdata as dp
from ase.build import bulk
from ase.build.supercells import make_supercell
from Utils.Supercell_Utils import generate_dictionary
from Utils.Supercell_Utils import HEA_supercell_replacement
import numpy as np
import os

### Crystal Parameters
atom_species = ['Co','Cr','Fe','Mn','Ni']
crystal_name = "".join(atom_species)
crystal_type = 'fcc'
lattice_constant = 3.52

### Structure Generation Parameters
#replacement_gradient = [0,0.25,0.5,0.75,1]
perturbation_parameters = [(1e-2,1e-2),(5e-2,2e-2),(1e-1,3e-2),(2e-1,5e-2)]
num_perturbations = 75
super_cell_side_length = 3
num_replacements = 10


###############################################################################
Toggle = True #Toggle to write submission.sh scripts for Calculation
###############################################################################
### Job Submission Parameters
total_jobs = num_perturbations * num_replacements * len(perturbation_parameters)
num_submissions = 20
submission_chunks = int(total_jobs / num_submissions)
#-------------------------------------------------------------------------------#
partition = "normal"
nNodes = 10
nCores = 560
hours, minutes, seconds = "11","00","00"
wall_time = f"{hours}:{minutes}:{seconds}"

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
### Creating initial system
primitive_crystal = bulk(name=atom_species[0],crystalstructure=crystal_type,
                         a=lattice_constant, cubic=True)
### Building super-cell
super_cell = make_supercell(prim=primitive_crystal,P=np.eye(3) * super_cell_side_length)

atom_distributions = generate_dictionary(atom_species,108)

count = 1
for perturbation_parameter in perturbation_parameters:

            ## Making TOP directory to store POSCAR files
            sub_dir_name = f"{perturbation_parameter[0]}A-{perturbation_parameter[1]}p"
            output_dir = os.path.join(os.getcwd(),crystal_name,sub_dir_name)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            for i in range (num_replacements):
                ### Converting to dpData format
                dp_system = dp.System(super_cell,fmt="ase/structure")

                dp_system = HEA_supercell_replacement(dp_system,atom_distributions)

                ## Perturbation
                perturbed_systems = dp_system.perturb(num_perturbations,
                                                  perturbation_parameter[0],
                                                  perturbation_parameter[1])
                for system in perturbed_systems:
                    system_name = "".join([crystal_name,"_",crystal_type, str(count),".vasp"])
                    system.to_poscar(os.path.join(output_dir,system_name))
                    count += 1

if Toggle:
    # Writing an automatic bash script writer
    #print(total_jobs,submission_chunks)
    for i in range(num_submissions):
        submission_file_name = f"submit_{i+1}.sh"
        with open(os.path.join(os.getcwd(),crystal_name,submission_file_name),"w") as file:
            file.write("#!/bin/bash\n")
            file.write("\n")
            file.write(f"#SBATCH -J {i+1}_{crystal_name}_{total_jobs}_Perts        # Job name\n")
            file.write(f"#SBATCH -o job_{i+1}.out                 # stdout\n")
            file.write(f"#SBATCH -e job_{i+1}.err                 # stderr\n")
            file.write(f"#SBATCH -p {partition}                        # partition\n")
            file.write(f"#SBATCH -N {nNodes}                             # nodes per job\n")
            file.write(f"#SBATCH -n {nCores}                           # MPI ranks per job\n")
            file.write(f"#SBATCH -t {wall_time}                      # wall time\n")
            file.write("#SBATCH --begin=now+0hour\n")
            file.write("#SBATCH --mail-user=myname@myschool.edu\n")
            file.write("#SBATCH --mail-type=FAIL                 # on failure\n")
            file.write("#SBATCH -A PHY20015                      # allocation name\n")
            file.write("\n")
            file.write("source ~cazes/texascale_settings.sh\n")
            file.write("\n")
            file.write(f"SPECIES=\"{crystal_name}\"\nRUN_DIR=\"$SCRATCH/$SPECIES/{i+1}\"\nmkdir -p \"$RUN_DIR\"\n")
            file.write(f"DEST_DIR=\"$WORK/$SPECIES/outcars\"\nmkdir -p \"$DEST_DIR\"\n")
            file.write("\n")
            file.write(f"START={(i*submission_chunks)+1}\n")
            file.write(f"END={submission_chunks*(i+1)}\n")
            file.write("\n")
            file.write("BASE_DIR=$(pwd)\n")
            file.write("\n")
            file.write("cp ./INCAR ./KPOINTS ./POTCAR \"$RUN_DIR\"\n")
            file.write("\n")
            file.write("for ((i=START; i<=END; i++)); do\n")
            file.write("    cd \"$BASE_DIR/$COMPOSITION\"\n")
            file.write("    vaspfile=$(find . -type f -name \"${SPECIES}_fcc${i}.vasp\" -print -quit)\n")
            file.write("    if [[ -z \"$vaspfile\" ]]; then\n")
            file.write("        echo \"Warning: no file for index $i\" >&2\n")
            file.write("        continue\n")
            file.write("    fi\n")
            file.write("    echo \"starting job ${i}\" >&2\n")
            file.write("    cp \"$vaspfile\" \"$RUN_DIR\"/POSCAR\n")
            file.write("    cd \"$RUN_DIR\"\n")
            file.write("    time ibrun -n $SLURM_NTASKS vasp_std\n")
            file.write("    echo \"Job ${i} done or failed\" >&2\n")
            file.write("    mv OUTCAR \"$DEST_DIR\"/OUTCAR${i}\n")
            file.write("    cd \"$BASE_DIR\"\n")
            file.write("done\n")
            file.write("\n")

