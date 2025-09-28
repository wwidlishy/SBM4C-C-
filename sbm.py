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
    while extenstion.lower() not in ["exe", "asm", "obj", "lib"]:
        extenstion = input(" What is your desired output? [exe/asm/obj/lib] ")

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
    for i in ["dist", "build", "last"]:
        folder = Path(directory + f"/{i}")

        for item in folder.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print(f"{Fore.GREEN} Cleaned: '{i}'. {Style.RESET_ALL}")

if option == "build" or option == "rebuild":
    build_files = []

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
    flags = ""

    try:
        compiler = config.get("compiler", "compiler")
        standard = config.get("compiler", "standard")
        output = config.get("compiler", "output")
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

    for module in [entry for entry in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, entry))]:
        
        print(f"{Fore.GREEN} Compiling module '{module}' {Style.RESET_ALL}")
        if not os.path.exists(directory + f"/build/modules/{module}"):
            os.makedirs(directory + f"/build/modules/{module}")


        folder_path = Path(directory + f"/modules/{module}")
        c_files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix in ([".c"] if compiler == "gcc" else [".cpp", ".c++"])[0]]

        for cf in c_files:
            try:
                f1 = open(cf.resolve()).read()
                f2 = open(directory + f"/last/modules/{module}/{cf.stem + cf.suffix}").read()
                if (f1 == f2):
                    print(f"{Fore.YELLOW} SKIPPED (No source modification). {Style.RESET_ALL}")
                    continue

            except:
                pass

            command = f"  {compiler} -I{directory}/include -c -std={standard} -o {directory}/build/modules/{module}/{cf.stem}.o {cf.resolve()} "
            try:
                command += config.get(f"m_{module}", "flags")
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

            source_file = cf.resolve()
            destination_folder = directory + f"/last/modules/{module}"

            Path(destination_folder).mkdir(parents=True, exist_ok=True)
            shutil.copy(source_file, destination_folder)



    directory2 = Path(directory + "/build")
    o_files = list(directory2.rglob("*.o"))
    o_files = [str(i) for i in o_files]
    print(f"{Fore.GREEN} Linking modules {Style.RESET_ALL}")
    command = f"  {compiler} -I{directory}/include -std={standard} -o {directory}/{output} {' '.join(o_files)}"
    print(command)
    result = os.system(command)

    if result == 0:
        print(f"{Fore.GREEN} Program build into {output} {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} [compilation failed] {Style.RESET_ALL}")