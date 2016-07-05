from __future__ import print_function
from collections import OrderedDict

def cpuinfo():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    CPU_info['proc0']={...}
    CPU_info['proc1']={...}
    '''
    cpuInfo = OrderedDict()
    procInfo = OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuInfo['proc%s' % nprocs] = procInfo
                nprocs = nprocs + 1
                # Reset
                procInfo = OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procInfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procInfo[line.split(':')[0].strip()] = ''

    cpuInfo['nprocs'] = nprocs
    return cpuInfo

def output():
    info = cpuinfo()
    print("{0} processors.".format(info['nprocs']))
    key, value = info.popitem(0)
    print(value['model name'])
    print()

if __name__ == '__main__':
    output()