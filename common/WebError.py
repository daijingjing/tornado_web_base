# -*- encoding: utf-8 -*-


class WebError(Exception):
	def __init__(self, code, message=''):
		Exception.__init__(self)
		self.code = code
		self.message = message

	def __str__(self):
		return self.message
