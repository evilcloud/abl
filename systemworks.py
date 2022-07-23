import os
import sys
import socket
import json


def load_json(filename: str) -> dict:
    """
    It tries to open a file, and if it can't, it returns None

    :param filename: The name of the file to load
    :type filename: str
    :return: A dictionary
    """
    if os.path.isfile(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("error loading json file")
    else:
        print(f"JSON file {filename} not found")
        return {}


def write_json(data: dict, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)


def get_os() -> str:
    """
    It returns the name of the operating system that the program is running on
    :return: The operating system of the computer.
    """
    ops = sys.platform.lower()
    if ops == "darwin":
        ret = "macOS"
    elif ops == "win32":
        ret = "Windows"
    elif ops.startswith("linux"):
        ret = "Linux"
    else:
        ret = "unidentified"
    return ret


def is_mac():
    ops = get_os()
    return True if ops else False


def get_machine_name() -> str:
    """
    It reads the machine name from a file, if it exists, or prompts the user for a machine name if it
    doesn't
    :return: The machine name.
    """
    machine = None
    if os.path.isfile("machine"):
        with open("machine") as f:
            machine = f.read()
    if not machine:
        machine = socket.gethostname()
        if not machine or machine == "localhost":
            print("no valid machine name found")
            machine = input("Enter a valid machine name: ")
            if not machine:
                print("no valid machine name found")
                sys.exit(1)
    return machine.strip("\n").strip()


def get_version() -> str:
    """
    It loads the version.json file and returns the version number
    :return: The version of the program.
    """
    data = load_json("version.json")
    if data:
        version = data.get("version", None)
    else:
        version = "unknown"
    return version
