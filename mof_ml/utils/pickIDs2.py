import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
# from ref_data.metal_set import metal_symbols
from metal_set import metal_symbols
from dimensions import get_transformation_matrix
from dimensions import read_dimensions


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
    return closest_metal_atoms_df, all_atoms_df


def pick_centre_id(closest_metal_atoms_df) -> list:
    centre_atom = closest_metal_atoms_df.iloc[0]
    central_id = [closest_metal_atoms_df.index[0]]
    print(centre_atom)
    return central_id, centre_atom

def xyz_to_frac(all_atoms_df, r):
    all_atoms_df["frac"]=np.dot(r,all_atoms_df["xyz"])
    all_atoms_df["a"]=all_atoms_df["frac"][0]
    return all_atoms_df

a_dim, b_dim, c_dim, alpha_val, beta_val, gamma_val=read_dimensions("/home/hiuki/mof-stability-ml/RASPA_Output/IRMOF-1.cif")
r=get_transformation_matrix(a_dim, b_dim, c_dim, alpha_val, beta_val, gamma_val)

xyz_dest_path = "/home/hiuki/mof-stability-ml/RASPA_Output/IRMOF-1.xyz"
all_atoms_df=xyz_to_df(xyz_dest_path)
closest_metal_atoms_df, all_ligand_atoms_df=determine_centroid(all_atoms_df)
central_id, centre_atom = pick_centre_id(closest_metal_atoms_df)
all_atoms_df=xyz_to_frac(all_ligand_atoms_df, r)
all_atoms_df.head()



# def pick_z_ids(central_id, centre_atom, all_atoms_df):
#     x_wanted = centre_atom.x
#     y_wanted = centre_atom.y
#     z_wanted = centre_atom.z

#     z_axis_atoms = all_atoms_df[(all_atoms_df['x'] == x_wanted) & (all_atoms_df['y'] == y_wanted) & (all_atoms_df['z'] < z_wanted)]
#     print(z_axis_atoms)
#     z_ax_ids = list(z_axis_atoms.index)

#     return z_ax_ids, z_axis_atoms


# def pick_xz_ids(central_id, centre_atom, all_atoms_df):
#     # z_ax_id = z_ax_ids[0]
#     # z_ax_atom = z_axis_atoms.iloc[0]
#     x_wanted = centre_atom.x
#     y_wanted = centre_atom.y
#     z_wanted = centre_atom.z
#     xz_plane_atoms = all_atoms_df[(all_atoms_df['x'] != x_wanted) & (all_atoms_df['y'] != y_wanted) & (all_atoms_df['z'] == z_wanted)]
#     print(xz_plane_atoms)
#     xz_plane_ids = list(xz_plane_atoms.index)
#     return xz_plane_ids
