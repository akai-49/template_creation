import json

import frappe
from frappe import _


def ensure_json(value, label, default=None):
	"""Return `value` as a JSON string, throwing a readable error if it can't be parsed.

	Used by every controller that stores a JSON blob in a Code field, so a malformed
	payload fails validation instead of blowing up later at read time.
	"""
	if value is None or value == "":
		return json.dumps(default if default is not None else {})

	if isinstance(value, dict | list):
		return json.dumps(value)

	try:
		json.loads(value)
	except TypeError, ValueError:
		frappe.throw(_("{0} is not valid JSON").format(_(label)), frappe.ValidationError)

	return value
