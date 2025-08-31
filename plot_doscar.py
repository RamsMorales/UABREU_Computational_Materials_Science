#! $PWD/.venv/bin/python
import numpy as np
import matplotlib.pyplot as plt

doscar = "DOSCAR.vasp"

# 1) Read first 6 lines to get NG (number of energy points)
with open(doscar) as f:
    header = [next(f) for _ in range(6)]
    parts = header[5].split()
    NG = int(parts[2])         # DOSCAR’s 6th line, 3rd column is # of points

# 2) Re‐open and skip header
f = open(doscar)
for _ in range(6):
    next(f)
first_line = next(f).split()
ncols = len(first_line)

# 3) Parse DOS lines
energies = []
dos_tot   = []
dos_up    = []
dos_dn    = []

# rewind back so we read that first line again
f.seek(0)
for _ in range(6):
    next(f)

for i in range(NG):
    line = next(f).split()
    E = float(line[0])
    if ncols == 2:
        # non‐spin‐polarized: [E, DOS_total]
        energies.append(E)
        dos_tot.append(float(line[1]))
    else:
        # spin‐polarized: [E, DOS↑, DOS↓, cum↑, cum↓]
        energies.append(E)
        up = float(line[1])
        dn = float(line[2])
        dos_up.append(up)
        dos_dn.append(dn)
        dos_tot.append(up + dn)

f.close()

energies = np.array(energies)
dos_tot   = np.array(dos_tot)

plt.figure(figsize=(6,4))

if ncols == 2:
    plt.plot(energies, dos_tot, "k")
    plt.ylabel("DOS (states/eV)")
    plt.xlabel("E – EF (eV)")
else:
    dos_up = np.array(dos_up)
    dos_dn = np.array(dos_dn)
    plt.plot(energies, dos_up,   "r", label="DOS ↑")
    plt.plot(energies, -dos_dn,  "b", label="–DOS ↓")
    plt.ylabel("DOS (states/eV)")
    plt.xlabel("E – EF (eV)")
    plt.legend()

plt.axvline(0.0, color="0.5", linestyle="--")
plt.tight_layout()
plt.show()
