from urllib.request import urlopen
import json
import sys
import os
import time
import subprocess
import shutil
import git

if "git" not in sys.modules:
    print("Force-installing git module")
    subprocess.call(["pip3", "install", "GitPython"])
    import git

    if "git" not in sys.modules:
        print("GitPython module failed to load")
        sys.exit(1)
    print("Git module installed successfully. Continuing...")


def get_github_version(url) -> dict:
    """
    It opens a URL, reads the JSON data, and returns the version and update information.
    :return: A tuple of the version and update
    """
    response = urlopen(url)
    data_json = json.loads(response.read())
    response.close()
    version = data_json.get("version", None)
    update = data_json.get("update", False)
    emergency = data_json.get("emergency", False)
    return {"version": version, "update": update, "emergency": emergency}


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
    print(f"Moving {len(files)} files from {update_storage} to {update_destination}")
    for file in files:
        if file.startswith("."):
            continue
        print(f"... moving {file}", end="")
        shutil.move(
            os.path.join(update_storage, file), os.path.join(update_destination, file)
        )
        time.sleep(0.5)
        print(f"\t done.")


def force_install(pip_module, package_name=None):
    package_name = package_name if package_name else pip_module
    if pip_module not in sys.modules:
        print(f"Force-installing {package_name} module")
        subprocess.call(["pip3", "install", package_name])

        if pip_module not in sys.modules:
            print(f"{package_name} module failed to load. Exiting...")
            return False
    print(f"{package_name} module installed successfully. Continuing...")
    return True
