import abel
import sys


def run(cluster):
    wallet = True if cluster == '-p' else False
    ret = abel.run(wallet)
    if ret == "EMERGENCY":
        sys.exit(1)
    else:
        sys.exit(0)
