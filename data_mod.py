from datetime import datetime, timedelta

# This is the largest nuber that Timestamp can be and thus is the basis for the reverse counting
# for the everincreasing key number for the DB
BIG_NUMBER = 9999999999


class Abecldata:
    def __init__(self, machine, wallet=False):
        self.old_data = {}
        self.new_data = {}
        self.changed = False
        self.machine = machine
        self.wallet = wallet
        self.key = 0

    def update(self, data):
        # Deal with that weird Go datetime format later. For now, just use the current time.
        current_time = datetime.utcnow()

        # The reverse timestamp as the key will help to display entries in consequitive order in Deta
        data["key"] = str(BIG_NUMBER - int(datetime.timestamp(current_time)))
        self.key = str(BIG_NUMBER - int(datetime.timestamp(current_time)))
        self.timestamp = int(datetime.timestamp(current_time))
        # We assidn the data to the new_data to be able to work with it later
        self.new_data = data

        # Checking if the balance has changed, in which case the self.changes switch goes ON
        # In other case we are switching the switch OFF
        old_balance = self.old_data.get("total_balance", None)
        new_balance = self.new_data.get("total_balance", None)
        if old_balance != new_balance:
            self.old_data = self.new_data
            self.changed = True
        else:
            self.changed = False

        # And we finally make our new data old
        self.old_data = self.new_data

    def machine_total(self):
        return {self.machine: self.new_data["total_balance"]}


class Cycle:
    def __init__(self):  # sourcery skip: aware-datetime-for-utc
        self.total: int = 0
        self.successes: int = 0
        self.new_ping: int = 0
        self.app_start_time: datetime = datetime.utcnow()
        self.last_sucess_time: datetime = self.app_start_time
        self.time_since_app_start: timedelta
        self.time_since_last_sucess: timedelta

    def update(self):  # sourcery skip: aware-datetime-for-utc
        self.time_now = datetime.utcnow()
        # Cycle.common()
        self.total += 1
        self.time_since_app_start = self.time_now - self.app_start_time
        self.time_since_last_sucess = self.time_now - self.last_sucess_time

    def success(self):  # sourcery skip: aware-datetime-for-utc
        self.time_now = datetime.utcnow()
        # Cycle.common()
        self.successes += 1
        self.last_sucess_time = self.time_now
        self.ping = self.new_ping
        self.new_ping = 0

    def pinging(self):
        self.new_ping += 1
