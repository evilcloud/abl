import os
import time
import redis_func
import sys
import subprocess


def force_import():
    try:
        subprocess.call(['pip3', 'install', 'redis'])
        import redis
        if "redis" in sys.modules:
            return True
    except ImportError:
        print("Redis module not installed")
    return False


def force_import():
    for attempt in range(3):
        try:
            import redis_func
            redis_module = True
            return True
        except ImportError:
            try:
                subprocess.call(['pip3', 'install', 'redis'])
                import redis_func
            except subprocess.CalledProcessError:
                print("Redis module not installed")
                redis_module = False
    return False


def connect():
    if not "redis" in sys.modules:
        print("Redis module not imported")
        ir = force_import()
        if not ir:
            return False
    redis_pass = os.environ.get("REDIS", None)
    redis_host = os.environ.get("REDIS_HOST", None)
    redis_port = os.environ.get("REDIS_PORT", None)
    if redis_pass and redis_host and redis_port:
        print("Redis validators positive. Connecting to Redis")
        for attempt in range(3):
            print(f"Connecting to Redis. Attempt {attempt +1}")
            try:
                redis_client = redis_func.Redis(host=redis_host,
                                                port=redis_port, password=redis_pass)
                print("Redis connected successfully")
                break
            except Exception:
                time.sleep(2)
                print("Redis connect failed")
    return redis_client
