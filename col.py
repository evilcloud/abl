import abel


def run(cluster):
    ret = abel.run(not cluster)
    return ret
