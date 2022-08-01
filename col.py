from ast import arg
import abel
import sys
import subprocess


def run(wallet):
    subprocess.call(['pip3', 'install', 'deta'])
    subprocess.call(['pip3', 'install', 'humanize'])
    wallet = True if wallet == '-p' or wallet == '--primary' else False

    print(f"Col lanuching {'WALLET' if wallet else 'CLUSTER'}")
    ret = abel.start(wallet)
    if ret == "EMERGENCY":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    print(arg1)
    input(arg1)
    run(arg1)
