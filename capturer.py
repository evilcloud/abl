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
db_machine = db_deta.Detadb(DETA_KEY, machine)
db_totals = db_deta.Detadb(DETA_KEY, "_totals")
prnt = se_term.Printdata(machine, wallet)

while True:
    cycle.update()

    data = abectl.get_data(RPC_USER, RPC_PASS)
    obj.update(data)
    if obj.changed:
        cycle.success()

        db_machine.put(obj.new_data)
        db_totals.put(obj.machine_total())
        prnt.changes(obj.new_data)
    else:
        cycle.pinging()

        prnt.no_changes(obj.new_data, cycle)
        time.sleep(1)
