import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
from ref_data.metal_set import metal_symbols

## This version works with main.py and picks atoms based off the xyz. It doesn't work with triclinic unit cells
def xyz_to_df(xyz_dest_path: str) -> pd.DataFrame:
    all_atoms_df = pd.read_table(xyz_dest_path, skiprows=2, delim_whitespace=True, names=['atom', 'x', 'y', 'z'])
    num_atoms = len(all_atoms_df)
    all_atoms_df.index = pd.RangeIndex(start=1, stop=num_atoms+1, step=1)
    all_atoms_df['xyz'] = tuple(all_atoms_df[['x', 'y', 'z']].values)
    return all_atoms_df


def determine_centroid(all_atoms_df: pd.DataFrame) -> pd.DataFrame:
    centroid = (all_atoms_df['x'].mean(), all_atoms_df['y'].mean(), all_atoms_df['z'].mean())
    all_atoms_df['distance'] = all_atoms_df['xyz'].apply(lambda row: distance.euclidean(centroid, row))
    all_metal_atoms_df = all_atoms_df.loc[all_atoms_df['atom'].isin(metal_symbols)]
    distance_column = all_metal_atoms_df['distance']
    closest_metal_atoms_df = all_metal_atoms_df[distance_column == distance_column.min()]
    return closest_metal_atoms_df, all_metal_atoms_df


def pick_centre_id(closest_metal_atoms_df) -> list:
    centre_atom = closest_metal_atoms_df.iloc[0]
    central_id = [closest_metal_atoms_df.index[0]]
    print(centre_atom)
    return central_id, centre_atom


def pick_z_ids(central_id, centre_atom, all_atoms_df):
    x_wanted = centre_atom.x
    y_wanted = centre_atom.y
    z_wanted = centre_atom.z

    z_axis_atoms = all_atoms_df[(all_atoms_df['x'] == x_wanted) & (all_atoms_df['y'] == y_wanted) & (all_atoms_df['z'] < z_wanted)]
    print(z_axis_atoms)
    z_ax_ids = list(z_axis_atoms.index)

    return z_ax_ids, z_axis_atoms


def pick_xz_ids(central_id, centre_atom, all_atoms_df):
    x_wanted = centre_atom.x
    y_wanted = centre_atom.y
    z_wanted = centre_atom.z
    xz_plane_atoms = all_atoms_df[(all_atoms_df['x'] != x_wanted) & (all_atoms_df['y'] != y_wanted) & (all_atoms_df['z'] == z_wanted)]
    print(xz_plane_atoms)
    xz_plane_ids = list(xz_plane_atoms.index)
    return xz_plane_ids
