import abel
import sys


def run(wallet):
    wallet = True if wallet == '-p' or wallet == '--primary' else False
    print(f"Col lanuching {'WALLET' if wallet else 'CLUSTER'}")
    ret = abel.run(wallet)
    if ret == "EMERGENCY":
        sys.exit(1)
    else:
        sys.exit(0)
