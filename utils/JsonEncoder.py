# -*- encoding: utf-8 -*-
import json
from datetime import datetime, date
from decimal import Decimal


class JsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.isoformat()
		elif isinstance(obj, date):
			return obj.isoformat()
		elif isinstance(obj, Decimal):
			return str(obj)
		else:
			return json.JSONEncoder.default(self, obj)
