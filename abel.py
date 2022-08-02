import time
import processor
import database_interface
import systemworks
import humanize
import datetime
import sys
import subprocess
import logging
try:
    import psutil
except ImportError:
    subprocess.run(["pip3", "install", "psutil"])
    subprocess.run(["pip", "install", "psutil"])
    import psutil

logging.basicConfig(level=logging.CRITICAL)


def run():
    wallet = systemworks.is_wallet()
    process_data = processor.Datadiff(wallet)
    machine_name = process_data.machine

    current_data = {}

    PRC_USER = database_interface.Secrets.RPC_USER
    PRC_PASS = database_interface.Secrets.RPC_PASS
    deta_name_mining = database_interface.Secrets.deta_name_mining
    deta_name_ping = database_interface.Secrets.deta_name_ping
    deta_name_all = database_interface.Secrets.deta_name_all
    version_url = database_interface.Secrets.version_url
    if version_url:
        remote_version = processor.get_github_version(version_url)
    else:
        print(f"No version url found. All defaults are set to NO UPDATES")

    mining = database_interface.Database(
        machine_name, deta_name_mining, wallet)
    datalake = database_interface.Database(machine_name, deta_name_all, wallet)
    ping = database_interface.Database(machine_name, deta_name_ping)
    current_version = systemworks.get_version()
    print("Taking a sampleo of current CPU utilization (4 sec)")
    cpu_percent = psutil.cpu_percent(4)
    wallet_version = "WALLET" if wallet else ""
    print(f"Launching v. {current_version} {wallet_version}")

    while True:
        logging.info(f"Loop start")
        if remote_version["version"] != current_version:
            if remote_version["emergency"]:
                logging.info(
                    f'Remote version {remote_version["version"]}, exit 0')
                sys.exit(0)
            if remote_version["update"]:
                logging.info(
                    f'Remote version {remote_version["version"]}, exit 1')
                sys.exit(1)

        current_data = processor.get_data(PRC_USER, PRC_PASS)
        logging.info(f"Current data: {current_data}")

        current_balance = current_data.get("total_balance", 0)
        if int(current_balance) != int(process_data.old.total_balance):
            process_data.update(current_data)
            print(
                f"{process_data.machine} balance updated by {process_data.update_amount} to {process_data.total_balance} {humanize.naturaldelta(process_data.update_period)} ago at {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}. CPU {cpu_percent}%. Ver. {current_version} {wallet_version}"
            )
            if wallet:
                mining.update(process_data)
                datalake.add(process_data)
        else:
            cpu_percent = psutil.cpu_percent(10)
            process_data.ping(current_data.get(
                "current_height", 0), cpu_percent)
            ping.ping(process_data)
            logging.info(f"Pinging: {current_data}")
            # time.sleep(10)


if __name__ == "__main__":
    run()
