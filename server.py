# -*- coding:utf-8 -*-
import os
import sys

import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options, parse_command_line

from application import app

define("port", default=10000, help="Server listening on the given ports", type=int)

def main():
    options.parse_command_line()
    print("HTTP Server running on {0} port ...".format(options.port))
    print("Stop the server, press Ctrl + C")
    httpServer = tornado.httpserver.HTTPServer(app)
    if sys.platform.startswith("linux"):
        httpServer.bind(options.port, reuse_port=True)
    else:
        httpServer.bind(options.port, reuse_port=False)
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
