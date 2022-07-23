import sys
import subprocess
from deta import Deta
from datetime import datetime

if "deta" not in sys.modules:
    print("Force-installing deta module")
    subprocess.call(["pip3", "install", "deta"])
    from deta import Deta

    if "deta" not in sys.modules:
        print("Missing deta module. Exiting...")
        sys.exit(1)
    print("Deta module installed successfully. Continuing...")


class Detadb:
    def __init__(self, DETA, DETA_DB_NAME, machine):
        deta = Deta(DETA)
        self.db = deta.Base(DETA_DB_NAME)
        db_entries = self.db.fetch()
        db_entries_count = db_entries.count
        if db_entries_count:
            print(f"Database already exists with {db_entries_count} entries...")
        else:
            print(f"Database {DETA_DB_NAME} does not exist. Creating...")

    def update(self, entry):
        self.db.put(entry)

    def ping(self, data):
        self.db.put(data)
