import abel
import subprocess


def run(cluster):
    subprocess.call(['pip', 'install', 'humanize'])
    subprocess.call(['pip', 'install', 'deta'])
    subprocess.call(['pip', 'install', 'redis'])
    ret = abel.run(not cluster)
    return ret
