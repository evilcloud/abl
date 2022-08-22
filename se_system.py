import os
import pathlib
import socket
import sys
import json


def get_envs():
    keys = {"DETA_KEY": None, "RPC_USER": None, "RPC_PASS": None}

    for key in keys:
        keys[key] = os.environ.get(key, None)
        if not keys[key]:
            print(f"{key} not found in environment")
            sys.exit(1)
    return keys


def get_machine_name() -> str:
    machine = None
    if os.path.isfile("machine"):
        machine = pathlib.Path("machine").read_text()
        print(f"Machine identified as {machine} from the file")
    if not machine:
        machine = socket.gethostname()
        if not machine or machine == "localhost":
            print("no valid machine name found")
            sys.exit(1)
        print(f"Machine identified as {machine} from the hostname socket")
    return machine.strip("\n").strip()


def is_wallet():
    return bool(os.path.isfile("wallet"))


# def get_os() -> str:
#     ops = sys.platform.lower()
#     if ops == "darwin":
#         return "macOS"
#     elif ops == "win32":
#         return "Windows"
#     elif ops.startswith("linux"):
#         return "Linux"
#     else:
#         return "unidentified"


# def is_mac():
#     ops = get_os()
#     return ops == "macOS"


def load_json(filename: str) -> dict:
    if os.path.isfile(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("error loading json file")
    else:
        print(f"JSON file {filename} not found")
        return {}
