import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 1) List of your ten energy‐distribution PNGs, in display order
'''
files = [
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoCr_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoFe_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoMn_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoNi_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CrFe_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CrMn_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CrNi_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/FeMn_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/FeNi_energy_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/MnNi_energy_Dist.png",
]
'''

files = [
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoCr_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoFe_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoMn_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CoNi_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CrFe_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CrMn_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/CrNi_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/FeMn_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/FeNi_volume_Dist.png",
    "/Users/ramsonmunoz/Projects/vasp_TEST/plots/MnNi_volume_Dist.png",
]

# 2 columns × 5 rows
n_cols, n_rows = 2, 5

# figsize in inches = (total width, total height)
fig = plt.figure(figsize=(6.5, 6.5))

# create the grid of axes manually so that each cell is exactly 3.25×1.30 in
cell_w, cell_h = 3.25/6.5, 1.30/6.5  # fractions of figure
for idx, fname in enumerate(files):
    col = idx % n_cols
    row = idx // n_cols
    # [left, bottom, width, height] in figure‐fraction coordinates
    left   = col * cell_w
    bottom = 1 - (row+1)*cell_h     # Matplotlib’s origin is bottom‐left
    ax = fig.add_axes([left, bottom, cell_w, cell_h])
    ax.imshow(mpimg.imread(fname), aspect='equal')
    ax.axis('off')

plt.savefig("combined_2x5_exact.png", dpi=300, bbox_inches="tight")
plt.show()
