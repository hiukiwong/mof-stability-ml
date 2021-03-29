import os, re, math
import numpy as np

with open('RASPA Output/IRMOF-1.cif', "r") as file:
    lines = file.readlines()
    cell_a = re.compile(r".*_cell_length_a    (\d*\d*\.\d*\d*\d*)")
    cell_b = re.compile(r".*_cell_length_b    (\d*\d*\.\d*\d*\d*)")
    cell_c = re.compile(r".*_cell_length_c    (\d*\d*\.\d*\d*\d*)")
    cell_alpha = re.compile(r".*_cell_angle_alpha (\d*\d*)")
    cell_beta = re.compile(r".*_cell_angle_beta  (\d*\d*)")
    cell_gamma = re.compile(r".*_cell_angle_gamma (\d*\d*)")
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

r = math.sqrt(a_dim**2+b_dim**2+c_dim**2+2*a_dim*b_dim*(math.cos(gamma_val))+2*a_dim*c_dim*(math.cos(beta_val))+2*b_dim*c_dim*(math.cos(alpha_val)))
