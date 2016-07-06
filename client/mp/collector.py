from __future__ import print_function
import time
import cpu1, cpu2, disk, interface, mem
import urllib
import uuid
import socket

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

    values = {'nprocs': cpuInfo['nprocs'],
              'cpu_model_name': value['model name'],
              'cpu_usage': {cpu: cpuUsage[cpu] for cpu in cpuUsage.keys()},
              'mem_total': memInfo['MemTotal'],
              'mem_free': memInfo['MemFree'],
              'mem_used_pct': memInfo['MemUsedPct'],
              'disk_available': diskUsage['available'],
              'disk_capacity': diskUsage['capacity'],
              'disk_used': diskUsage['used'],
              'disk_used_pct': diskUsage['usedPct'],
              'disk_io_stat': diskIoStat,
              'network_stat': networkStat,
              'mac_address': get_mac_address(),
              'name': socket.getfqdn(socket.gethostname())
              }

    data = urllib.urlencode(values)

    url = "http://localhost:8888/monitor/server"

    res = urllib.urlopen(url, data)
    content = res.read().decode()
    print(content)

if __name__ == '__main__':
    submit()