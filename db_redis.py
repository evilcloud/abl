import sys
import subprocess
import redis
import os

REDIS = os.environ.get("REDIS", None)
REDIS_HOST = os.environ.get("REDIS_HOST", None)
REDIS_PORT = os.environ.get("REDIS_PORT", None)
if not REDIS or not REDIS_HOST or not REDIS_PORT:
    print("ERROR: REDIS environment variables not set")
    sys.exit(1)


if "redis" not in sys.modules:
    print("Force-installing redis module")
    subprocess.call(["pip3", "install", "redis"])
    import redis

    if "redis" not in sys.modules:
        print("Missing redis module. Exiting...")
        sys.exit(1)
    print("Redis module installed successfully. Continuing...")


class Redisdb:
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS)

    def get(self, key):
        print(key)
        key = self.r.get(key)
        return key.decode("utf-8")
