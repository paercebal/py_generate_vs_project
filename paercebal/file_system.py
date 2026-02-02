import os
import paercebal.user_data
from pathlib import Path


def create_directory(p_parent_path, p_new_directory_name, p_ignore_already_exist_error = True):
    #os.path.sep
    new_directory = os.path.join(p_parent_path, p_new_directory_name)
    Path("/my/directory").mkdir(parents=True, exist_ok=True)
    return new_directory


def create_directory_structure(p_user_data):
    Path(p_user_data.get_solution_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_module_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_vs2017_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_vs2019_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_vs2022_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_vs2026_directory()).mkdir(parents=True, exist_ok=True)
    #Path(p_user_data.get_gcc11_directory()).mkdir(parents=True, exist_ok=True)
    #Path(p_user_data.get_gcc14_directory()).mkdir(parents=True, exist_ok=True)
    #Path(p_user_data.get_gcc17_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_gcc20_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_gcc23_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_gcc26_directory()).mkdir(parents=True, exist_ok=True)
    Path(p_user_data.get_base_private_directory()).mkdir(parents=True, exist_ok=True)
    if p_user_data.m_module_type == 'DLL':
        Path(p_user_data.get_base_public_directory()).mkdir(parents=True, exist_ok=True)












