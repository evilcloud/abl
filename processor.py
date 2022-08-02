from copy import copy
from datetime import datetime
import os
import sys
import subprocess
import json
import systemworks
import datetime
from urllib.request import urlopen

DATETIME_STR = "%Y-%m-%dT%H:%M:%S"


def get_data(rpcuser, rpcpass):
    """
    It runs the `start_abectl.sh` script with the `getbalancesabe` command, and returns the output as a
    Python dictionary

    :param mac: if you're on a mac, you'll need to use the temp.json file to get the data
    :return: A list of dictionaries.
    """
    abectl_list = f"./start_abectl.sh --rpcuser={rpcuser} --rpcpass={rpcpass} --wallet getbalancesabe".split()
    is_mac = sys.platform.lower() == "darwin"
    if is_mac:  # macos can not handle the stdout pipe properly
        _ = os.popen(f"{' '.join(abectl_list)} > temp.json")
        ret = systemworks.load_json("temp.json")
    else:
        proc = subprocess.Popen(abectl_list, stdout=subprocess.PIPE)
        try:
            ret = json.loads(proc.stdout.read().decode("utf-8"))
        except Exception:
            print("Error parsing JSON. Returning empty dictionary")
            ret = {}
    return ret


def get_data_2():
    return systemworks.load_json("test.json")


def get_github_version(url) -> dict:
    """
    It opens a URL, reads the JSON data, and returns the version and update information.
    In case of failure everything is denied
    :return: A tuple of the version and update
    """
    try:
        response = urlopen(url)
        data_json = json.loads(response.read())
        response.close()
        version = data_json.get("version", None)
        update = data_json.get("update", False)
        emergency = data_json.get("emergency", False)
    except Exception as e:
        print(f"Failed to load version data from {url}\n{e}")
        version = None
        update = False
        emergency = False
    return {"version": version, "update": update, "emergency": emergency}


# Class responsible for the current machine state within the scope of miner report
# The calss should be acesses only though the difference class
class _Adata:
    def __init__(self, wallet: bool = False):
        self.os = systemworks.get_os()
        self.machine = systemworks.get_machine_name()
        self.software_version = systemworks.get_version()
        self.wallet = wallet
        self.programmatic = True
        self.total_balance = 0
        self.current_height = 0
        self.update_time = datetime.datetime.utcnow()
        self.update_time_str = self.update_time.strftime(DATETIME_STR)

    def update_data(self, data):
        self.total_balance = int(data.get("total_balance", self.total_balance))
        self.current_height = int(
            data.get("current_height", self.current_height))
        self.update_time = datetime.datetime.utcnow()
        self.update_time_str = self.update_time.strftime("%Y-%m-%dT%H:%M:%S")


# Central access point to the current transaction, previous transaction and the difference between these tranactions
class Datadiff:
    def __init__(self, wallet=False):
        self.wallet = wallet
        self.old = _Adata(wallet)
        self.new = _Adata(wallet)
        self.machine = self.new.machine
        self.os = self.new.os
        self.version = self.new.software_version
        self.total_balance = self.new.total_balance
        self.current_height = self.new.current_height
        self.update_time = self.new.update_time
        self.update_time_str = self.new.update_time.strftime(DATETIME_STR)
        self.programmatic = self.new.programmatic
        self.ping_time = datetime.datetime.utcnow()
        self.ping_delta_time = "00:00:00"
        self.ping_block = 0
        self.ping_delta_block = 0

    def update(self, data):
        self.old = copy(self.new)
        self.new.update_data(data)
        self.total_balance = self.new.total_balance
        self.current_height = self.new.current_height
        self.update_amount = self.new.total_balance - self.old.total_balance
        self.update_period = self.new.update_time - self.old.update_time
        self.update_period_str = str(self.update_period).split(".")[0]
        self.update_block_diff = self.new.current_height - self.old.current_height
        self.old = copy(self.new)

    def ping(self, current_height: int, cpu_percent: int):
        self.ping_time = datetime.datetime.utcnow()
        self.cpu_percent = cpu_percent
        self.ping_time_str = self.ping_time.strftime(DATETIME_STR)
        self.ping_delta_time = datetime.datetime.utcnow() - self.new.update_time
        self.ping_delta_time_str = str(self.ping_delta_time).split(".")[0]
        self.ping_block = current_height
        self.ping_delta_block = self.ping_block - self.new.current_height
