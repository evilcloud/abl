import subprocess


def run(cluster):
    subprocess.call(['pip3', 'install', 'deta'])
    subprocess.call(['pip3', 'install', 'humanize'])
    import abel
    ret = abel.run(not cluster)
    return ret
