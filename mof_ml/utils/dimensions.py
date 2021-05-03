import os, re, math
import numpy as np

cif_dest_path="/home/hiuki/mof-stability-ml/RASPA_Output/IRMOF-1.cif"

def read_dimensions(cif_dest_path):
    with open(cif_dest_path, "r") as file:
        lines = file.readlines()
        cell_a = re.compile(r".*_cell_length_a[ ]{1,}(\d*\d*\.\d*\d*\d*)")
        cell_b = re.compile(r".*_cell_length_b[ ]{1,}(\d*\d*\.\d*\d*\d*)")
        cell_c = re.compile(r".*_cell_length_c[ ]{1,}(\d*\d*\.\d*\d*\d*)")
        cell_alpha = re.compile(r".*_cell_angle_alpha[ ]{1,}(\d*\d*)")
        cell_beta = re.compile(r".*_cell_angle_beta[ ]{1,}(\d*\d*)")
        cell_gamma = re.compile(r".*_cell_angle_gamma[ ]{1,}(\d*\d*)")
        for line_num, line in enumerate(lines):
            cell_a_match = cell_a.search(line)
            cell_b_match = cell_b.search(line)
            cell_c_match = cell_c.search(line)
            cell_alpha_match = cell_alpha.search(line)
            cell_beta_match = cell_beta.search(line)
            cell_gamma_match = cell_gamma.search(line)

            if cell_a_match:
                a_dim = float(cell_a_match[1])
            elif cell_b_match:
                b_dim = float(cell_b_match[1])
            elif cell_c_match:
                c_dim = float(cell_c_match[1])
            elif cell_alpha_match:
                alpha_dval = float(cell_alpha_match[1])
            elif cell_beta_match:
                beta_dval = float(cell_beta_match[1])
            elif cell_gamma_match:
                gamma_dval = float(cell_gamma_match[1])

    alpha_val = math.radians(alpha_dval)
    beta_val = math.radians(beta_dval)
    gamma_val = math.radians(gamma_dval)
    return a_dim, b_dim, c_dim, alpha_val, beta_val, gamma_val

def get_transformation_matrix(all_atoms_df, a_dim, b_dim, c_dim, alpha_val, beta_val, gamma_val):
    cosa = np.cos(alpha_val)
    sina = np.sin(alpha_val)
    cosb = np.cos(beta_val)
    sinb = np.sin(beta_val)
    cosg = np.cos(gamma_val)
    sing = np.sin(gamma_val)
    volume = 1.0 - cosa**2.0 - cosb**2.0 - cosg**2.0 + 2.0 * cosa * cosb * cosg
    volume = np.sqrt(volume)
    r = np.zeros((3, 3))
    r[0, 0] = 1.0 / a
    r[0, 1] = -cosg / (a_dim * sing)
    r[0, 2] = (cosa * cosg - cosb) / (a_dim * volume * sing)
    r[1, 1] = 1.0 / (b_dim * sing)
    r[1, 2] = (cosb * cosg - cosa) / (b_dim * volume * sing)
    r[2, 2] = sing / (c_dim * volume)
    return r


a_dim, b_dim, c_dim, alpha_val, beta_val, gamma_val=read_dimensions(cif_dest_path)
r = get_transformation_matrix(a_dim, b_dim, c_dim, alpha_val, beta_val, gamma_val)
print(r)

# r = math.sqrt(a_dim**2+b_dim**2+c_dim**2+2*a_dim*b_dim*(math.cos(gamma_val))+2*a_dim*c_dim*(math.cos(beta_val))+2*b_dim*c_dim*(math.cos(alpha_val)))
