import os

# Define the folder below below "ui", that contains the existing code base, set to "." if ui is toplevel
# main_level = "./desktop"

# Define the root directory where you want to start searching for QML files
root_directory = '.'

all_modules = []
all_subdirs = []
all_replace_cmds = []

root_module = ""

# Define a function to generate the CMakeLists.txt content for a directory
def generate_cmake_lists(path, qml_files):
    global root_module
    global all_modules
    global all_subdirs
    global all_replace_cmds
    global top_level

    directory = os.path.basename(path)
    # print(f'{directory} => {path}')

    if path == ".":
        module_name = f'ui'
        uri = f'ui'
    else:
        module_name = f'ui_{path.replace("./", "").replace("/", "_")}'
        uri = f'ui.{path.replace("./", "").replace("/", ".")}'

    cmake_content = f'qt_add_library({module_name} STATIC)\n\n'

    print(f'Write module {module_name}')

    if path == ".":
        root_module = module_name
    else:
        all_modules.append(module_name)
        all_subdirs.append(path)

    if not "+" in directory:
        if path == ".":
            rx = f'import "\.+.*"' # "import ".." etc. => top level module
        else:
            rx = f'import ".*{directory}"'

        replace_cmd = f"git grep -E -l '{rx}' | xargs gsed -i -E -e 's/{rx}/import {uri}/g'"
        all_replace_cmds.append(replace_cmd)

    if qml_files:
        cmake_content += f'qt_add_qml_module({module_name}\n  URI {uri}\n  VERSION 1.0\n  QML_FILES\n'
        for qml_file in qml_files:
            cmake_content += f'    {os.path.basename(qml_file)}\n'
        cmake_content += ')\n'

    return cmake_content

# Traverse the directory structure
for root, dirs, files in os.walk(root_directory):
    qml_files = [os.path.join(root, file) for file in files if file.endswith('.qml')]
    qml_files.sort()
    
    if qml_files:
        cmake_lists_path = os.path.join(root, 'CMakeLists.txt')
        
        with open(cmake_lists_path, 'w') as cmake_lists_file:
            cmake_lists_file.write(generate_cmake_lists(root, qml_files))

print("CMakeLists.txt generation completed.")

all_modules.sort()
all_subdirs.sort()

root_cmakelist = os.path.join(root_directory, 'CMakeLists.txt')

with open(root_cmakelist, "a") as f:
    f.write('\n')

    for subdir in all_subdirs:
        f.write(f'add_subdirectory({subdir})\n')
    f.write('\n')

    f.write(f'target_link_libraries({root_module} PRIVATE\n')
    for module in all_modules:
        f.write(f'  {module}plugin\n')
    f.write(')\n')

with open("fix_imports.sh", "w") as f:
    # the top one is too generic
    all_replace_cmds.append(all_replace_cmds.pop(0))

    for cmd in all_replace_cmds:
        f.write(f'{cmd}\n')
