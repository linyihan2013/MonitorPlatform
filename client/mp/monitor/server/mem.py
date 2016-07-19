from __future__ import print_function
from collections import OrderedDict

def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    memInfo = OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            memInfo[line.split(':')[0]] = line.split(':')[1].strip()

    if 'MemTotal' in memInfo.keys() and 'MemFree' in memInfo.keys():
        memInfo['MemTotal'] = round(long(memInfo['MemTotal'].split(' ')[0]) / 1024.0, 2)
        memInfo['MemFree'] = round(long(memInfo['MemFree'].split(' ')[0]) / 1024.0, 2)
        memInfo['MemUsed'] = memInfo['MemTotal'] - memInfo['MemFree']
        memInfo['MemUsedPct'] = round(memInfo['MemUsed'] * 100.0 / memInfo['MemTotal'], 2)

    return memInfo

def output():
    memInfo = meminfo()
    print('Total memory: {0} MB'.format(memInfo['MemTotal']))
    print('Free memory: {0} MB'.format(memInfo['MemFree']))
    print('Used memory percentage: {0} %'.format(memInfo['MemUsedPct']))
    print()

if __name__ == '__main__':
    output()