import tornado.ioloop
import tornado.web
import time
import json
from collections import OrderedDict

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class MonitorServerHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("server monitoring.")

    def post(self, *args, **kwargs):
        values = json.loads(self.request.body)
        cpuUsage = values['cpu_usage']
        cpus = sorted(cpuUsage.keys())

        f = open('log.txt', 'w')
        f.write("{0} \r\n".format(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))))
        f.write('name : {0}\n'.format(values['name']))
        f.write('mac_address : {0}\n'.format(values['mac_address']))
        f.write('nprocs : {0}\n'.format(values['nprocs']))
        f.write('cpu_model_name : {0}\n'.format(values['cpu_model_name']))

        f.write('cpu_usage : \n')
        for cpu in cpus:
            f.write('   {0} : {1} %\n'.format(cpu, cpuUsage[cpu]))
        f.write('\n')

        f.write('mem_total : {0}\n'.format(values['mem_total']))
        f.write('mem_free : {0}\n'.format(values['mem_free']))
        f.write('mem_used_pct : {0} %\n'.format(values['mem_used_pct']))

        f.write('disk_capacity : {0}\n'.format(values['disk_capacity']))
        f.write('disk_available : {0}\n'.format(values['disk_available']))
        f.write('disk_used : {0}\n'.format(values['disk_used']))
        f.write('disk_used_pct : {0} %\n'.format(values['disk_used_pct']))

        f.write('disk io status : \n')
        for dev in values['disk_io_stat'].keys():
            f.write('device {0} :\n'.format(dev))
            stats = values['disk_io_stat'][dev]
            f.write('   tps : {0}\n'.format(stats['tps']))
            f.write('   kB_read/s : {0}\n'.format(stats['kB_read/s']))
            f.write('   kB_wrtn/s : {0}\n'.format(stats['kB_wrtn/s']))
            f.write('   kB_read : {0}\n'.format(stats['kB_read']))
            f.write('   kB_wrtn : {0}\n'.format(stats['kB_wrtn']))
            f.write('\n')

        f.write('network status : \n')
        for interface in values['network_stat'].keys():
            f.write('interface {0} : \n'.format(interface))
            stats = values['network_stat'][interface]
            f.write('   {0} MB received\n'.format(stats['rx_MB']))
            f.write('   {0} MB sent\n'.format(stats['tx_MB']))
            f.write('   {0} KB/s received\n'.format(stats['rx_KBps']))
            f.write('   {0} KB/s sent\n'.format(stats['tx_KBps']))
            f.write('\n')

        f.close()

        self.write("%s \r\n" % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.write("submit successfully.")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/monitor/server", MonitorServerHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()