from __future__ import print_function
from collections import OrderedDict
import time

def read_network_stat():
    ''' Return the information in /proc/net/dev
        as a dictionary.
    '''
    netStat = OrderedDict()

    with open('/proc/net/dev') as f:
        for line in f:
            if len(line.split(':')) == 2:
                ifstat = OrderedDict()

                interface = line.split(':')[0]
                data = line.split(':')[1].split()

                if len(data) >= 9:
                    ifstat['rx_bytes'], ifstat['tx_bytes'] = (data[0], data[8])
                else:
                    ifstat['rx_bytes'], ifstat['tx_bytes'] = (0, 0)
                netStat[interface] = ifstat

    return netStat


def get_network_stat():
    """
        get interface network speed.
    """
    netStat1 = read_network_stat()
    if not netStat1:
        return None

    wait_time = 2
    time.sleep(wait_time)

    netStat2 = read_network_stat()
    if not netStat2:
        return None

    result = {}

    for key in netStat2.keys():
        stat = {}
        stat['rx_KBps'] = round((long(netStat2[key]['rx_bytes']) - long(netStat1[key]['rx_bytes'])) / (1024.0 * wait_time), 2)
        stat['tx_KBps'] = round((long(netStat2[key]['tx_bytes']) - long(netStat1[key]['tx_bytes'])) /  (1024.0 * wait_time), 2)
        stat['rx_MB'] = round(long(netStat2[key]['rx_bytes']) / (1024.0 * 1024), 2)
        stat['tx_MB'] = round(long(netStat2[key]['tx_bytes']) / (1024.0 * 1024), 2)

        result[key] = stat

    return result

def output():
    netStat = get_network_stat()
    for interface in netStat.keys():
        print('interface %s : ' % interface)
        print('{0} MB received'.format(netStat[interface]['rx_MB']))
        print('{0} MB sent'.format(netStat[interface]['tx_MB']))
        print('{0} KB/s received'.format(netStat[interface]['rx_KBps']))
        print('{0} KB/s sent'.format(netStat[interface]['tx_KBps']))
        print()

if __name__ == '__main__':
    output()