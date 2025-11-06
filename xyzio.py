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


