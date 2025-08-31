#! $PWD/.venv/bin/python

import argparse
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

def main():
    # 1) parse CLI arguments
    parser = argparse.ArgumentParser(
        description="Overlayed distribution histograms with range in legend"
    )
    parser.add_argument("--data","-in",default="energy",help="Type of distribution displayed. Example \"energy\" or \"volume\"",required=True)
    parser.add_argument("INPUT_FILE", help=f"Path to [INPUT FILE].txt")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--crystal", "-c",
        metavar="CRYSTAL",
        help="Specify crystal structure (this disables -a1/-a2)"
    )
    parser.add_argument(
        "--atom1", "-a1",
        default="Cr",
        help="Optional - Symbol of the first atom (default: Cr)"
    )
    parser.add_argument(
        "--atom2", "-a2",
        default="Fe",
        help="Optional - Symbol of the second atom (default: Fe)"
    )
    parser.add_argument(
        "--outdir", "-o",
        default="~/Projects/vasp_TEST/plots/",
        help="Optional - Directory to save the figure (created if missing)"
    )
    args = parser.parse_args()

    # 2) ensure output folder exists
    outdir = Path(os.path.expanduser(args.outdir))
    outdir.mkdir(parents=True, exist_ok=True)

    # 3) read in energies
    energies = []
    count= 0
    with open(args.INPUT_FILE, "r") as f:
        for line in f:
            count += 1
            line = line.strip()
           # print(count,line)
            if not line or line.startswith("(will"):
                continue
            energies.append(float(line))
    
    perturbation_parameters = [(1e-2,1e-2),(5e-2,2e-2),(1e-1,3e-2),(2e-1,5e-2)]
    # Energy palette: cool blue → light blue → pale gold → UAB gold
    energy_colors = [
        "#002244",  # darkest cool blue
        "#4A90E2",  # bright sky blue
        "#FFB347",  # warm orange
        "#FDB81C"   # UAB gold
    ]

    volume_colors = [
        "#001F3F",  # deep navy
        "#00AABB",  # vivid teal-blue
        "#FFCC66",  # soft amber
        "#FDB81C"   # UAB gold
    ]

    # prep metadata
    data_class = args.data
    if data_class == "volume":
        units = "$Å^3$"
        alphas = volume_colors
        loc = "upper left"
    elif data_class == "energy":
        units = "eV"
        alphas = energy_colors
        loc = "upper right"
    else:
        raise ValueError("Please input energy or volume for -in or --data")
    if args.crystal:
        title = f"{data_class.capitalize()} Spread for {args.crystal}"
        png_name = f"{args.crystal}_{data_class}_Dist.png"
        subset_lengths = [0, 750, 1500, 2250, len(energies)]
    else:
        a1, a2 = args.atom1, args.atom2
        title = f"{data_class.capitalize()} Spread for 50% {a1} 50% {a2} FCC 2x2x2 Kpoints 5x5x5"
        png_name = f"{a1}{a2}_{data_class}_Dist.png"    
        subset_lengths = [0, 250, 500, 750, len(energies)]

    out_path = outdir / png_name

    plt.style.use('default')

    # compute global bins once
    bin_edges = np.histogram_bin_edges(energies, bins="fd")

    # cutoff percentiles
    p_low, p_high = np.percentile(energies, [1,97])
    n_below = np.sum(np.array(energies) < p_low)
    n_above = np.sum(np.array(energies) > p_high)

    # build figure with grid and cleaned spines
    fig, ax = plt.subplots(figsize=(12,6))
    ax.grid(axis='y', linestyle=':', linewidth=0.5, alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # plot each subset clipped to [p_low,p_high]
    for j in range(1, len(subset_lengths)):
        data = np.array(energies)[ subset_lengths[j-1] : subset_lengths[j] ]
        #print(data,len(data))
        disp = data[(data >= p_low) & (data <= p_high)]
        alpha_val = 0.7 if j < len(subset_lengths)-1 else 0.5
        ax.hist(
            disp,
            bins=bin_edges,
            range=(p_low, p_high),
            rwidth=0.9,
            histtype="stepfilled",
            color=alphas[j-1],
            alpha=alpha_val,
            edgecolor='white',
            linewidth=0.5,
            label=f"{perturbation_parameters[j-1][0]}Å, {perturbation_parameters[j-1][1]}% shear "
                  f"range {np.ptp(data):.2f} {units}"
        )

    # 8) finalize
    ax.set_xlim(p_low, p_high)
    ax.set_xlabel(f"{data_class.capitalize()} in {units}", fontsize=14)
    #ax.set_ylabel("Count", fontsize=14)
    ax.set_title(title, fontsize=16)
    ax.tick_params(axis='both', labelsize=16)
    ax.text(0.75, 0.25,
            f"{n_below} clipped  |  {n_above} clipped",
            transform=ax.transAxes, va="top", fontsize=16)
    ax.legend(frameon=False, fontsize=16, loc=loc)
    plt.tight_layout()

    # 9) save
    plt.savefig(out_path, dpi=200)
    print(f"Saved overlaid histogram to {out_path}")  

if __name__ == "__main__":
    main()
