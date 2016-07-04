from __future__ import print_function
from collections import OrderedDict
import os

def disk_usage():
    '''
    Return the information about the disk
    '''
    hd={}
    disk = os.statvfs("/")
    hd['available'] = round(disk.f_bsize * disk.f_bavail / (1024.0 * 1024), 2)
    hd['capacity'] = round(disk.f_bsize * disk.f_blocks / (1024.0 * 1024), 2)
    hd['used'] = hd['capacity'] - hd['available']
    hd['usedPct'] = round(hd['used'] * 100.0 / hd['capacity'], 2)
    return hd

def disk_iostat():
    '''
    Return the io status of disk.
    '''
    diskInfo = OrderedDict()

    f = os.popen('iostat -d -k').readlines()
    if len(f) >= 4 and f[2].startswith('Device:'):
        f = f[3:]
        for line in f:
            data = line.strip().split()
            if len(data) == 6:
                devInfo = OrderedDict()

                devInfo['tps'] = float(data[1])
                devInfo['kB_read/s'] = float(data[2])
                devInfo['kB_wrtn/s'] = float(data[3])
                devInfo['kB_read'] = long(data[4])
                devInfo['kB_wrtn'] = long(data[5])

                diskInfo[data[0]] = devInfo

    return diskInfo

if __name__ == '__main__':
    du = disk_usage()
    print('The capacity space of disk is: {0} MB'.format(du['capacity']))
    print('The available space of disk is: {0} MB'.format(du['available']))
    print('The used percentage of disk is: {0} %'.format(du['usedPct']))
    print()

    di = disk_iostat()
    for dev in di.keys():
        print('Device {0} :'.format(dev))
        print('tps : {0}'.format(di[dev]['tps']))
        print('kB_read/s : {0}'.format(di[dev]['kB_read/s']))
        print('kB_wrtn/s : {0}'.format(di[dev]['kB_wrtn/s']))
        print('kB_read : {0}'.format(di[dev]['kB_read']))
        print('kB_wrtn : {0}'.format(di[dev]['kB_wrtn']))
        print()