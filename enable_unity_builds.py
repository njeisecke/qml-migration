import os

from common import *

# Define the folder below below "ui", that contains the existing code base, set to "." if ui is toplevel
# main_level = "./desktop"

# Define the root directory where you want to start searching for QML files
root_directory = '.'

# Define a function to generate the CMakeLists.txt content for a directory
def append_unity_build(path, qml_files):
    module_name = path_to_module_name(path)
    return f'\nset_target_properties({module_name} PROPERTIES\n  UNITY_BUILD ON\n)\n'

# Traverse the directory structure
for root, dirs, files in os.walk(root_directory):
    # follow the same logic: if there are .qml files, there now must be a CMakeLists.txt file
    qml_files = [os.path.join(root, file) for file in files if file.endswith('.qml')]
    
    if qml_files:
        cmake_lists_path = os.path.join(root, 'CMakeLists.txt')
        
        with open(cmake_lists_path, 'a') as cmake_lists_file:
            print(f'enable unity build in {cmake_lists_path}')
            cmake_lists_file.write(append_unity_build(root, qml_files))
