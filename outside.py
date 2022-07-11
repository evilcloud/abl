from urllib.request import urlopen
import time
import git
import shutil
import os
import inside
import sys

VERSION = '0.0.1'


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
        if file == "version.json":
            input("version")
        print(f"... moving {file}", end="")
        shutil.move(os.path.join(update_storage, file),
                    os.path.join(update_destination, file))
        time.sleep(0.5)
        print(f"\t done.")


repo_url = "https://github.com/evilcloud/abl"
update_destination = os.getcwd()
update_storage = os.path.join(update_destination, "update")

while True:
    inside_data = inside.start()
    if inside_data == ("EMERGENCY"):
        print("Emergency stop signal received. Shutting down...")
        sys.exit(0)
    if inside_data == ("UPDATE"):
        print("Updating process(outside) initiated")
        print("Fetching update")
        clone_repo(repo_url, update_storage)
        print("Updating...")
        update_files(update_destination, update_storage)
        print("Done.")
        print("Restarting main process")
    time.sleep(1)
