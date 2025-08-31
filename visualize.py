#! $PWD/.venv/bin/python

import matplotlib.pyplot as plt
import os
import re

energies = []
latice_constants = []
pattern = re.compile(r"E0= \-?\.\d{1,}E\+\d{1,}")



with open("SUMMARY.fcc","r") as file:
    for line in file:
        lattice_constant = re.match(r"\d{1,}\.\d",line)
        energy = re.search(pattern,line)
        #print(f"Found lattice constant: {lattice_constant.group()}")
        #print(f"Found energy: {float(str(energy.group()).split()[1])}")
        latice_constants.append(float(lattice_constant.group()))
        energies.append(float(str(energy.group()).split()[1]))
plt.scatter(latice_constants,energies)
plt.show()









