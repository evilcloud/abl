from deta import Deta


class Detadb:
    def __init__(self, DETA, DETA_DB_NAME, machine):
        deta = Deta(DETA)
        self.db = deta.Base(DETA_DB_NAME)
        db_entries = self.db.fetch()
        db_entries_count = db_entries.count
        if db_entries_count:
            print(
                f"Database already exists with {db_entries_count} entries...")
        else:
            print(f"Database {DETA_DB_NAME} does not exist. Creating...")

    def update(self, entry):
        try:
            self.db.put(entry)
        except Exception as e:
            print(f"\tError updating database\n", e)

    # Legacy method -- afraid to remove
    def ping(self, data):
        try:
            self.db.put(data)
        except Exception as e:
            print(f"\tError updating ping\n", e)

    def fetch(self, key):
        self.existing_entries = self.db.fetch(key)
