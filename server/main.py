import tornado.ioloop
import tornado.web
import pymongo
import time, datetime
from dateutil.relativedelta import *
import json

settings = {}
settings['MONGODB_DBNAME'] = 'idc?replicaSet=bidong_nodes'
settings['MONGODB_USER'] = 'mp'
settings['MONGODB_PASSWORD'] = 'mp_LYH_001*'
settings['MONGODB_IP'] = '14.23.62.180:27517,14.23.62.181:27517'

url = "mongodb://{0}:{1}@{2}/{3}".format(
     settings['MONGODB_USER'], settings['MONGODB_PASSWORD'], settings['MONGODB_IP'], settings['MONGODB_DBNAME'])
conn = pymongo.MongoClient(url)
db = conn['idc']

servers = db['servers']
server_status = db['server_status']

class GetServersHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #   return the server

        result = []
        servers = db['servers']
        for server in servers.find():
            del server['_id']
            result.append(server)

        self.write(json.dumps(result))

class UpdateServerStatusHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # self.output()

        values = json.loads(self.request.body)
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip
        now = datetime.datetime.now()

        #   insert into server_status
        status = {}
        status['datetime'] = now
        status['name'] = values['name']
        status['ip_address'] = remote_ip
        status['mac_address'] = values['mac_address']
        status['cpu_usage'] = values['cpu_usage']
        status['mem_free'] = values['mem_free']
        status['mem_used'] = values['mem_used']
        status['mem_used_pct'] = values['mem_used_pct']
        status['disk_available'] = values['disk_available']
        status['disk_used'] = values['disk_used']
        status['disk_used_pct'] = values['disk_used_pct']
        status['disk_io_stat'] = values['disk_io_stat']
        status['network_stat'] = values['network_stat']

        server_status.insert_one(status)

        #   insert into server_info
        server= {}
        server['name'] = values['name']
        server['ip_address'] = remote_ip
        server['mac_address'] = values['mac_address']
        server['nprocs'] = values['nprocs']
        server['cpu_model_name'] = values['cpu_model_name']
        server['mem_total'] = values['mem_total']
        server['disk_capacity'] = values['disk_capacity']
        server['disk_list'] = values['disk_io_stat'].keys()
        server['interface_list'] = values['network_stat'].keys()
        server['lastest_active_time'] = now

        if servers.find_one({'mac_address': server['mac_address']}):
            servers.update({'mac_address': server['mac_address']}, {'$set': server})
        else:
            servers.insert_one(server)

        self.write("%s \r\n" % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.write("submit successfully.")

def GetLastAndNow(period):
    now, last = None, None

    if period == 'recentday':
        now = datetime.datetime.now()
        last = now + datetime.timedelta(days=-1)
    elif period == 'lastday':
        today = datetime.date.today()
        now = datetime.datetime(today.year, today.month, today.day)
        last = now + datetime.timedelta(days=-1)
    elif period == 'recentmonth':
        today = datetime.date.today()
        now = datetime.datetime(today.year, today.month, today.day)
        last = now + relativedelta(months=-1)

    return (last, now)

class GetCPUHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        ip = self.get_argument('ip', '::1')
        name = self.get_argument('name', 'cpu')
        period = self.get_argument('period', 'recentday')

        last, now = GetLastAndNow(period)

        print('getting cpu status...')
        print('ip : {0}'.format(ip))
        print ('name : {0}'.format(name))
        print('period : {0}'.format(period))
        print('last : {0}'.format(last))
        print('now : {0}'.format(now))
        print('')

        found = server_status.find({'ip_address': ip, 'datetime': {'$gt': last, '$lt': now}},
                                   {'datetime': 1, 'cpu_usage.{0}'.format(name): 1}).sort('datetime', pymongo.ASCENDING)
        result = []
        for f in found:
            # print(f)
            result.append({'datetime': str(f['datetime']), 'cpu_usage': f['cpu_usage'][name]})
        self.write(json.dumps(result))

class GetMemUsageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        ip = self.get_argument('ip', '::1')
        period = self.get_argument('period', 'recentday')

        last, now = GetLastAndNow(period)

        print('getting memory usage...')
        print('ip : {0}'.format(ip))
        print('period : {0}'.format(period))
        print('last : {0}'.format(last))
        print('now : {0}'.format(now))
        print('')

        found = server_status.find({'ip_address': ip, 'datetime': {'$gt': last, '$lt': now}},
                                   {'datetime': 1, 'mem_free': 1, 'mem_used': 1, 'mem_used_pct': 1})\
            .sort('datetime', pymongo.ASCENDING)
        result = []
        for f in found:
            # print(f)
            result.append({'datetime': str(f['datetime']), 'mem_free': f['mem_free'],
                           'mem_used': f['mem_used'], 'mem_used_pct': f['mem_used_pct']})
        self.write(json.dumps(result))

class GetDiskUsageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        ip = self.get_argument('ip', '::1')
        period = self.get_argument('period', 'recentday')

        last, now = GetLastAndNow(period)

        print('getting disk usage...')
        print('ip : {0}'.format(ip))
        print('period : {0}'.format(period))
        print('last : {0}'.format(last))
        print('now : {0}'.format(now))
        print('')

        found = server_status.find({'ip_address': ip, 'datetime': {'$gt': last, '$lt': now}},
                                   {'datetime': 1, 'disk_available': 1, 'disk_used': 1, 'disk_used_pct': 1})\
            .sort('datetime', pymongo.ASCENDING)
        result = []
        for f in found:
            # print(f)
            result.append({'datetime': str(f['datetime']), 'disk_available': f['disk_available'],
                           'disk_used': f['disk_used'], 'disk_used_pct': f['disk_used_pct']})
        self.write(json.dumps(result))

class GetDiskIOHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        ip = self.get_argument('ip', '::1')
        name = self.get_argument('name', '')
        period = self.get_argument('period', 'recentday')

        last, now = GetLastAndNow(period)

        print('getting disk IO status...')
        print('ip : {0}'.format(ip))
        print('name : {0}'.format(name))
        print('period : {0}'.format(period))
        print('last : {0}'.format(last))
        print('now : {0}'.format(now))
        print('')

        found = server_status.find({'ip_address': ip, 'datetime': {'$gt': last, '$lt': now}},
                                   {'datetime': 1, 'disk_io_stat.{0}'.format(name): 1})\
            .sort('datetime', pymongo.ASCENDING)
        result = []
        for f in found:
            # print(f)
            result.append({'datetime': str(f['datetime']), 'tps': f['disk_io_stat'][name]['tps'], 'kB_wrtn': f['disk_io_stat'][name]['kB_wrtn'],
                           'kB_wrtn/s': f['disk_io_stat'][name]['kB_wrtn/s'], 'kB_read': f['disk_io_stat'][name]['kB_read'],
                           'kB_read/s': f['disk_io_stat'][name]['kB_read/s']})
        self.write(json.dumps(result))

class GetNetworkIOHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        ip = self.get_argument('ip', '::1')
        name = self.get_argument('name', '')
        period = self.get_argument('period', 'recentday')

        last, now = GetLastAndNow(period)

        print('getting network IO status...')
        print('ip : {0}'.format(ip))
        print('name : {0}'.format(name))
        print('period : {0}'.format(period))
        print('last : {0}'.format(last))
        print('now : {0}'.format(now))
        print('')

        found = server_status.find({'ip_address': ip, 'datetime': {'$gt': last, '$lt': now}},
                                   {'datetime': 1, 'network_stat.{0}'.format(name): 1})\
            .sort('datetime', pymongo.ASCENDING)
        result = []
        for f in found:
            # print(f)
            result.append({'datetime': str(f['datetime']), 'tx_KBps': f['network_stat'][name]['tx_KBps'],
                           'tx_MB': f['network_stat'][name]['tx_MB'], 'rx_KBps': f['network_stat'][name]['rx_KBps'],
                           'rx_MB': f['network_stat'][name]['rx_MB']})
        self.write(json.dumps(result))

def make_app():
    return tornado.web.Application([
        (r"/servers/status", UpdateServerStatusHandler),
        (r"/servers/cpus", GetCPUHandler),
        (r"/servers/mem_usage", GetMemUsageHandler),
        (r"/servers/disk_usage", GetDiskUsageHandler),
        (r"/servers/disk_io", GetDiskIOHandler),
        (r"/servers/network_io", GetNetworkIOHandler),
        (r"/servers", GetServersHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()