import abel
import subprocess


subprocess.call(['pip', 'install', 'humanize'])
subprocess.call(['pip', 'install', 'deta'])
subprocess.call(['pip', 'install', 'redis'])


def run(cluster):
    ret = abel.run(not cluster)
    return ret
