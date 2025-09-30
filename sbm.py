import sys
import os
import configparser
from pathlib import Path
import shutil

import colorama
from colorama import Fore, Back, Style
colorama.init()

option = ""
directory = ""


def get_files(folder_path: Path, extenstions):
    return [f for f in folder_path.rglob("*") if f.is_file() and f.suffix in extenstions]

if len(sys.argv) == 3:
    option = sys.argv[1]
    directory = sys.argv[2]
else:
    print(
"""Usage: sbm [new/build/clean/rebuild] project_directory
    example: sbm new .
    
    new - creates new project
    build - builds project
    clean - cleans all compiled files and caches
    rebuild = clean + build
    """
    )

    sys.exit(0)

if option == "new":
    if not os.path.exists(directory):
        print(f"{Fore.GREEN} Created project directory. {Style.RESET_ALL}")
        os.makedirs(directory)
    else:
        print(f"{Fore.GREEN} Project directory already present. {Style.RESET_ALL}")
        input(" Press any key if you want to continue (else cancel the command) ...")

    c_cpp = ""
    while c_cpp.lower() not in ["c", "cpp", "c++"]:
        c_cpp = input(" What programming language would you want to use? [C/CPP] ")

    c_cpp = c_cpp.replace("c++", "cpp")

    extenstion = ""
    extt = ""
    while extenstion.lower() not in ["exe", "obj"]:
        extenstion = input(" What is your desired output? [exe/obj] ")
        extt = str(extenstion)

    standards = ["c89", "c90", "c95", "c99", "c11", "c17", "c23", "gnu89", "gnu90", "gnu95", "gnu99", "gnu11", "gnu17", "gnu23"]
    if c_cpp == "cpp":
        standards = ["c++98", "c++03", "c++11", "c++14", "c++17", "c++20", "c++23", "gnu++98", "gnu++03", "gnu++11", "gnu++14", "gnu++17", "gnu++20", "gnu++23"]

    standard = "" 
    while standard not in standards:
        standard = input(f" What standard? [{'/'.join(standards)}] ")

    if sys.platform == "linux":
        extenstion = extenstion.replace("exe", "out")
        extenstion = extenstion.replace("obj", "o")
    if sys.platform == "win32":
        extenstion = extenstion.replace("lib", "dll")

    try:
        f = open(directory + "/__sbmconfig__", 'w')
    except OSError:
        print(f"{Fore.RED} Unable to create config.\n [compilation terminated] {Style.RESET_ALL}")
        sys.exit()

    with f:
        config = configparser.ConfigParser()

        config["compiler"] = {
            "compiler": "gcc" if c_cpp == "c" else "g++",
            "standard": standard,
            "output": f"dist/output.{extenstion}",
            "type": extt,
            "flags": ""
        }

        config.write(f)
        print(f"{Fore.GREEN} Written config. {Style.RESET_ALL}")

    if not os.path.exists(directory + "/include"):
        print(f"{Fore.GREEN} Created include directory. {Style.RESET_ALL}")
        os.makedirs(directory + "/include")

    if not os.path.exists(directory + "/last"):
        print(f"{Fore.GREEN} Created last directory. {Style.RESET_ALL}")
        os.makedirs(directory + "/last")

    if not os.path.exists(directory + "/build"):
        print(f"{Fore.GREEN} Created build directory. {Style.RESET_ALL}")
        os.makedirs(directory + "/build")

    if not os.path.exists(directory + "/dist"):
        print(f"{Fore.GREEN} Created dist directory. {Style.RESET_ALL}")
        os.makedirs(directory + "/dist")

    if not os.path.exists(directory + "/modules"):
        print(f"{Fore.GREEN} Created modules directory. {Style.RESET_ALL}")
        os.makedirs(directory + "/modules")

    if not os.path.exists(directory + "/modules/main"):
        print(f"{Fore.GREEN} Created modules/main directory. {Style.RESET_ALL}")
        os.makedirs(directory + "/modules/main")

    try:
        f = open(directory + f"/modules/main/main.{c_cpp}", 'w')
    except OSError:
        print(f"{Fore.RED} Unable to create /modules/main/main.{c_cpp}.\n [compilation terminated] {Style.RESET_ALL}")
        sys.exit()
    with f:
        f.write(
"""#include <stdio.h>

int main(int argc, char** argv) {
    printf("%s\\n", "Hello, world!");
    return 0;
}
""" if c_cpp == "c" else
"""#include <iostream>

int main(int argc, char** argv) {
    std::cout << "Hello, world!" << "\\n";
    return 0;
}
"""
        )
        print(f"{Fore.GREEN} Written /modules/main/main.{c_cpp}. {Style.RESET_ALL}")
    
if option == "clean" or option == "rebuild":
    print("~~== Cleaning ==~~")
    for i in ["dist", "build", "last"]:
        folder = Path(directory + f"/{i}")

        for item in folder.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print(f"{Fore.GREEN} Cleaned: '{i}'. {Style.RESET_ALL}")

def build_c(module, cf, force=False):
            try:
                f1 = open(cf.resolve()).read()
                destination_folder = directory + "/last/" + str(cf.relative_to(directory))
                if destination_folder.startswith("./"):
                    destination_folder = destination_folder[2:]

                f2 = open(destination_folder).read()
                if (f1 == f2 and os.path.exists(f"{directory}/build/modules/{module}/{cf.stem}.o") and not force):
                    print(f"{Fore.YELLOW} SKIPPED (No source modification). {Style.RESET_ALL}")
                    return 5

            except:
                pass

            command = f"  {compiler} -I{directory}/include -c -std={standard} -o {directory}/build/modules/{module}/{cf.stem}.o {cf.resolve()} "
            try:
                command += config.get(f"m_{module}", "flags")
            except:
                pass

            try:
                modules = config.get(f"m_{module}", "include").split(" ")
                includes = ""
                folder_path = directory + "/modules"
                for i in modules:
                    valid = False
                    for _module in [entry for entry in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, entry))]:
                        module_path = directory + f"/modules/{_module}"
                        if f"m_{_module}" == i:
                            valid = True
                            includes += f" -I{directory}/modules/{_module}"
                    if not valid:
                        print(f"{Fore.RED} Invalid module id 'm_{_module}'. {Style.RESET_ALL}")
                        sys.exit(0)
                command += includes
            except:
                pass

            print(command)
            exit_code = os.system(command)

            if exit_code == 0:
                print(f"{Fore.GREEN} SUCCESS. {Style.RESET_ALL}")
                build_files.append(f"{module}/{cf.stem}{cf.suffix}")

            else:
                print(f"{Fore.RED} FAILURE. \n [compilation terminated]{Style.RESET_ALL}")
                sys.exit(0)

            # source_file = cf.resolve()
            # destination_folder = directory + f"/last/modules/{module}"

            # Path(destination_folder).mkdir(parents=True, exist_ok=True)
            # shutil.copy(source_file, destination_folder)

def validate_mpath(directory, mpath, all_ext):
    mpath = mpath.split("/")
    if len(mpath) <= 1:
        return None
    
    folder_path = directory + "/modules"
    for module in [entry for entry in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, entry))]:
        module_path = directory + f"/modules/{module}"
        if f"m_{module}" == mpath[0]:
            if os.path.exists(module_path + "/" + "/".join(mpath[1:])):
                return module_path + "/" + "/".join(mpath[1:])
            else:
                return None
            
    return None

def is_mpath_same(directory, mpath, all_ext):
    mpath = mpath.split("/")
    if len(mpath) <= 1:
        return None
    
    folder_path = directory + "/modules"
    f1 = ""
    f2 = "-"

    for module in [entry for entry in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, entry))]:
        module_path = directory + f"/modules/{module}"
        if f"m_{module}" == mpath[0]:
            if os.path.exists(module_path + "/" + "/".join(mpath[1:])):
                f1 = open(module_path + "/" + "/".join(mpath[1:])).read()

    if os.path.exists(directory + "/last/modules"):
        folder_path = directory + "/last/modules"
        for module in [entry for entry in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, entry))]:
            module_path = directory + f"/last/modules/{module}"
            if f"m_{module}" == mpath[0]:
                if os.path.exists(str(module_path + "/" + "/".join(mpath[1:])).replace("\\", "/")):
                    f2 = open(module_path + "/" + "/".join(mpath[1:])).read()

    return f1 == f2

if option == "build" or option == "rebuild":
    build_files = []

    print("~~== Initial checks ==~~")
    if os.path.exists(directory):
        print(f"{Fore.GREEN} Project directory present. {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} Project directory doesn't exist. {Style.RESET_ALL}")
        sys.exit(0)

    config = configparser.ConfigParser()
    if os.path.exists(directory + "/__sbmconfig__"):
        print(f"{Fore.GREEN} Project config present. {Style.RESET_ALL}")
        config.read(directory + "/__sbmconfig__")
    else:
        print(f"{Fore.RED} Project config doesn't exist. {Style.RESET_ALL}")
        sys.exit(0)

    
    compiler = ""
    standard = ""
    output = ""
    type_ = ""
    flags = ""

    try:
        compiler = config.get("compiler", "compiler")
        standard = config.get("compiler", "standard")
        output = config.get("compiler", "output")
        type_ = config.get("compiler", "type")
        flags = config.get("compiler", "flags")
    except:
        print(f"{Fore.RED} Couldnt find required fields.\n Make sure [compiler] contains: compiler, standard, output, flags. {Style.RESET_ALL}")
        sys.exit(0)

    for i in ["build", "dist", "include", "last", "modules"]:
        if os.path.exists(directory + "/" + str(i)):
            print(f"{Fore.GREEN} {i} present. {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} {i} doesn't exist. {Style.RESET_ALL}")
            sys.exit(0)

    folder_path = directory + "/modules"
    num_folders = sum(
        1 for entry in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, entry))
    )

    print(f"{Fore.GREEN} Found {num_folders} modules. {Style.RESET_ALL}")
    print("~~== Compiling modules ==~~")

    for module in [entry for entry in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, entry))]:
        
        print(f"{Fore.GREEN} Compiling module '{module}' {Style.RESET_ALL}")
        if not os.path.exists(directory + f"/build/modules/{module}"):
            os.makedirs(directory + f"/build/modules/{module}")

        c_files = get_files(Path(directory + f"/modules/{module}"), [".c"] if compiler == "gcc" else [".c", ".cpp", ".c++"])

        for cf in c_files:
            if build_c(module, cf) != 5:
                build_files.append(str(cf).replace("\\", "/"))


    print("~~== Enforcing relations ==~~")
    relations = None
    try:
        relations = config["relations"].items()
    except:
        print(f"{Fore.YELLOW} No relations found. ignoring... {Style.RESET_ALL}")
    if relations:
        print(f"{Fore.GREEN} Found {len(relations)} {'relation' if len(relations) == 1 else 'relations'}. {Style.RESET_ALL}")
        for key, value in relations:
            _recompile = value.split(" ")
            actual_paths = []
            print(f"  {Fore.MAGENTA}if_changed{Style.RESET_ALL} {key} {Fore.MAGENTA}recompile{Style.RESET_ALL} {_recompile}")

            for index, mpath in enumerate([key] + _recompile):
                exts = [".c"] if compiler == "gcc" else [".c", ".cpp", ".c++"]
                if index == 0:
                    exts = [".c", ".h"] if compiler == "gcc" else [".c", ".cpp", ".c++", ".h", ".hpp", ".h++"]

                tpath = validate_mpath(directory, mpath, exts)
                if tpath == None:
                    print(f"  {Fore.RED}Invalid mpath '{mpath}'. \n [compilation terminated]{Style.RESET_ALL}")
                    sys.exit(0)
                actual_paths.append(tpath)
            if len(actual_paths) == 1:
                continue

            rebuild = not is_mpath_same(directory, key, [".c", ".h"] if compiler == "gcc" else [".c", ".cpp", ".c++", ".h", ".hpp", ".h++"])
            if rebuild:
                for index, ap in enumerate(actual_paths[1:]):
                    if ap not in build_files:
                        print(f" {Fore.GREEN}Rebuilding due to relation.{Style.RESET_ALL}")
                        build_c(_recompile[index].split("/")[0][len("m_"):], Path(actual_paths[index + 1]), True)
                    else:
                        print(f" {Fore.YELLOW}SKIPPED (already compiled).{Style.RESET_ALL}")

    for module in [entry for entry in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, entry))]:
        h_files = get_files(Path(directory + f"/modules/{module}"), [".c", ".h"] if compiler == "gcc" else [".c", ".cpp", ".c++", ".h", ".hpp", ".h++"])
        for hf in h_files:
            source_file = hf.resolve()

            destination_folder = f"{directory}/" + "last/" + str(hf.parent.relative_to(directory))
            if destination_folder.startswith("./"):
                destination_folder = destination_folder[2:]

            Path(destination_folder).mkdir(parents=True, exist_ok=True)
            shutil.copy(source_file, destination_folder)

    print("~~== Linking ==~~")
    o_files = get_files(Path(directory + "/build"), ".o")
    o_files = [str(i) for i in o_files]

    print(f"{Fore.GREEN} Linking modules {Style.RESET_ALL}")

    result = 0
    if type_ == "exe":
        command = f"  {compiler} -I{directory}/include -std={standard} -o {directory}/{output} {' '.join(o_files)} {flags}"
        print(command)
        result = os.system(command)
    elif type_ == "obj":
        command = f"  ar rcs {directory}/{output} {' '.join(o_files)}"
        print(command)
        result = os.system(command)
    else:
        print(f" {Fore.RED}Invalid type{Style.RESET_ALL}")

    print(f"~~== {Fore.CYAN}Finished{Style.RESET_ALL} ==~~")
    if result == 0:
        print(f"{Fore.GREEN} Program build into {output} {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} [compilation failed] {Style.RESET_ALL}")