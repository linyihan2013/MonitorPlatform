from __future__ import print_function
import time
from collections import OrderedDict

def read_cpu_usage():
    """Read the current system cpu usage from /proc/stat."""
    cpuInfo = OrderedDict()

    with open('/proc/stat') as f:
        for line in f:
            l = line.split()
            if len(l) < 5:
                continue
            if l[0].startswith('cpu'):
                cpuInfo[l[0]] = l

    return cpuInfo

def get_cpu_usage():
    """ 
    get cpu avg used by percent 
    """
    cpuInfo1 = read_cpu_usage()
    if not cpuInfo1:
        return None

    time.sleep(2)

    cpuInfo2 = read_cpu_usage()
    if not cpuInfo2:
        return None

    cpuUsage = OrderedDict()

    for key in cpuInfo1.keys():
        cpustr1 = cpuInfo1[key]

        totalCPUTime1 = long(cpustr1[1]) + long(cpustr1[2]) + long(cpustr1[3]) + long(cpustr1[4]) + long(cpustr1[5]) + long(cpustr1[6]) + long(
            cpustr1[7])
        usedCPUTime1 = totalCPUTime1 - long(cpustr1[4])

        cpustr2 = cpuInfo2[key]

        totalCPUTime2 = float(cpustr2[1]) + long(cpustr2[2]) + long(cpustr2[3]) + long(cpustr2[4]) + long(cpustr2[5]) + long(cpustr2[6]) + long(
            cpustr2[7])
        usedCPUTime2 = totalCPUTime2 - long(cpustr2[4])

        cpuper = round((usedCPUTime2 - usedCPUTime1) * 100 / (totalCPUTime2 - totalCPUTime1), 3)
        cpuUsage[key] = cpuper
    return cpuUsage

if __name__ == '__main__':
    print(get_cpu_usage())