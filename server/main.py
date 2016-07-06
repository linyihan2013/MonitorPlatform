import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ServerHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("server monitoring.")

    def post(self, *args, **kwargs):
        self.write("server monitoring.")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/monitor/server", ServerHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()