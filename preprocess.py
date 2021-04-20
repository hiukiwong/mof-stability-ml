import os
import glob
import shutil
import subprocess
import sys
import time
import numpy as np
from pathlib import Path

def write_raspa_input_file(simulation_type, number_of_cycles, print_every, framework, framework_name, unit_cells):
    molecule_name_list = []
    simulation_file_name = "simulation.input"
    f = open(simulation_file_name, "w+")
    f.write("SimulationType     %s\n" % simulation_type)
    f.write("NumberofCycles     %d\n" % number_of_cycles)
    f.write("PrintEvery     %d\n\n" % print_every)
    f.write("Framework      %s\n" % framework)
    f.write("FrameworkName      %s\n" % framework_name)
    f.write("UnitCells      %g %g %g\n" % (unit_cells[0], unit_cells[1], unit_cells[2]))
    f.close()
    return simulation_file_name
    # return (molecule_name_list, unit_cells)

def raspa_create_cif(mof_name):
    shutil.rmtree("VTK")
    shutil.rmtree("Restart")
    shutil.rmtree("Output")
    raspa_output_folder_path = "RASPA_Output/"
    if not os.path.exists(raspa_output_folder_path):
        os.makedirs(raspa_output_folder_path)

    cif_filename = "Framework_0_initial_2_2_2_P1.cif"
    cif_src_path = os.path.join("Movies/System_0/", cif_filename)

    cif_dest_path = os.path.join(raspa_output_folder_path, f"{mof_name}.cif")
    xyz_dest_path = os.path.join(raspa_output_folder_path, f"{mof_name}.xyz")

    for filename in os.listdir("Movies/System_0"):
        if filename.endswith("Framework_0_initial_2_2_2_P1.cif"):
            shutil.copy(cif_src_path, cif_dest_path)

    shutil.rmtree("Movies")
    return cif_dest_path, xyz_dest_path


mof_name = "UIO-66"
sim_input_file_path = write_raspa_input_file(
    simulation_type="MonteCarlo",
    number_of_cycles=1,
    print_every=1,
    framework=0,
    framework_name=mof_name,
    unit_cells=[2, 2, 2]
)
path_to_raspa = "/home/hiuki/RASPA/src/simulate"
subprocess.run([path_to_raspa, sim_input_file_path])
cif_dest_path, xyz_dest_path = raspa_create_cif(mof_name)
subprocess.run(["obabel",  "-icif", cif_dest_path, "-oxyz", "-O", xyz_dest_path])
