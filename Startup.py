#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging

from os import path
from tornado import ioloop, httpserver, web
from tornado.options import options

from urls import urls
from common.JinjaTornado import JinjaLoader


def config_shutdown():
	def shutdown():
		import time
		global webserver_instance
		webserver_instance.stop()

		deadline = time.time() + 5

		io_loop = ioloop.IOLoop.instance()

		def stop_loop():
			import os
			now = time.time()
			if now < deadline and (io_loop._callbacks or io_loop._timeouts):
				io_loop.add_timeout(now + 1, stop_loop)
			else:
				io_loop.stop()
				logging.warning('Server shutdown! PID=%d' % (os.getpid()))

		stop_loop()

	def sig_handler(sig, frame):
		logging.warning("Shutdown... (%d)!" % sig)
		ioloop.IOLoop.instance().add_callback(shutdown)

	import signal
	signal.signal(signal.SIGTERM, sig_handler)
	signal.signal(signal.SIGINT, sig_handler)


def main():
	import os

	logging.basicConfig(  # filename = os.path.join(os.getcwd(), 'server.log'),
		level=logging.INFO,
		filemode='a',
		datefmt='%Y-%m-%d %H:%M:%S',
		format='[%(asctime)s] %(levelname)s: %(message)s')

	settings = {
		"static_path": options.static_path,
		"template_loader": JinjaLoader(options.template_path),
		"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
		"xsrf_cookies": True,
	}

	logging.warning("Server startup on %s:%d PID=%d ..." % (options.ip, options.port, os.getpid()))
	global webserver_instance
	webserver_instance = httpserver.HTTPServer(web.Application(urls, **settings))
	webserver_instance.bind(options.port, options.ip)
	webserver_instance.start(num_processes=options.num_processes)

	config_shutdown()
	ioloop.IOLoop.instance().start()


def parse_command():
	options.define("ip", type=str, default='127.0.0.1')
	options.define("port", type=int, default=8888)
	options.define("num_processes", type=int, default=0)

	options.define("template_path", type=str, default=path.join(path.dirname(__file__), "templates"))
	options.define("static_path", type=str, default=path.join(path.dirname(__file__), "static"))

	from tornado.options import parse_command_line
	parse_command_line()


if __name__ == '__main__':
	parse_command()
	main()
