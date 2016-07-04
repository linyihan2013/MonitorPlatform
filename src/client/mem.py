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
        memInfo['MemTotal'] = long(memInfo['MemTotal'].split(' ')[0]) / 1024
        memInfo['MemFree'] = long(memInfo['MemFree'].split(' ')[0]) / 1024
        memInfo['Buffers'] = long(memInfo['Buffers'].split(' ')[0]) / 1024
        memInfo['Cached'] = long(memInfo['Cached'].split(' ')[0]) / 1024
        usedMemory = memInfo['MemTotal'] - memInfo['MemFree']
        memInfo['MemUsedPct'] = round(usedMemory * 100.0 / memInfo['MemTotal'], 3)

    return memInfo

if __name__ == '__main__':
    info = meminfo()
    print('Total memory: {0} MB'.format(info['MemTotal']))
    print('Free memory: {0} MB'.format(info['MemFree']))
    print('Used memory percentage: {0} %'.format(info['MemUsedPct']))