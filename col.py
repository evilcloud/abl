import json
import time
import sys
import socket
import subprocess
from configparser import ConfigParser
import os
from urllib.request import urlopen


# Read config.ini file


def load_json(filename: str) -> dict:
    """
    It tries to open a file, and if it can't, it returns None

    :param filename: The name of the file to load
    :type filename: str
    :return: A dictionary
    """
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def write_json(data: str, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)


def get_version() -> str:
    """
    It loads the version.json file and returns the version number
    :return: The version of the program.
    """
    data = load_json("version.json")
    version = data.get("version", None)
    return version


def get_github_version():
    """
    It opens a URL, reads the JSON data, and returns the version and update information.
    :return: A tuple of the version and update
    """
    url = 'https://raw.githubusercontent.com/evilcloud/abl/main/version.json'
    response = urlopen(url)
    data_json = json.loads(response.read())
    response.close()
    version = data_json.get("version", None)
    update = data_json.get("update", False)
    emergency = data_json.get("emergency", False)
    return (version, update, emergency)


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


def get_machine() -> str:
    """
    It gets the machine name, and if it's not valid, it prompts the user to enter a valid one
    :return: The machine name.
    """
    machine = socket.gethostname()
    if not machine or machine == "localhost":
        print("no valid machine name found")
        machine = input("Enter a valid machine name: ")
        if not machine:
            print("no valid machine name found")
            sys.exit(1)
    return machine


def get_data(mac=None):
    """
    It runs the `start_abectl.sh` script with the `getbalancesabe` command, and returns the output as a
    Python dictionary

    :param mac: if you're on a mac, you'll need to use the temp.json file to get the data
    :return: A list of dictionaries.
    """
    rpcuser = os.environ.get("RPC_USER", None)
    rpcpass = os.environ.get("RPC_PASS", None)
    if not rpcuser or not rpcpass:
        print("no RPC_USER and/or RPC_PASS environment variables found")
        sys.exit(1)
    abectl_list = f'./start_abectl.sh --rpcuser={rpcuser} --rpcpass={rpcpass} --wallet getbalancesabe'.split()
    if mac:
        _ = os.popen(
            f"{' '.join(abectl_list)} > temp.json"
        )
        return load_json("temp.json")

    proc = subprocess.Popen(abectl_list, stdout=subprocess.PIPE)
    return json.loads(proc.stdout.read().decode("utf-8"))


def format_time(t):
    """
    It takes a string in the format of a time-date string, and returns a string in the format of an ISO
    8601 time-date string

    :param t: The time of the tweet
    :return: A string in the format of a datetime object.
    """
    td_date, td_time, offset, timezone, *_ = t.split(" ")
    td_time = td_time.split(".")[0]
    offset = offset[1:3] + ":" + offset[3:]
    return f"{td_date}T{td_time}Z"


def get_config() -> dict:
    """
    It checks if the file col.ini exists, and if it does, it loads the configuration from the file,
    otherwise it loads the default configuration
    :return: A dictionary with the keys "measurement", "host", and "location"
    """
    if os.path.isfile("col.ini"):
        print("col.ini found. Loading configuration from the file")
        config_object = ConfigParser()
        config_object.read("col.ini")
        measurement = config_object["DATA"]["measurement"]
        host = config_object["DATA"]["host"]
        location = config_object["DATA"]["location"]
    else:
        print("col.ini not found. Loading default configuration")
        measurement = "mining"
        host = "Linode"
        location = "VPS"
    return {"measurement": measurement, "host": host, "location": location}


class Indata:
    def __init__(self):
        ini_data = get_config()
        self.measurement = ini_data["measurement"]
        self.host = ini_data["host"]
        self.location = ini_data["location"]
        self.os = get_os()
        self.machine = get_machine()
        self.col_version = get_version()
        self.total_balance = 0
        self.current_height = 0

    def update_data(self, data):
        if data.get("total_balance"):
            self.total_balance = int(data["total_balance"])
        if data.get("current_height"):
            self.current_height = int(data["current_height"])
        if data.get("current_time"):
            self.current_time = format_time(data["current_time"])
        else:
            delattr(Indata, "current_time")


class Inping:
    def __init__(self):
        # config_object = ConfigParser()
        # config_object.read("col.ini")
        self.measurement = "blockchain"
        self.machine = get_machine()
        self.col_version = get_version()
        self.current_height = 0

    def update_data(self, data):
        if data.get("current_height"):
            self.current_height = int(data["current_height"])
        else:
            pass


def run(cluster, main_launch=False):
    current_version = get_version()
    print_cluster = " CLUSTER" if cluster else " PRIMARY"
    print(f"Pinger v. {current_version} {print_cluster}")

    filename = "tel.json"

    old_data = Indata()
    print("Machine:", old_data.machine)
    new_data = Indata()
    empty_data = {}
    write = True if old_data.os == "macOS" else None

    # block ping
    ping_data = Inping()

    while True:
        if main_launch:
            new_version, update, emergency = get_github_version()
            if emergency:
                return "EMERGENCY"
            if current_version != new_version:
                print(
                    f"New version {new_version} detected. Updating from version {current_version}")
                if update:
                    print(
                        f"The UPDATE instruction has been issued. Attempting to update now...")
                    return "UPDATE"

        data = get_data(write)
        new_data.update_data(data)
        ping_data.update_data(data)
        time.sleep(0.1)
        write_json(ping_data.__dict__, filename)
        if old_data.total_balance != new_data.total_balance:
            print("New total balance:",
                  new_data.total_balance, new_data.current_time,)
            old_data.update_data(data)
            if cluster:
                print("Cluster version. No data is being written")
            else:
                write_json(new_data.__dict__, filename)
        time.sleep(9.9)


if __name__ == "__main__":
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    cluster = True
    if arg1:
        if arg1 == "-p" or arg1 == "--primary":
            cluster = False
        else:
            print("Unknown argument:", arg1)
            sys.exit(1)
    main_launch = True
    run(cluster, main_launch)
