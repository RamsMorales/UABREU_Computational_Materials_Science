#! $PWD/.venv/bin/python

import matplotlib.pyplot as plt 
import numpy
import math


# Need: Energy vs kpar and time vs kpar
kpar = []
time = []
energies = []
with open("3x3x3_kpar_time.csv","r") as file:
    count = 0
    for line in file:
        if count == 0:
            count += 1
            continue
        else:
            kpar.append(int(math.pow(int(line.split(',')[0]),1/3)))
            time.append(float(line.split(',')[1]))
file.close()

with open("energies_3x3x3_kpar.txt","r") as file:
    for line in file:
        energies.append(float(line))

#print(energies,kpar, time)


#Plot Energy vs Kpar
plt.bar(kpar,energies)
plt.title("Energy vs KPAR 3x3x3 CoCrFeMnNi 10 cores")
plt.ylabel("Energy eV")
plt.xlabel(f"K Points_x")

# Only show ticks at the bar locations
plt.xticks(kpar)

# Limit x-axis range to reduce whitespace
plt.xlim(min(kpar) - 1, max(kpar) + 1)
plt.show()

#Plot time vs KPAR
plt.bar(kpar,time)
plt.title("Time vs KPAR 3x3x3 CoCrFeMnNi 10 cores")
plt.ylabel("Time s")
plt.xlabel(f"K Points_x")

# Only show ticks at the bar locations
plt.xticks(kpar)

# Limit x-axis range to reduce whitespace
plt.xlim(min(kpar) - 1, max(kpar) + 1)

plt.show()
