import abel
import sys


def run(cluster):
    ret = abel.run(cluster)
    if ret == "EMERGENCY":
        sys.exit(1)
    else:
        sys.exit(0)
