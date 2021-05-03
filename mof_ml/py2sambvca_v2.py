# pylint: disable=too-many-arguments
import glob
import os
import re
import subprocess
from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pandas as pd
from ref_data.radiitable import radii_table


class Py2sambvca:
    """
    Wrapper class for py2sambvca functions.
    Call this class to instantiate a py2sambvca object, which has methods to write input,
    call SambVca, and retreieve output.

    Parameters:
    xyz_filepath (str): Location of .xyz molecular coordinates file for writing input data
    sphere_center_atom_ids (list): ID of atoms defining the sphere center,
                                    mid point if multiple chosen.
    z_ax_atom_ids (list): ID of atoms for positive z-axis, mid point if multiple chosen.
    xz_plane_atoms_ids (list): ID of atoms for xz-plane, mid point if multiple chosen.
    atoms_to_delete_ids (list): ID of atoms to be deleted (default None)
    sphere_radius (float): Sphere radius in Angstrom (default 3.5)
    displacement (float): Displacement of oriented molecule from
                            sphere center in Angstrom (default 0.0)
    mesh_size (float): Mesh size for numerical integration (default 0.10)
    remove_H (int): 0/1 Do not remove/remove H atoms from Vbur calculation (default 1)
    orient_z (int): 0/1 Molecule oriented along negative/positive Z-axis (default 1)
    write_surf_files (int): 0/1 Do not write/write files for top and bottom surfaces (default 1)
    path_to_sambvcax (str): Path to the SambVca executable. Only needed to use py2sambvca.calc()
    (default "/path/to/executable/sambvca.x")
    """

    def __init__(
        self,
        xyz_filepath: str,
        sphere_center_atom_ids: List[int],
        z_ax_atom_ids: List[int],
        xz_plane_atoms_ids: List[int],
        atoms_to_delete_ids: Union[None, List[int]] = None,
        sphere_radius: float = 3.5,
        displacement: float = 0.0,
        mesh_size: float = 0.10,
        remove_H: int = 1,
        orient_z: int = 0,
        write_surf_files: int = 1,
        path_to_sambvcax: str = "/path/to/executable/sambvca.x",
    ) -> None:
        """
        See docstring for py2sambvca
        """
        # if atoms are requested to be deleted, assign them and the number of them
        # otherwise, set to none to avoid bad writes in the future
        self.n_atoms_to_delete: Union[None, int] = None
        self.atoms_to_delete_ids = None

        if atoms_to_delete_ids:
            self.atoms_to_delete_ids = atoms_to_delete_ids
            self.n_atoms_to_delete = len(atoms_to_delete_ids)

        # Parameters to setup orientation
        self.sphere_center_atom_ids = sphere_center_atom_ids
        self.z_ax_atom_ids = z_ax_atom_ids
        self.xz_plane_atoms_ids = xz_plane_atoms_ids

        self.n_sphere_center_atoms: int = len(sphere_center_atom_ids)
        self.n_z_atoms: int = len(z_ax_atom_ids)
        self.n_xz_plane_atoms: int = len(xz_plane_atoms_ids)

        self.sphere_radius = sphere_radius
        self.displacement = displacement
        self.mesh_size = mesh_size
        self.remove_H = remove_H  # pylint: disable=invalid-name
        self.orient_z = orient_z
        self.write_surf_files = write_surf_files

        # open the xyz file, read the data
        with open(xyz_filepath, "r") as file:
            self.xyz_data: List[str] = file.readlines()

        # assign the path to the calculator
        self.path_to_sambvcax = path_to_sambvcax

    def write_input(self, inp_filepath: str) -> None:
        """
        Write input for the Sambvca buried-volume Fortran calculator based on the data entered
        when object was initialized.
        """
        # make file in the same cwd, which is where sambvca will look

        try:
            with open(inp_filepath, "w") as file:
                # write atoms to be deleted, if there are any
                if self.atoms_to_delete_ids:
                    file.writelines(
                        [
                            str(self.n_atoms_to_delete) + "\n",
                            str(self.atoms_to_delete_ids)
                            .replace(",", "")
                            .replace("[", "")
                            .replace("]", "")
                            + "\n",
                        ]
                    )
                else:
                    file.write("0\n")

                # write user settings
                file.writelines(
                    [
                        str(self.n_sphere_center_atoms) + "\n",
                        str(self.sphere_center_atom_ids)
                        .replace(",", "")
                        .replace("[", "")
                        .replace("]", "")
                        + "\n",
                        str(self.n_z_atoms) + "\n",
                        str(self.z_ax_atom_ids).replace(",", "").replace("[", "").replace("]", "")
                        + "\n",
                        str(self.n_xz_plane_atoms) + "\n",
                        str(self.xz_plane_atoms_ids)
                        .replace(",", "")
                        .replace("[", "")
                        .replace("]", "")
                        + "\n",
                        str(self.sphere_radius) + "\n",
                        str(self.displacement) + "\n",
                        str(self.mesh_size) + "\n",
                        str(self.remove_H) + "\n",
                        str(self.orient_z) + "\n",
                        str(self.write_surf_files) + "\n",
                        str(len(radii_table)) + "\n",
                    ]
                )
                # write radii
                file.writelines(radii_table)
                # write the atom coordinates
                file.writelines(self.xyz_data)
                file.close()
        except FileNotFoundError as err:
            raise FileNotFoundError("Unable to write input file.") from err

    def calc(self, inp_filepath: str) -> None:
        """
        Call SambVca based on the executable path given on initiliazation of py2sambvca.
        Be sure to write_input() before calling this function.
        """

        if not os.path.exists(inp_filepath):
            raise FileNotFoundError(
                """The given .inp file does not exist.
                Check that .inp file was successfully
                generated at the appropriate location."""
            )

        # sambvca.x reads the inp file without the .inp file extension
        inp_filename = inp_filepath.split(".", 1)[0]

        try:
            subprocess.run(
                [self.path_to_sambvcax, inp_filename],
                stderr=subprocess.DEVNULL,
                check=True,
            )
            print("Calculation successful.")
        except subprocess.CalledProcessError as calculation_error:
            raise Exception("Calculation failed.") from calculation_error

    # pylint: disable=too-many-locals
    @staticmethod
    def extract_calc_results(out_filepath: str) -> Dict[Any, Any]:
        """Retrieves the buried volume from a SambVca output file in the current working directory
        or False if it cannot find it.

        Args:
            out_filepath (str): [description]

        Raises:
            FileNotFoundError: [description]

        Returns:
            Dict[Any, Any]: [description]
        """
        if not os.path.exists(out_filepath):
            raise FileNotFoundError(
                """The given .out file does not exist. Please run the calculation first and
                check that .out file was successfully generated at the appropriate location."""
            )

        # open the file, read data
        with open(out_filepath, "r") as file:
            lines = file.readlines()

            vbur_percent_pattern = re.compile(r".*The %V Bur of the molecule is:[ ]{1,}(\d*\.\d*)")
            vbur_pattern = re.compile(r".*Buried volume =[ ]{1,}(\d*\.\d*)")
            quad_pattern = re.compile(r".*Quadrants analysis")
            oct_pattern = re.compile(r".*Octants analysis")
            file.close()

        outputs = {
            "Buried Volume %": None,
            "Buried Volume": None,
            "Quadrant Data": None,
            "Octant Data": None,
        }


        for line_num, line in enumerate(lines):
            vbur_percent_match = vbur_percent_pattern.search(line)
            vbur_match = vbur_pattern.search(line)
            quad_match = quad_pattern.search(line)
            oct_match = oct_pattern.search(line)

            if vbur_match:
                outputs["Buried Volume"] = float(vbur_match[1])
            elif vbur_percent_match:
                outputs["Buried Volume %"] = float(vbur_percent_match[1])
            elif quad_match:
                start = line_num + 2
                end = start + 4
                quad_data = [
                    list(map(str, v.replace("\n", "").strip().split())) for v in lines[start:end]
                ]
                outputs["Quadrant Data"] = pd.DataFrame(
                    quad_data, columns=["Quadrant", "Vf", "Vb", "Vt", "%Vf", "%Vb"]
                )
            elif oct_match:
                start = line_num + 2
                end = start + 8
                oct_data = [
                    list(map(str, v.replace("\n", "").strip().split())) for v in lines[start:end]
                ]
                outputs["Octant Data"] = pd.DataFrame(oct_data, columns=["Octant", "Vf", "Vb", "Vt", "%Vf", "%Vb"])

        if any(val is None for val in list(outputs.values())):
            raise ValueError("Some values are missing, please check the .out file manually.")
        return outputs

    @staticmethod
    def clean_files() -> None:
        """
        Remove all input and output files associated with py2sambvca.
        """
        for i in glob.glob("py2sambvca_input*"):
            os.remove(i)
