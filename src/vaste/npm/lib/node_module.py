from genericpath import exists
import json
import os
from vaste.npm.macro.node_module import NodeModuleJsMacro


def get(name):
    if exists("packages.json"):
        with open("packages.json", "r") as file:
            packages_dict = json.load(file)
    else:
        packages_dict = {"dependencies": {}}
    if name not in packages_dict.keys():
        os.system(f"npm install {name}")
    return NodeModuleJsMacro(name)


def get_file(path):
    return NodeModuleJsMacro(path)
