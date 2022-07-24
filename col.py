import abel
import sys


def run(wallet):
    wallet = True if wallet == 'wallet' else False
    ret = abel.run(wallet)
    if ret == "EMERGENCY":
        sys.exit(1)
    else:
        sys.exit(0)
