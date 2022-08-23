import humanize
from datetime import datetime, timezone

DATE_TIME_LENGHT_STR = 19


class Printdata:
    def __init__(self, machine, wallet=False):
        self.machine = machine
        self.wallet = "W" if wallet else ""
        self.printed = {
            "current_time": None,
            "total_balance": None,
            "current_height": None,
        }

    def changes(self, data):
        printed = self.printed
        for key, value in data.items():
            if key in printed:
                printed[key] = value

        print()
        print(
            f'{printed["current_time"][:DATE_TIME_LENGHT_STR]} Blocks: {printed["current_height"]}  Total: {printed["total_balance"]} Machine: {self.machine} {self.wallet}'
        )
        print()

    def no_changes(self, data, cycle):
        current_height = data.get("current_height", None)
        block = f"BLOCK: {current_height}." if current_height else ""
        print(
            f"\r{datetime.utcnow().replace(microsecond=0, tzinfo=None)}. {block} Since START: {cycle.total}, LAST SUCCESS: {cycle.new_ping} | {humanize.naturaldelta(cycle.time_since_last_sucess)}",
            end=" ",
        )


def print_changes(data):
    printed = {
        "current_time": None,
        "total_balance": None,
        "machine": None,
        "wallet": None,
        "current_height": None,
    }
    for key, value in data.items():
        if key in printed:
            printed[key] = value

    wallet = "W" if printed["wallet"] else ""

    # time_since_last_sucess = (
    #     humanize.naturaldelta(cycle.time_since_last_sucess)
    #     if cycle.time_since_last_sucess
    #     else "?"
    # )

    # time_since_app_start = (
    #     humanize.naturaldelta(cycle.time_since_app_start)
    #     if cycle.time_since_app_start
    #     else "?"
    # )
    print()
    print(
        f'{printed["current_time"][:DATE_TIME_LENGHT_STR]} Blocks: {printed["current_height"]}  Total: {printed["total_balance"]} Machine: {printed["machine"]} {wallet}'
    )
    print()


def print_ping(cycle, data):  # sourcery skip: aware-datetime-for-utc
    block = f"BLOCK: {data['current_height']}." if data["current_height"] else ""
    print(
        f"\r{datetime.utcnow().replace(microsecond=0, tzinfo=None)}. {block} Since START: {cycle.total}, LAST SUCESS: {cycle.new_ping} | {humanize.naturaldelta(cycle.time_since_last_sucess)}",
        end=" ",
    )
