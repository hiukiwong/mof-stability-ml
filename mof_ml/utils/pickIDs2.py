import pandas as pd
import math
# import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from ref_data.metal_set import metal_symbols


cif_dest_path='/home/hiuki/mof-stability-ml/RASPA_Output/IRMOF-1.cif'
def cif_to_df(cif_dest_path: str) -> pd.DataFrame:
    all_atoms_df = pd.read_table(cif_dest_path, skiprows=36, delim_whitespace=True, names=['atom label', 'atom symbol', 'a', 'b', 'c', 'charge'])
    num_atoms = len(all_atoms_df)
    all_atoms_df.index = pd.RangeIndex(start=1, stop=num_atoms+1, step=1)
    all_atoms_df['abc'] = tuple(all_atoms_df[['a', 'b', 'c']].values)
    del all_atoms_df['charge']
    del all_atoms_df["atom label"]
    return all_atoms_df



def determine_centroid(all_atoms_df: pd.DataFrame) -> pd.DataFrame:
    centroid = (all_atoms_df['a'].mean(), all_atoms_df['b'].mean(), all_atoms_df['c'].mean())
    all_atoms_df['distance'] = all_atoms_df['abc'].apply(lambda row: distance.euclidean(centroid, row))
    all_metal_atoms_df = all_atoms_df.loc[all_atoms_df['atom symbol'].isin(metal_symbols)]
    distance_column = all_metal_atoms_df['distance']
    closest_metal_atoms_df = all_metal_atoms_df[distance_column == distance_column.min()]
    return closest_metal_atoms_df, all_atoms_df


def pick_centre_id(closest_metal_atoms_df) -> list:
    centre_atom = closest_metal_atoms_df.iloc[0]
    central_id = [closest_metal_atoms_df.index[0]]
    print(centre_atom)
    return central_id, centre_atom



def pick_z_ids(central_id, centre_atom, all_atoms_df):
    a_wanted = centre_atom.a
    b_wanted = centre_atom.b
    c_wanted = centre_atom.c

    z_axis_atoms = all_atoms_df[(all_atoms_df['a'] == a_wanted) & (all_atoms_df['b'] == b_wanted) & (all_atoms_df['c'] < c_wanted)]
    print(z_axis_atoms)
    z_ax_ids = list(z_axis_atoms.index)

    return z_ax_ids, z_axis_atoms


def pick_xz_ids(central_id, centre_atom, all_atoms_df):
    a_wanted = centre_atom.a
    b_wanted = centre_atom.b
    c_wanted = centre_atom.c
    xz_plane_atoms = all_atoms_df[(all_atoms_df['a'] != a_wanted) & (all_atoms_df['b'] != b_wanted) & (all_atoms_df['c'] == c_wanted)]
    print(xz_plane_atoms)
    xz_plane_ids = list(xz_plane_atoms.index)
    return xz_plane_ids

def xyz_to_df(xyz_dest_path: str) -> pd.DataFrame:
    all_atoms_cartesian_df = pd.read_table(xyz_dest_path, skiprows=2, delim_whitespace=True, names=['atom', 'x', 'y', 'z'])
    num_atoms = len(all_atoms_cartesian_df)
    all_atoms_cartesian_df.index = pd.RangeIndex(start=1, stop=num_atoms+1, step=1)
    all_atoms_cartesian_df['xyz'] = tuple(all_atoms_cartesian_df[['x', 'y', 'z']].values)
    return all_atoms_cartesian_df

def get_atom_del_list (central_id, centre_atom, all_atoms_cartesian_df) -> list:
    centre_atom = all_atoms_cartesian_df.loc[central_id]
    x_centre = centre_atom.x
    y_centre = centre_atom.y
    z_centre = centre_atom.z
    centre = (x_centre, y_centre, z_centre)
    all_atoms_cartesian_df["distance"] = all_atoms_cartesian_df['xyz'].apply(lambda row: distance.euclidean(centre, row))
    atoms_to_del = all_atoms_cartesian_df[all_atoms_cartesian_df['distance'] > 12]
    atoms_to_del_ids = list(atoms_to_del.index)
    return atoms_to_del_ids

# xyz_dest_path = "/home/hiuki/mof-stability-ml/RASPA_Output/Cd3BTB2.xyz"
# cif_dest_path = "/home/hiuki/mof-stability-ml/RASPA_Output/Cd3BTB2.cif"

# all_atoms_df = cif_to_df(cif_dest_path)
# closest_metal_atoms_df, all_metal_atoms_df = determine_centroid(all_atoms_df)


# central_id, centre_atom = pick_centre_id(closest_metal_atoms_df)
# z_ax_ids, z_axis_atoms = pick_z_ids(central_id, centre_atom, all_atoms_df)
# xz_plane_ids = pick_xz_ids(central_id, centre_atom, all_atoms_df)
# all_atoms_cartesian_df = xyz_to_df(xyz_dest_path)
# atoms_to_del_ids = get_atom_del_list(central_id, centre_atom, all_atoms_cartesian_df)
# print(atoms_to_del_ids)