#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging

from os import path
from tornado import ioloop
from tornado import web

from urls import urls
from common.JinjaTornado import JinjaLoader


def main():
	logging.basicConfig(  # filename = os.path.join(os.getcwd(), 'server.log'),
		level=logging.INFO,
		filemode='a',
		datefmt='%Y-%m-%d %H:%M:%S',
		format='[%(asctime)s] %(levelname)s: %(message)s')

	settings = {
		"static_path": path.join(path.dirname(__file__), "static"),
		"template_loader": JinjaLoader(path.join(path.dirname(__file__), "templates")),
		"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
		"xsrf_cookies": True,
	}
	app = web.Application(urls, **settings)
	app.listen(8888)
	ioloop.IOLoop.instance().start()


if __name__ == '__main__':
	main()
