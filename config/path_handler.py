import os
from pathlib import Path

current_directory = Path(os.path.dirname(os.path.abspath(__file__)))
project_dir = current_directory.parent

input_files_directory = Path(os.path.join(project_dir, "Inputs"))
output_files_directory = Path(os.path.join(project_dir, "Outputs"))
sambvca21_full_path = Path(os.path.join(project_dir, "Sambvca21_source//sambvca21.x"))
