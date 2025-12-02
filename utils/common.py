import pathlib
import sys


def get_project_root():
    entry_point = pathlib.Path(sys.argv[0]).resolve()

    current_dir = entry_point
    while current_dir.name != 'Autonomous_security_robot':
        if current_dir.parent == current_dir: 
            raise FileNotFoundError("Could not find the project root directory.")
        current_dir = current_dir.parent
    
    return current_dir

def resolve_project_path(relative_path_str):
    project_root = get_project_root()
    return project_root / pathlib.Path(relative_path_str)
  
def p():
  print("worked")