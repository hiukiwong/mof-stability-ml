import os, glob, shutil, subprocess, sys, time
import numpy as np
from pathlib import Path

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
raspa_output_folder_path = "RASPA_Output/"
if not os.path.exists(raspa_output_folder_path):
    os.makedirs(raspa_output_folder_path)

cif_filename = "Framework_0_initial_2_2_2_P1.cif"
cif_src_path = os.path.join("Movies/System_0/", cif_filename)

def name_of_mof(filepath: str) -> str:
    with open(filepath, "r") as f:
        first_line = f.readline()
        mof_name = first_line.split("data_", 1)[1].split("\n", 1)[0]
        f.close()
    return mof_name

mof_name = name_of_mof(cif_src_path)
cif_dest_path = os.path.join(raspa_output_folder_path, f"{mof_name}.cif")
xyz_dest_path = os.path.join(raspa_output_folder_path, f"{mof_name}.xyz")

for filename in os.listdir("Movies/System_0"):
    if filename.endswith("Framework_0_initial_2_2_2_P1.cif"):
        shutil.copy(cif_src_path, cif_dest_path)

shutil.rmtree("Movies")

subprocess.run(["obabel",  "-icif", cif_dest_path, "-oxyz", "-O", xyz_dest_path])