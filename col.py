import abel
import subprocess


def run(cluster):
    ret = abel.run(not cluster)
    return ret
