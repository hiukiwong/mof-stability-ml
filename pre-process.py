import os, glob, shutil, subprocess, sys, time
import numpy as np

# def read_cif_file(file, flag):
#     #specify full relative path, flag = true
#         # blank list to store the cif data
#     cif_data = []
#         # blank list to store the entire cif file
#     cif_file = []
#         # the flag variable has been introduced as a marker to activate when the cif data is to be read and switched off
#         # when it doesn't have to be read.
#     flag1 = 1
#     flag2 = 1
#     flag3 = 1
#     if flag == False:
#         keywords = "_atom_site_fract_z"
#     if flag == True:
#         keywords = "_atom_site_fract_z"
#     exit_keyword = "#END"
#     exit_keyword_2 = "loop_"
#         # get the current working directory
#     cwd = os.getcwd()
#     if flag == False:
#         path = "%s/%s" %(cwd, file)
#     if flag == True:
#         path = "%s" % file
#         # in this case the file is opened using this syntax as the syntax used to open a file in the output_parser
#         # function was not working for this case
#     f = open(path, "r")
#     for x in f:
#         if (exit_keyword in x) or (exit_keyword_2 in x):
#             flag1 = 1
#         if flag1 == 2:
#             x = x.strip()
#             x = x.split()
#                 # the if statements below along with the for loops are used to remove the brackets (and the data contained within these brackets)
#             for i in range(0, len(x)):
#                 x[i] = remove_brackets_from_line(x[i])
#             cif_data.append(x)
#                 # Creating a copy of list y, so I can append "\n" to the cif data to make it easier to print
#             y = x.copy()
#             y.append("\n")
#             cif_file.append(y)
#         if flag1 == 1:
#             cif_file.append(x)
#         if keywords in x:
#             flag1 = 2
#     return (cif_data, cif_file)
# def remove_brackets_from_line(line):
#     flag3 = 1
#     for i in range(0, len(line)):
#         if line[i] == ')':
#             flag2 = 1
#             stop = i
#             flag3 = 2
#         if line[i] == '(':
#             flag2 = 2
#             start = i
#     if flag3 == 2:
#         line = line[0: start:] + line[stop + 1::]
#     return (line)
# #[x,y] = read_cif_file(tag, True)

# [x,y] = read_cif_file('/home/hiuki/Downloads/IRMOF-1.cif', True)


# def calc_number_of_unit_cells(unit_cell_dimensions):
#     #remember to check the cutoff everytime you run the program
#     cutoff = 12.9
#     length_a = unit_cell_dimensions[0]
#     length_b = unit_cell_dimensions[1]
#     length_c = unit_cell_dimensions[2]
#     alpha = unit_cell_dimensions[3]
#     beta = unit_cell_dimensions[4]
#     gamma = unit_cell_dimensions[5]
#     # Convert cif information to unit_cell vectors
#     ax = length_a
#     ay = 0.0
#     az = 0.0
#     bx = length_b * np.cos(gamma * np.pi / 180.0)
#     by = length_b * np.sin(gamma * np.pi / 180.0)
#     bz = 0.0
#     cx = length_c * np.cos(beta * np.pi / 180.0)
#     cy = (length_c * length_b * np.cos(alpha * np.pi / 180.0) - bx * cx) / by
#     cz = (length_c ** 2 - cx ** 2 - cy ** 2) ** 0.5
#     unit_cell = np.asarray([[ax, ay, az], [bx, by, bz], [cx, cy, cz]])
#     # Unit cell vectors
#     A = unit_cell[0]
#     B = unit_cell[1]
#     C = unit_cell[2]
#     # minimum distances between unit cell faces
#     Wa = np.divide(np.linalg.norm(np.dot(np.cross(B, C), A)), np.linalg.norm(np.cross(B, C)))
#     Wb = np.divide(np.linalg.norm(np.dot(np.cross(C, A), B)), np.linalg.norm(np.cross(C, A)))
#     Wc = np.divide(np.linalg.norm(np.dot(np.cross(A, B), C)), np.linalg.norm(np.cross(A, B)))
#     uc_x = int(np.ceil(cutoff / (0.5 * Wa)))
#     uc_y = int(np.ceil(cutoff / (0.5 * Wb)))
#     uc_z = int(np.ceil(cutoff / (0.5 * Wc)))
#     number_of_unit_cells = [uc_x, uc_y, uc_z]
#     return (number_of_unit_cells)



# def extract_unit_cell_dimensions(cif_file):
#     # List of all unit cell dimensions in the following order: length_a, length_b, length_c, alpha, gamma, beta
#     unit_cell_dimensions = []
#     for line in cif_file:
#         flag3 = 1
#         if "_cell_length_a" in line:
#             line= line.split()[1]  # unit cell vector
#             line = remove_brackets_from_line(line)
#             unit_cell_dimensions.append(float(line))  # string to float
#         if "_cell_length_b" in line:
#             line = line.split()[1]
#             line = remove_brackets_from_line(line)
#             unit_cell_dimensions.append(float(line))
#         if "_cell_length_c" in line:
#             line = line.split()[1]
#             line = remove_brackets_from_line(line)
#             unit_cell_dimensions.append(float(line))
#         if "_cell_angle_alpha" in line:
#             line = line.split()[1]
#             line = remove_brackets_from_line(line)
#             unit_cell_dimensions.append(float(line))
#         if "_cell_angle_beta" in line:
#             line = line.split()[1]
#             line = remove_brackets_from_line(line)
#             unit_cell_dimensions.append(float(line))
#         if "_cell_angle_gamma" in line:
#             line = line.split()[1]
#             line = remove_brackets_from_line(line)
#             unit_cell_dimensions.append(float(line))
#     return(unit_cell_dimensions)


# unit_cell_dimensions = extract_unit_cell_dimensions(y) 
# calc_number_of_unit_cells(unit_cell_dimensions)

def write_raspa_input_file(simulation_type, number_of_cycles, print_every, framework, framework_name, unit_cells):
    molecule_name_list = []
    f = open("simulation.input", "w+")
    f.write("SimulationType     %s\n" % simulation_type)
    f.write("NumberofCycles     %d\n" % number_of_cycles)
    f.write("PrintEvery     %d\n\n" % print_every)
    f.write("Framework      %s\n" % framework)
    f.write("FrameworkName      %s\n" % framework_name)
    f.write("UnitCells      %g %g %g\n" % (unit_cells[0], unit_cells[1], unit_cells[2]))
    # return (molecule_name_list, unit_cells)


write_raspa_input_file("MonteCarlo", 1, 1, 0, "IRMOF-1", [2, 2, 2])

subprocess.run(["/home/hiuki/RASPA/src/simulate", "simulation.input"])
shutil.rmtree("VTK")
shutil.rmtree("Restart")
shutil.rmtree("Output")
cif_path = "Movies/System_0/Framework_0_initial_2_2_2_P1.cif"
while not os.path.exists(cif_path):
    time.sleep(20)

if os.path.isfile(cif_path):
    for Cleanup in glob.glob("/home/hiuki/mof-stability-ml/Movies/System_0/*.*"):
        if not Cleanup.endswith("Framework_0_initial_2_2_2_P1.cif"):
            os.remove(Cleanup)