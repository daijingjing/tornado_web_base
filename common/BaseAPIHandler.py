# -*- encoding: utf-8 -*-
import httplib
import json
import logging
import traceback

import tornado.web

from common.BaseHandler import BaseHandler
from common.WebError import WebError
from utils.JsonEncoder import JsonEncoder


class BaseAPIHandler(BaseHandler):
	def __init__(self, application, request, **kwargs):
		super(BaseAPIHandler, self).__init__(application, request, **kwargs)

	def has_params(self, data, params, isRaise=True):
		if not isinstance(data, dict):
			if isRaise:
				raise WebError(500, '调用参数错误，缺少参数')
			else:
				return False

		if isinstance(params, str):
			if isRaise and not data.has_key(params):
				raise WebError(500, '调用参数错误，缺少参数[%s]' % str(params))
			else:
				return data.has_key(params)

		elif isinstance(params, tuple) or isinstance(params, list):
			for p in params:
				if not data.has_key(str(p)):
					if isRaise:
						raise WebError(500, '调用参数错误，缺少参数[%s]' % str(p))
					else:
						return False

		return True

	def post(self, p):
		if not p:
			raise WebError(404)

		params = str(p).split('/') if p else []
		attr = getattr(self, params[0], None)

		if attr:

			if 'Content-Type' in self.request.headers and 'application/json' in self.request.headers['Content-Type']:
				data = None
				try:
					data = json.loads(self.request.body.decode('utf-8'))

				except:
					logging.error("解析JSON数据错误(Content: %s)" % (str(self.request.body)))
					raise WebError(500, '解析JSON数据错误')

				try:
					attr(params[1:], data)

				except WebError, e:
					traceback.print_exc()
					logging.error(
						"服务器内部功能调用错误(URI: %s, Error: %s, Content: %s)" % (str(p), str(e), str(self.request.body)))
					raise

				except BaseException, e:
					traceback.print_exc()
					logging.error(
						"服务器内部功能调用错误(URI: %s, Error: %s, Content: %s)" % (str(p), str(e), str(self.request.body)))
					raise WebError(500, '服务器内部错误')

			else:
				logging.error("数据格式不支持(Content-Type: %s)" % (str(self.request.headers.get('Content-Type', None))))
				raise WebError(500, '数据格式不支持')
		else:
			logging.error("功能方法不存在(%s)" % (str(p)))
			raise WebError(404, '功能方法不存在')

	def get(self, p):
		if not p:
			logging.error("功能调用错误，未提供调用方法")
			raise tornado.web.HTTPError(404, "功能调用错误，未提供调用方法")

		params = str(p).split('/') if p else []
		attr = getattr(self, params[0], None) if params[0].startswith('get_') else None

		if attr:
			try:
				args = {}
				for k in self.request.arguments.keys():
					args[k] = self.get_argument(k)
				attr(params[1:], args)

			except WebError, e:
				traceback.print_exc()
				logging.error(
					"服务器内部功能调用错误(URI: %s, Error: %s, Content: %s)" % (str(p), str(e.message), str(self.request.body)))
				raise

			except tornado.web.HTTPError, e:
				traceback.print_exc()
				logging.error("服务器内部功能调用错误(URI: %s, Error: %s, Content: %s)" % (str(p), str(e), str(self.request.body)))
				raise

			except BaseException, e:
				traceback.print_exc()
				logging.error("服务器内部功能调用错误(URI: %s, Error: %s, Content: %s)" % (str(p), str(e), str(self.request.body)))
				raise WebError(500, '服务器内部错误')

		else:
			logging.error("功能方法不存在(%s)" % (str(p)))
			raise tornado.web.HTTPError(404, "功能方法不存在(%s)" % (str(p)))
