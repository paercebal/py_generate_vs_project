import json

class configuration:

    def __init__(self):
        self.parent_directories = [r'D:\_rbr\dev\cpp']
        self.root_namespace = r'paercebal'
        self.application_name = r'my_app'
        self.module_name = 'my_module'
        self.explicit_vcpkg_paercebal = False
        self.open_explorer_on_finish = True
        self.message_box_on_finish = True

def load_configuration(p_path):
    # Open and read the JSON file
    with open(p_path, 'r') as file:
        data = json.load(file)
    return data

def save_configuration(p_path, p_configuration):
    with open(p_path, 'w') as file:
        json.dump(p_configuration, file, indent=3)

