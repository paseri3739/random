import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
import sys
import argparse
import math
import numpy as np

# Regular expression pattern for matching atomic coordinates
PATTERN = r"([A-Za-z]{1,2})\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)"


def open_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines


def match_coordinates(line):
    return re.match(PATTERN, line)


def parse_line(line):
    match = match_coordinates(line)
    if match:
        atom, x, y, z = match.groups()
        x, y, z = map(float, [x, y, z])
        return (atom, x, y, z)
    return None


def is_new_molecule(line):
    return line.startswith("--Link1--")


def parse_gaussian_file(filename):
    lines = open_file(filename)

    molecules = []
    molecule = []
    for line in lines:
        coord = parse_line(line)
        if coord:
            molecule.append(coord)
        elif is_new_molecule(line):
            molecules.append(molecule)
            molecule = []
    if molecule:
        molecules.append(molecule)

    return molecules


def get_plot_dimensions(num_molecules):
    return int(math.ceil(math.sqrt(num_molecules)))


def plot_2d_molecule(ax, molecule, index):
    atoms, x, y, z = zip(*molecule)
    ax.plot(x + x[:1], y + y[:1], color="blue")  # Plot line (with line from last point to first)
    ax.scatter(x, y, color="red", s=100)  # Plot points
    for j in range(len(x)):  # Add labels
        ax.text(x[j], y[j], f"{atoms[j]}{j + 1}", color="green", fontsize=12)
    ax.set_title(f"Cluster {index+1}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")


def plot_3d_molecule(ax, molecule, index):
    atoms, x, y, z = zip(*molecule)
    ax.plot(x + x[:1], y + y[:1], z + z[:1], color="blue")  # Plot line (with line from last point to first)
    ax.scatter(x, y, z, color="red", s=100)  # Plot points
    for j in range(len(x)):  # Add labels
        ax.text(x[j], y[j], z[j], f"{atoms[j]}{j + 1}", color="green", fontsize=12)
    ax.set_title(f"Cluster {index+1}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Get maximum range of the coordinates to have equal scales
    max_range = np.array([max(x) - min(x), max(y) - min(y), max(z) - min(z)]).max() / 2.0

    # Get the mean of each coordinate
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    mean_z = np.mean(z)

    # Set the limits of the plot to have equal scales
    ax.auto_scale_xyz(
        [mean_x - max_range, mean_x + max_range],
        [mean_y - max_range, mean_y + max_range],
        [mean_z - max_range, mean_z + max_range],
    )


def plot_2d_molecules(molecules, plot_type):
    n = get_plot_dimensions(len(molecules))
    fig, axs = plt.subplots(
        n, n, figsize=(5 * n, 5 * n), subplot_kw={"projection": "3d" if plot_type == "3d" else None}
    )

    for i, ax in enumerate(axs.flat):
        if i < len(molecules):
            molecule = molecules[i]
            if plot_type == "2d":
                plot_2d_molecule(ax, molecule, i)
            else:
                plot_3d_molecule(ax, molecule, i)
        else:
            ax.axis("off")  # Hide unused subplots

    plt.tight_layout()
    plt.savefig("output.png")  # Save the figure to a file
    plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--plot", default="3d")
    return parser.parse_args()


def main():
    args = parse_arguments()
    molecules = parse_gaussian_file(args.filename)
    plot_2d_molecules(molecules, args.plot)


if __name__ == "__main__":
    main()
