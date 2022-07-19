import os
import time
import pymongo
import sys
import subprocess


def force_import():
    try:
        subprocess.call(['pip3', 'install', 'pymongo[srv]'])
        import pymongo
        if "pymongo" in sys.modules:
            return True
    except ImportError:
        print("Mongo module not installed")

    return False


def connect():
    if not "pymongo" in sys.modules:
        print("Mongo module not imported. Attempting to force-import.")
        f = force_import()
        if not f:
            return False
    mongo_uri = os.environ.get("MONGO", None)
    if mongo_uri:
        print("Mongo validators positive. Connecting to MongoDB")
        for attempt in range(3):
            print(f"Connecting to MongoDB. Attempt {attempt +1}")
            try:
                mongo_client = pymongo.MongoClient(mongo_uri)
                print("MongoDB connected successfully")
                return mongo_client
            except Exception:
                time.sleep(2)
    return False
