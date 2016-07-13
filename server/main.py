import tornado.ioloop
import tornado.web
import pymongo
import time, datetime
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

        #   insert into server_status
        status = {}
        status['datetime'] = datetime.datetime.utcnow()
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

        server_status = db['server_status']
        server_status.insert_one(values)

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

        servers = db['servers']
        if servers.find_one({'mac_address': server['mac_address']}):
            servers.update({'mac_address': server['mac_address']}, {'$set': server})
        else:
            servers.insert_one(server)

        self.write("%s \r\n" % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self.write("submit successfully.")

def make_app():
    return tornado.web.Application([
        (r"/servers/status", UpdateServerStatusHandler),
        (r"/servers", GetServersHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()