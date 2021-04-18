import os
import time

from config.path_handler import input_files_directory
from config.path_handler import output_files_directory
from config.path_handler import sambvca21_full_path
from py2_2.py2_2 import Py2sambvca
from utils import plot
from utils import str_handling
# from pickIDs import pick_center_id
# from pickIDs import pick_z_ids


_DEBUG = True


def main() -> None:  # pylint: disable=too-many-locals, too-many-statements

    # Check if SambVca calculator is installed at the right place.
    try:
        assert sambvca21_full_path.is_file()
        print("Found SambVca21.x calculator")
    except AttributeError:
        print("path supplied to SambVca calculator is not of valid type 'Path'.")
    except AssertionError:
        print("SambVca calculator file not present.")

    # pre-process.py here? Do we still need the for loop below if we
    # only have 1 .xyz file at a time? Do we want to delete the .cif?
    # Or should we just check that the file name ends with .xyz? endswith()
    # Which ordering is better for scaling up.

    for xyz_filename in os.listdir(input_files_directory):

        # Start the timer for this calculation.
        start_time = time.time()

        # TODO: Logic to parse the xyz files and pick centres go here
        center_atom = [130]
        z_ax_atoms = [123]
        xz_plane_atoms = [57]
        # xyz_fullpath = os.path.join(input_files_directory, xyz_filename)
        # [center_atom, z_ax_atoms, xz_plane_atoms] = pickIDs.pick_id(xyz_fullpath)

        center_atom_str = "c" + str_handling.atoms_to_string(center_atom)
        z_ax_atoms_str = "z" + str_handling.atoms_to_string(z_ax_atoms)
        xz_plane_atoms_str = "xz" + str_handling.atoms_to_string(xz_plane_atoms)
        orientation_tag = "_".join([center_atom_str, z_ax_atoms_str, xz_plane_atoms_str])

        # Testing, only doing the first one: 09010N2.xyz
        xyz_fullpath = os.path.join(input_files_directory, xyz_filename)
        mof_name = xyz_filename[:-4]
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

        print(f"xyz_fullpath: {xyz_fullpath}")
        print(f"mof_name: {mof_name}")
        print(f"orientation tag: {orientation_tag}")
        print(f"orientation_dir: {orientation_dir}")
        print(f"inp_filepath: {inp_filepath}")
        print(f"out_filepath: {out_filepath}")

        P2S = Py2sambvca(
            xyz_filepath=xyz_fullpath,
            sphere_center_atom_ids=center_atom,
            z_ax_atom_ids=z_ax_atoms,
            xz_plane_atoms_ids=xz_plane_atoms,
            path_to_sambvcax=str(sambvca21_full_path),
        )

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

        if _DEBUG:
            break


if __name__ == "__main__":
    main()
