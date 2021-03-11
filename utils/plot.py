import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
from utils.read import read_cloud
from utils.read import read_contour


def filled_contour(
    x_coords: np.array, y_coords: np.array, z_coords: np.array, xmin: float, xmax: float, title: str
) -> figure:
    """This function generates a figure object of filled contour steric map with the
    given x, y, z data, and its title.

    Args:
        x_coords (np.array): Array of floats of x coordinates
        y_coords (np.array): Array of floats of y coordinates
        z_coords (np.array): Array of floats of z coordinates
        xmin (float): Minimum value of x
        xmax (float): Maximum value of x
        title (str): Title of the output figure printed at the top of the chart

    Returns:
        Figure: matplotlib figure object of the steric map
    """

    plt.close("all")
    levels = np.arange(xmin, xmax + 0.001, 0.25)
    fig, axe = plt.subplots()
    cset1 = axe.contourf(
        x_coords, y_coords, z_coords, levels, cmap=plt.cm.get_cmap("jet", len(levels) - 1)
    )
    cset2 = axe.contour(x_coords, y_coords, z_coords, cset1.levels, colors="k")
    for contour_line in cset2.collections:
        contour_line.set_linestyle("solid")
    fig.colorbar(cset1)
    axe.set_title(title, fontsize=16)
    return fig


def cloud_3d(x_coords: np.array, y_coords: np.array, z_coords: np.array, title: str) -> figure:
    """[summary]

    Args:
        x_coords (np.array): [description]
        y_coords (np.array): [description]
        z_coords (np.array): [description]
        title (str): [description]

    Returns:
        Figure: [description]
    """
    plt.close("all")
    fig = plt.figure()
    axe = fig.add_subplot(111, projection="3d")
    data_points = axe.scatter(
        x_coords, y_coords, z_coords, c=z_coords, s=1, cmap=plt.cm.get_cmap("jet")
    )
    plt.colorbar(data_points)
    axe.set_xlim3d(-3, 3)
    axe.set_ylim3d(-3, 3)
    axe.set_zlim3d(-3, 3)
    axe.set_title(title, fontsize=16)
    return fig


def save_plot(figure: figure, dat_file_path: str, additional_name: str = "") -> None:
    """[summary]

    Args:
        figure (Figure): [description]
        dat_file_path (str): [description]
        additional_name (str, optional): [description]. Defaults to "".
    """
    jpg_save_path = dat_file_path[:-4] + additional_name + ".jpg"
    figure.savefig(jpg_save_path)
    print(f"Info: image saved in {jpg_save_path}")


def save_steric_map(orientation_dir: str, dat_filename: str) -> None:
    """[summary]

    Args:
        orientation_dir (str): [description]
        dat_filename (str): [description]
    """
    # Generate and Save filled contour plot.
    dat_filepath = os.path.join(orientation_dir, dat_filename)
    x_loc, y_loc, z_loc, xmin, xmax = read_contour(dat_filepath)
    filled_contour_figure = filled_contour(x_loc, y_loc, z_loc, xmin, xmax, dat_filename)
    save_plot(filled_contour_figure, dat_filepath)


def save_cloud_3d(orientation_dir: str, dat_filename: str) -> None:
    """[summary]

    Args:
        orientation_dir (str): [description]
        dat_filename (str): [description]
    """
    # Generate and Save filled 3D Cloud plot.
    dat_filepath = os.path.join(orientation_dir, dat_filename)
    x_coords, y_coords, z_coords = read_cloud(dat_filepath)
    cloud_3d_figure = cloud_3d(x_coords, y_coords, z_coords, dat_filename)
    save_plot(cloud_3d_figure, dat_filepath, additional_name="-3d")
