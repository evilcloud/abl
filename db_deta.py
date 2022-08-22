from deta import Deta


class Detadb:
    def __init__(self, DETA_KEY, machine_name):
        deta = Deta(DETA_KEY)
        self.db = deta.Base(machine_name)

    def put(self, data):
        self.db.put(data)
