from typing import List

def atoms_to_string(atoms_list: List[int]) -> str:
    return str(atoms_list).strip("[]").replace(",", "_").replace(" ","")