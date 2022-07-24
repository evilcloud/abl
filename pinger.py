from ast import arg
import col
import sys
import os
import shutil
from urllib.request import urlopen
import subprocess
import time
try:
    import git
except ImportError:
    try:
        subprocess.call(['pip3', 'install', 'GitPython'])
        import git
    except subprocess.CalledProcessError:
        print("GitPython module failed to load")


VERSION = '1.0.0'


def clone_repo(repo_url: str, update_storage: str):
    """
    Clone a repo from GitHub.
    :param repo: Name of the repo to clone
    :return: The cloned repo
    """
    if os.path.exists(update_storage):
        print("Uncleaned update dicrectory exists. Force-cleaning directory.")
        shutil.rmtree(update_storage)
    print(f"Cloning repository {repo_url} into {update_storage}")
    git.Repo.clone_from(repo_url, update_storage)
    print("done.")


def update_files(update_destination: str, update_storage: str) -> None:
    files = os.listdir(update_storage)
    print(
        f"Moving {len(files)} files from {update_storage} to {update_destination}")
    for file in files:
        if file.startswith("."):
            continue
        print(f"... moving {file}", end="")
        shutil.move(os.path.join(update_storage, file),
                    os.path.join(update_destination, file))
        time.sleep(0.5)
        print(f"\t done.")


def launch_procedure(wallet):
    wallet = "wallet" if wallet else "no-wallet"
    print(f"Launching procedure with {wallet}")
    ret = subprocess.call(['python3', 'abel.py', wallet])
    if ret == 1:
        return "EMERGENCY"
    else:
        return "UPDATE"


def launch(wallet):
    repo_url = "https://github.com/evilcloud/abl"
    update_destination = os.getcwd()
    update_storage = os.path.join(update_destination, "update")

    while True:
        col_data = launch_procedure(wallet)
        if col_data == ("EMERGENCY"):
            print("Emergency stop signal received. Shutting down...")
            sys.exit(0)
        if col_data == ("UPDATE") and 'git' in sys.modules:
            print("Updating process(outside) initiated")
            print("Fetching update")
            clone_repo(repo_url, update_storage)
            print("Updating...")
            update_files(update_destination, update_storage)
            print("Done.")
            print("Restarting main process")
        time.sleep(1)


if __name__ == "__main__":
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    wallet = False
    if arg1:
        if arg1 == "-p" or arg1 == "--primary":
            print("launching WALLET")
        else:
            print("Unknown argument:", arg1)
            sys.exit(1)

    launch(wallet)
