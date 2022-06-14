import time
def epochTimeToHumanReadable(epoch: str):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(epoch)))