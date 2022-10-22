from genericpath import exists
import json
import os
from vaste.npm.macro.node_module import NodeModuleJsMacro


def get(name, extra_files = []):
    if exists("package.json"):
        with open("package.json", "r") as file:
            packages_dict = json.load(file)
    else:
        packages_dict = {"dependencies": {}}
    if name not in packages_dict["dependencies"].keys():
        os.system(f"npm install {name}")
    return NodeModuleJsMacro(name, extra_files)


def get_file(path):
    return NodeModuleJsMacro(path)
