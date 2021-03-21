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
cif_path = "Movies/System_0/Framework_0_initial_2_2_2_P1.cif"
while not os.path.exists(cif_path):
    time.sleep(20)

if os.path.isfile(cif_path):
    for Cleanup in glob.glob("/home/hiuki/mof-stability-ml/Movies/System_0/*.*"):
        if not Cleanup.endswith("Framework_0_initial_2_2_2_P1.cif"):
            os.remove(Cleanup)


p = Path('Movies/System_0/Framework_0_initial_2_2_2_P1.cif').absolute()
parent_dir = p.parents[1]
p.rename(parent_dir/p.name)
os.rename('Movies', 'RASPA Output')
shutil.rmtree('RASPA Output/System_0')
os.rename('RASPA Output/Framework_0_initial_2_2_2_P1.cif', 'RASPA Output/IRMOF-1.cif')