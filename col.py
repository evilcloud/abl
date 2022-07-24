import abel
import sys
import subprocess


def run(wallet):
    subprocess.call(['pip3', 'install', 'deta'])
    subprocess.call(['pip3', 'install', 'humanize'])
    wallet = True if wallet == '-p' or wallet == '--primary' else False
    print(f"Col lanuching {'WALLET' if wallet else 'CLUSTER'}")
    ret = abel.run(wallet)
    if ret == "EMERGENCY":
        sys.exit(1)
    else:
        sys.exit(0)
