import subprocess
import json
import os
import se_system
import sys
import logging


def is_mac():
    return sys.platform.lower() == "darwin"


def get_data(rpcuser, rpcpass):
    abectl_list = f"./start_abectl.sh --rpcuser={rpcuser} --rpcpass={rpcpass} --wallet getbalancesabe".split()
    if is_mac():  # macos can not handle the stdout pipe properly
        _ = os.popen(f"{' '.join(abectl_list)} > temp.json")
        ret = se_system.load_json("temp.json")
    else:
        proc = subprocess.Popen(abectl_list, stdout=subprocess.PIPE)
        try:
            ret = json.loads(proc.stdout.read().decode("utf-8"))
        except Exception:
            print("Error parsing JSON. Returning empty dictionary")
            ret = {}
    return ret
