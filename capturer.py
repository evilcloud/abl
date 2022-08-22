import se_term
import time
import data_mod
import se_system
import abectl
import db_deta


envs = se_system.get_envs()
DETA_KEY = envs["DETA_KEY"]
RPC_USER = envs["RPC_USER"]
RPC_PASS = envs["RPC_PASS"]

machine = se_system.get_machine_name()
wallet = se_system.is_wallet()

obj = data_mod.Abecldata(machine, wallet)
cycle = data_mod.Cycle()
db = db_deta.Detadb(DETA_KEY, machine)
prnt = se_term.Printdata(machine, wallet)

while True:
    cycle.update()

    data = abectl.get_data(RPC_USER, RPC_PASS)
    obj.update(data)
    if obj.changed:
        cycle.success()

        db.put(obj.new_data)
        # se_term.print_changes(obj.new_data)
        prnt.changes(obj.new_data)
    else:
        cycle.pinging()

        # se_term.print_ping(cycle, obj.new_data)
        prnt.no_changes(obj.new_data, cycle)
        time.sleep(1)
