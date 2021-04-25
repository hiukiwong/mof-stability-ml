import os
from typing import List
from typing import Tuple

import numpy as np


# pylint: disable=too-many-locals
def read_contour(dat_filename: str) -> Tuple[np.array, np.array, np.array, float, float]:

    if not os.path.exists(dat_filename):
        raise FileNotFoundError(
            """The given file path does not exist.
            Check that the appropriate .dat file is given as an argument"""
        )

    dat_file = open(dat_filename)
    lines = dat_file.readlines()
    dat_file.close()
    val = 0

    # Create 3D space and fill it with zeros
    # Find min and max x,y values, plus spacing
    zdata = []
    xmin = +999.0
    xmax = -999.0
    ymin = +999.0
    ymax = -999.0
    for line in lines:
        fields = line.split()
        if len(fields) == 3:
            zdata.append(float(fields[2]))
            val += 1
            if float(fields[0]) < xmin:
                xmin = float(fields[0])
            if float(fields[0]) > xmax:
                xmax = float(fields[0])
            if float(fields[1]) < ymin:
                ymin = float(fields[1])
            if float(fields[1]) > ymax:
                ymax = float(fields[1])
    d_val = int(np.sqrt(val))
    x_coords = np.zeros(d_val, float)
    y_coords = np.zeros(d_val, float)
    z_coords = np.zeros((d_val, d_val), float)
    grid_mesh = float((xmax - xmin) / (d_val - 1))

    # Setting grid mesh values here
    for i in range(d_val):
        x_coords[i] = xmin + i * grid_mesh
        y_coords[i] = ymin + i * grid_mesh
    count = 0
    for i in range(0, d_val, 1):
        for j in range(0, d_val, 1):
            z_coords[j, i] = zdata[count]
            count += 1
    return x_coords, y_coords, z_coords, xmin, xmax


def read_cloud(dat_filepath: str) -> Tuple[List[float], List[float], List[float]]:
    x_coords, y_coords, z_coords = [], [], []
    bot_lim = -7
    top_lim = 7
    with open(dat_filepath, "r") as file:
        for line in file:
            coords = list(map(float, line.split()))
            if bot_lim < coords[2] < top_lim:
                x_coords.append(coords[0])
                y_coords.append(coords[1])
                z_coords.append(coords[2])
    return x_coords, y_coords, z_coords
