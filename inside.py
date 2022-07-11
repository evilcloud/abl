from urllib.request import urlopen
import json
import time


def get_github_version():
    """
    It opens a URL, reads the JSON data, and returns the version and update information.
    :return: A tuple of the version and update
    """
    url = 'https://raw.githubusercontent.com/evilcloud/abl/main/version.json'
    response = urlopen(url)
    data_json = json.loads(response.read())
    print(data_json)
    version = data_json.get("version", None)
    update = data_json.get("update", False)
    emergency = data_json.get("emergency", False)
    return (version, update, emergency)


def load_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def get_version() -> str:
    data = load_json("version.json")
    version = data.get("version", None)
    return version


def start():
    while True:
        current_version = get_version()
        new_version, update, emergency = get_github_version()
        print(new_version, current_version)
        if emergency:
            return "EMERGENCY"
        if current_version != new_version:
            print(
                f"New version {new_version} detected. Updating from version {current_version}")
            if update:
                print(
                    f"The UPDATE instruction has been issued. Attempting to update now...")
                return "UPDATE"
        time.sleep(10)
