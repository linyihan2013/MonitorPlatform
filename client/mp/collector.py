from __future__ import print_function
from collections import OrderedDict
import cpu1, cpu2, disk, interface, mem
import time
import urllib, urllib2
import uuid
import socket
import json

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def output():
    '''
    Print the total information.
    '''
    print("hello test service %s \r\n" % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    cpu1.output()
    cpu2.output()
    mem.output()
    disk.output()
    interface.output()

def submit():
    '''
    Submit the data to the server.
    '''
    cpuInfo = cpu1.cpuinfo()
    key, value = cpuInfo.popitem(0)
    cpuUsage = cpu2.get_cpu_usage()
    memInfo = mem.meminfo()
    diskUsage = disk.disk_usage()
    diskIoStat = disk.disk_iostat()
    networkStat = interface.get_network_stat()

    values = {'name': socket.getfqdn(socket.gethostname()),
              'mac_address': get_mac_address(),
              'nprocs': cpuInfo['nprocs'],
              'cpu_model_name': value['model name'],
              'cpu_usage': cpuUsage,
              'mem_total': memInfo['MemTotal'],
              'mem_free': memInfo['MemFree'],
              'mem_used_pct': memInfo['MemUsedPct'],
              'disk_capacity': diskUsage['capacity'],
              'disk_available': diskUsage['available'],
              'disk_used': diskUsage['used'],
              'disk_used_pct': diskUsage['usedPct'],
              'disk_io_stat': diskIoStat,
              'network_stat': networkStat
              }

    data = json.dumps(values)
    url = "http://172.16.17.34:8888/servers/status"

    req = urllib2.Request(url, data)
    res = urllib2.urlopen(req)
    content = res.read().decode()
    print(content)
    print()

if __name__ == '__main__':
    submit()