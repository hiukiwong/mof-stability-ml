import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
from refdata.metal_set import metal_symbols

all_atoms_df = pd.read_table('RASPA_Output/IRMOF-1.xyz', skiprows=2, delim_whitespace=True, names=['atom', 'x', 'y', 'z'])
num_atoms = len(all_atoms_df)
all_atoms_df.index = pd.RangeIndex(start=1, stop=num_atoms+1, step=1)
all_atoms_df['xyz'] = tuple(all_atoms_df[['x', 'y', 'z']].values)

centroid = (all_atoms_df['x'].mean(), all_atoms_df['y'].mean(), all_atoms_df['z'].mean())
all_atoms_df['distance'] = all_atoms_df['xyz'].apply(lambda row: distance.euclidean(centroid, row))

all_metal_atoms_df = all_atoms_df.loc[all_atoms_df['atom'].isin(metal_symbols)]
distance_column = all_metal_atoms_df['distance']
closest_metal_atoms_df = all_metal_atoms_df[distance_column == distance_column.min()]

centre_atom = closest_metal_atoms_df.iloc[0]
central_id = [closest_metal_atoms_df.index[0]]
x_wanted = centre_atom.x
y_wanted = centre_atom.y
z_wanted = centre_atom.z

z_axis_atoms = all_atoms_df[(all_atoms_df['x'] == x_wanted) & (all_atoms_df['y'] == y_wanted) & (all_atoms_df['z'] != z_wanted)]
z_ax_ids = list(z_axis_atoms.index)

xz_plane_atoms = all_atoms_df[(all_atoms_df['x'] != x_wanted) & (all_atoms_df['y'] == y_wanted) & (all_atoms_df['z'] == z_wanted)]
xz_plane_ids = list(xz_plane_atoms.index)

print(f'Centre atom ID: {central_id}')
print(f'Z axis atom IDs: {z_ax_ids}')
print(f'XZ plane atom IDs: {xz_plane_ids}')
