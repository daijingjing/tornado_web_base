#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging

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

	template_loader = JinjaLoader('./template/')
	settings = {
		"template_loader": template_loader,
		"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
		"xsrf_cookies": True,
	}
	app = web.Application(urls, **settings)
	app.listen(8888)
	ioloop.IOLoop.instance().start()


if __name__ == '__main__':
	main()
