import abel
import subprocess


subprocess.call(['pip3', 'install', 'humanize'])
subprocess.call(['pip3', 'install', 'deta'])
subprocess.call(['pip3', 'install', 'redis'])


def run(cluster):
    ret = abel.run(not cluster)
    return ret
