from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

metal_atoms_set = {'zn'}

with open('RASPA_Output/IRMOF-1.xyz') as file:
    num_atoms = int(file.readline())
    MOF_name = file.readline()
    print(num_atoms)
    print(MOF_name)
        
    atom = []
    atom_ids = []
    points = []
    
    atom_id = 1

    for line in file:
        atom_name, x, y, z = line.split()
        atom_name = atom_name.lower()
        atom.append((atom_name, atom_id))

        # Extract metal atoms to visualise on a 3D scatter plot.
        if atom_name in metal_atoms_set:
            x = float(x)
            y = float(y)
            z = float(z)
            atom_ids.append(atom_id)
            point = (x, y, z)
            points.append(point)
        
        atom_id += 1

x_locs = [p[0] for p in points]
y_locs = [p[1] for p in points]
z_locs = [p[2] for p in points]

points = np.array(points)
centroid = points.mean(axis=0)


dist_array = [distance.euclidean(centroid, point) for point in points]
print(min(dist_array), np.argmin(dist_array))
print(atom_ids[197])
print(atom[2579])
