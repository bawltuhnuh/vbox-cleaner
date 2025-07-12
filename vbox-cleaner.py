import os
import shutil

REMOVE = False

cwd = os.getcwd()

def get_paths(directory: str, paths: list = None):
    paths = paths if paths is not None else []
    directories = [file for file in os.listdir(directory) if os.path.isdir(os.path.join(directory, file))]
    for file in directories:
        if file in ["Snapshots", "Logs"]:
            paths.append(directory)
            return
        path = os.path.join(directory, file)
        get_paths(path, paths)
    return paths

def get_files_with_ext(path: str, ext: str):
    files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(ext)]
    return files

def get_sav(path: str):
    return get_files_with_ext(path, '.sav')

def get_nvram(path: str):
    return get_files_with_ext(path, '.nvram')

def extract_sav_and_nvram(path: str):
    def extract_ext(line: str, ext: str):
        parts = line.split('"')
        for part in parts:
            if ext in part:
                return os.path.join(path, part)

    vm_file = os.path.join(path, f'{os.path.basename(path)}.vbox')
    if not os.path.exists(vm_file):
        return None

    files = []

    with open(vm_file, "r") as file:
        for line in file:
            if '.sav' in line:
                files.append(extract_ext(line, '.sav'))
            elif '.nvram' in line:
                files.append(extract_ext(line, '.nvram'))
    return files

vm_paths = get_paths(cwd)

remove = []

for vm in vm_paths:
    snaphots_path = os.path.join(vm, 'Snapshots')
    if not os.path.exists(snaphots_path):
        continue
    files = get_sav(snaphots_path)
    files.extend(get_nvram(snaphots_path))

    paths = extract_sav_and_nvram(vm)

    if paths is None:
        remove.append(vm)
        continue

    for file in files:
        if file not in paths:
            remove.append(file)
if REMOVE:
    for path in remove:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
else:
    print(*remove, sep='\n')
