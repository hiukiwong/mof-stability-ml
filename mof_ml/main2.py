import os
import time
import subprocess

from project_paths import input_files_directory
from project_paths import output_files_directory
from project_paths import sambvca21_full_path
from py2sambvca_v2 import Py2sambvca

from utils import plot
from utils import str_handling



from utils.preprocess import write_raspa_input_file
from utils.preprocess import raspa_create_cif

from utils.pickIDs2 import cif_to_df
from utils.pickIDs2 import determine_centroid
from utils.pickIDs2 import pick_centre_id
from utils.pickIDs2 import pick_z_ids
from utils.pickIDs2 import pick_xz_ids
from utils.pickIDs2 import xyz_to_df
from utils.pickIDs2 import get_atom_del_list



##One problem currently observed is if the file name is too long, the .dats cannot be properly named and come out as .d or .da instead and the plots are unable to be generated

_DEBUG = True


def main() -> None:  # pylint: disable=too-many-locals, too-many-statements

    print("==================RUNNING RASPA==================")

    mof_name = "HKUST-1"

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

    print("==================RUNNING SAMBVCA==================")

    # Check if SambVca calculator is installed at the right place.
    try:
        assert sambvca21_full_path.is_file()
        print("Found SambVca21.x calculator")
    except AttributeError:
        print("path supplied to SambVca calculator is not of valid type 'Path'.")
    except AssertionError:
        print("SambVca calculator file not present.")
    

    xyz_dest_path = "/home/hiuki/mof-stability-ml/RASPA_Output/HKUST-1.xyz"
    cif_dest_path = "/home/hiuki/mof-stability-ml/RASPA_Output/HKUST-1.cif"



    all_atoms_df = cif_to_df(cif_dest_path)
    closest_metal_atoms_df, all_metal_atoms_df = determine_centroid(all_atoms_df)


    central_id, centre_atom = pick_centre_id(closest_metal_atoms_df)
    z_ax_ids, z_axis_atoms = pick_z_ids (central_id, centre_atom, all_atoms_df)
    xz_plane_ids = pick_xz_ids(central_id, centre_atom, all_atoms_df)

    all_atoms_cartesian_df = xyz_to_df(xyz_dest_path)
    atoms_to_del_ids = get_atom_del_list(central_id, centre_atom, all_atoms_cartesian_df)
 

    # Start the timer for this calculation.
    start_time = time.time()

    center_atom = central_id
    z_ax_atoms = [z_ax_ids[0]]
    xz_plane_atoms = [xz_plane_ids[0]]
   
    print(center_atom, z_ax_atoms, xz_plane_atoms)

    center_atom_str = "c" + str_handling.atoms_to_string(center_atom)
    z_ax_atoms_str = "z" + str_handling.atoms_to_string(z_ax_atoms)
    xz_plane_atoms_str = "xz" + str_handling.atoms_to_string(xz_plane_atoms)
    orientation_tag = "_".join([center_atom_str, z_ax_atoms_str, xz_plane_atoms_str])


    mof_out_dir = os.path.join(output_files_directory, mof_name)
    orientation_dir = os.path.join(mof_out_dir, orientation_tag)

    # Create the output directories for this MOF if it doesn't already exist
    if not os.path.exists(mof_out_dir):
        os.makedirs(mof_out_dir)

    if not os.path.exists(orientation_dir):
        os.makedirs(orientation_dir)

    full_tag = "_".join([mof_name, orientation_tag])

    inp_file_name = full_tag + ".inp"
    inp_filepath = os.path.join(orientation_dir, inp_file_name)

    out_file_name = full_tag + ".out"
    out_filepath = os.path.join(orientation_dir, out_file_name)

    print(f"xyz_fullpath: {xyz_dest_path}")
    print(f"mof_name: {mof_name}")
    print(f"orientation tag: {orientation_tag}")
    print(f"orientation_dir: {orientation_dir}")
    print(f"inp_filepath: {inp_filepath}")
    print(f"out_filepath: {out_filepath}")

    P2S = Py2sambvca(
        xyz_filepath=xyz_dest_path,
        sphere_center_atom_ids=central_id,
        z_ax_atom_ids=z_ax_atoms,
        xz_plane_atoms_ids=xz_plane_atoms,
        path_to_sambvcax=str(sambvca21_full_path),
        atoms_to_delete_ids=atoms_to_del_ids
    )

    # inp_filepath = "sample.inp"
    P2S.write_input(inp_filepath)
    P2S.calc(inp_filepath)
    results_dict = P2S.extract_calc_results(out_filepath)

    buried_volume_percent = results_dict["Buried Volume %"]
    print(f"%Buried volume = {buried_volume_percent}%")

    buried_volume_num = results_dict["Buried Volume"]
    print(f"Buried volume = {buried_volume_num}Angs^3")

    quad_num = results_dict["Quadrant Data"]
    print(f"Quadrant Data = {quad_num}%")

    octant_num = results_dict["Octant Data"]
    print(f"Octant Data = {octant_num}%")

    # Generate and Save filled contour plot.
    top_dat_filename = full_tag + "-TopSurface.dat"
    plot.save_steric_map(orientation_dir, top_dat_filename)
    plot.save_cloud_3d(orientation_dir, top_dat_filename)

    bot_dat_filename = full_tag + "-BotSurface.dat"
    plot.save_steric_map(orientation_dir, bot_dat_filename)
    plot.save_cloud_3d(orientation_dir, bot_dat_filename)

    # End the timer for this calculation.
    end_time = time.time()

    print(f"{mof_name} completed! Time taken: {end_time-start_time}s")

    print(orientation_dir)

    # if _DEBUG:
    #     break


if __name__ == "__main__":
    main()
