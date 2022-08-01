from dataclasses import dataclass
from platform import machine
import db_deta
import db_redis
import os


print("redis request")
r = db_redis.Redisdb()
DETA_KEY = os.environ.get('DETA', r.get("DETA"))


@dataclass
class Secrets:
    DETA_KEY = r.get("DETA")
    DETA_name_mining = os.environ.get(
        "DETA_NAME_MINING", r.get("DETA_name_mining"))
    DETA_name_ping = os.environ.get("DETA_NAME_PING", r.get("DETA_name_ping"))
    DETA_name_all = os.environ.get("DETA_NAME_ALL", r.get("DETA_name_all"))
    RPC_USER = os.environ.get("RPC_USER", r.get("RPC_USER"))
    RPC_PASS = os.environ.get("RPC_PASS", r.get("RPC_PASS"))
    version_url = os.environ.get("VERSION_URL", r.get("version_url"))


class Database:
    def __init__(self, machine, db_name, wallet=False):
        self.detadb = db_deta.Detadb(DETA_KEY, db_name, machine)

    def update(self, data):
        self.detadb.update(
            {
                "key": data.machine,
                "os": data.os,
                "balance": data.total_balance,
                "block": data.current_height,
                "programmatic": data.programmatic,
                "updatetime": data.update_time_str,
                "update amount": data.update_amount,
                "update period": data.update_period_str,
                "update block difference": data.update_block_diff,
                "version": data.version,
            }
        )

    def add(self, data):
        self.detadb.update(
            {
                "machine": data.machine,
                "os": data.os,
                "balance": data.total_balance,
                "block": data.current_height,
                "programmatic": data.programmatic,
                "updatetime": data.update_time_str,
                "update amount": data.update_amount,
                "update period": data.update_period_str,
                "update block difference": data.update_block_diff,
                "version": data.version,
            }
        )

    def ping(self, data):
        self.detadb.update(
            {
                "key": data.machine,
                "block": data.ping_block,
                "blocks since last": data.ping_delta_block,
                "time": data.ping_time_str,
                "since last award": data.ping_delta_time_str,
                "version": data.version,
            }
        )

    def fetch(self, key):
        self.value = self.detadb.get(key)
