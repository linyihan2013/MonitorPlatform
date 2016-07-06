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
        cpustr2 = cpuInfo2[key]

        if len(cpustr1) >= 7 and len(cpustr2) >= 7:

            totalCPUTime1 = long(cpustr1[1]) + long(cpustr1[2]) + long(cpustr1[3]) + long(cpustr1[4]) + long(cpustr1[5]) + long(cpustr1[6]) + long(
                cpustr1[7])
            usedCPUTime1 = long(cpustr1[1]) + long(cpustr1[2]) + long(cpustr1[3])

            totalCPUTime2 = float(cpustr2[1]) + long(cpustr2[2]) + long(cpustr2[3]) + long(cpustr2[4]) + long(cpustr2[5]) + long(cpustr2[6]) + long(
                cpustr2[7])
            usedCPUTime2 = float(cpustr2[1]) + long(cpustr2[2]) + long(cpustr2[3])

            cpuPct = round((usedCPUTime2 - usedCPUTime1) * 100 / (totalCPUTime2 - totalCPUTime1), 2)
            cpuUsage[key] = cpuPct

    return cpuUsage

def output():
    cpuUsage = get_cpu_usage()
    for cpu in cpuUsage.keys():
        print('The used percentage of {0} is : {1} %'.format(cpu, cpuUsage[cpu]))
    print()

if __name__ == '__main__':
    output()