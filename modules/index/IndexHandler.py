#!/usr/bin/env python
from common.BaseHandler import BaseHandler


class IndexHandler(BaseHandler):
	def get(self):
		self.render('index/test.html')
