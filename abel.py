import time
import processor
import database_interface
import systemworks
import humanize
import datetime
import updater
import subprocess
import sys


def run(wallet):
    process_data = processor.Datadiff(wallet)
    machine_name = process_data.machine

    current_data = {}

    PRC_USER = database_interface.Secrets.RPC_USER
    PRC_PASS = database_interface.Secrets.RPC_PASS
    DETA_name_mining = database_interface.Secrets.DETA_name_mining
    DETA_name_ping = database_interface.Secrets.DETA_name_ping
    DETA_name_all = database_interface.Secrets.DETA_name_all
    mining = database_interface.Database(
        machine_name, DETA_name_mining, wallet)
    all = database_interface.Database(machine_name, DETA_name_all, wallet)
    ping = database_interface.Database(machine_name, DETA_name_ping)
    current_version = systemworks.get_version()
    wallet_version = "WALLET" if wallet else ""

    while True:
        # current_data = processor.get_data_2()
        version_url = database_interface.Secrets.version_url
        remote_version = updater.get_github_version(version_url)
        if remote_version["version"] != current_version:
            if remote_version["emergency"]:
                return "EMERGENCY"
            if remote_version["update"]:
                return "UPDATE"

        current_data = processor.get_data(PRC_USER, PRC_PASS)

        current_balance = current_data.get("total_balance", 0)
        if int(current_balance) != int(process_data.old.total_balance):
            process_data.update(current_data)
            mining.update(process_data)
            all.update(process_data)
            print(
                f"{process_data.machine} balance updated by {process_data.update_amount} to {process_data.total_balance} {humanize.naturaldelta(process_data.update_period)} ago at {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}. Ver. {current_version} {wallet_version}"
            )
        else:
            process_data.ping(current_data.get("current_height", 0))
            ping.ping(process_data)
            time.sleep(10)


if __name__ == "__main__":
    run(True)
