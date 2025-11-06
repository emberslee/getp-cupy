import numpy as np

def write_xyz(filename, coords):
    with open(filename, "w") as f:
        for coord in coords:
            f.write(
                "H {:.3f} {:.3f} {:.3f}\n".format(
                    coord[0],
                    coord[1],
                    coord[2],
                )
            )


def write_pdb(filename, coords, bfactor=None):
    with open(filename, "w") as f:
        for i, coord in enumerate(coords):
            f.write(
                "ATOM  {:>5d}  CA  ALA A{:>4d}    {:8.3f}{:8.3f}{:8.3f}  1.00100.00\n".format(
                    i + 1,
                    i + 1,
                    coord[0],
                    coord[1],
                    coord[2],
                )
            )
            f.write("TER\n")
