# -*- encoding: utf-8 -*-
import httplib
import json
import logging
import traceback

import tornado.web

from common.WebError import WebError
from utils.JsonEncoder import JsonEncoder


class BaseHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		super(BaseHandler, self).__init__(application, request, **kwargs)

	def set_default_headers(self):
		self.set_header('Server', 'WEB-Server')

	def response_json(self, data):
		self.set_header('Content-Type', 'application/json; charset=utf-8')
		self.write(json.dumps(data, cls=JsonEncoder, sort_keys=False))
		self.write('\n')

	def write_error(self, status_code, **kwargs):
		logging.error(u'Error Request Url: ' + unicode(self.request.path))
		logging.error(u'Error Request Body: ' + unicode(self.request.body if self.request.body else ''))
		data = {'error': status_code, 'message': httplib.responses[status_code]}

		for item in kwargs['exc_info']:
			if isinstance(item, WebError):
				self.set_status(550 + int(item.code) if int(item.code) < 50 else int(item.code), item.message)
				data['error'] = item.code
				data['message'] = item.message
			elif isinstance(item, tornado.web.HTTPError):
				data['message'] = item.log_message
			elif isinstance(item, Exception):
				data['message'] = str(item)

		self.response_json(data)
