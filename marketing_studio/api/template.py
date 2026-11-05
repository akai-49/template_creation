import json

import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import strip_html_tags, validate_email_address
from frappe.utils.html_utils import sanitize_html

from marketing_studio.utils import ensure_json

TEMPLATE = "Marketing Template"
SUBMISSION = "Marketing Form Submission"

# Guest submission limits. Generous enough for a long contact form, small enough
# that a bot can't push megabytes through an unauthenticated endpoint.
MAX_SUBMISSION_BYTES = 32 * 1024
MAX_SUBMISSION_FIELDS = 60
MAX_VALUE_LENGTH = 2000
MAX_NESTING_DEPTH = 3


@frappe.whitelist()
def get_block_library():
	# get_list (not get_all) so the block library respects Marketing Block read permissions.
	blocks = frappe.get_list(
		"Marketing Block",
		filters={"is_active": 1},
		fields=["name", "block_name", "block_type", "category", "icon", "default_props", "thumbnail"],
		order_by="category asc, block_name asc",
	)
	for block in blocks:
		if block.default_props:
			try:
				block.default_props = json.loads(block.default_props)
			except ValueError:
				block.default_props = {}
	return blocks


@frappe.whitelist()
def list_templates(template_type=None, status=None, category=None):
	filters = {}
	if template_type:
		filters["template_type"] = template_type
	if status:
		filters["status"] = status
	if category:
		filters["category"] = category
	return frappe.get_list(
		TEMPLATE,
		filters=filters,
		fields=[
			"name",
			"title",
			"template_type",
			"status",
			"category",
			"thumbnail",
			"modified",
			"is_default",
		],
		order_by="modified desc",
	)


@frappe.whitelist()
def get_template(name):
	doc = frappe.get_doc(TEMPLATE, name)
	doc.check_permission("read")
	data = doc.as_dict()
	if data.get("layout"):
		try:
			data["layout"] = json.loads(data["layout"])
		except ValueError:
			data["layout"] = {"blocks": []}
	else:
		data["layout"] = {"blocks": []}
	return data


@frappe.whitelist()
def create_template(title, template_type, category=None, layout=None):
	frappe.has_permission(TEMPLATE, "create", throw=True)
	doc = frappe.new_doc(TEMPLATE)
	doc.title = strip_html_tags(str(title))
	doc.template_type = template_type
	doc.category = category
	doc.layout = ensure_json(layout, "Layout", {"blocks": []})
	doc.insert()
	return doc.name


@frappe.whitelist()
def save_template_layout(name, layout, preview_html=None):
	doc = frappe.get_doc(TEMPLATE, name)
	doc.check_permission("write")
	doc.layout = ensure_json(layout, "Layout", {"blocks": []})
	if preview_html is not None:
		# Preview HTML is client-generated and may be rendered back in Desk or on a
		# public page, so it never gets stored raw.
		doc.preview_html = sanitize_html(preview_html, always_sanitize=True)
	doc.save()
	return {"name": doc.name, "modified": doc.modified}


@frappe.whitelist()
def duplicate_template(name, title=None):
	source = frappe.get_doc(TEMPLATE, name)
	source.check_permission("read")
	frappe.has_permission(TEMPLATE, "create", throw=True)
	new = frappe.copy_doc(source)
	new.title = strip_html_tags(str(title)) if title else f"{source.title} Copy"
	new.status = "Draft"
	new.is_default = 0
	new.insert()
	return new.name


@frappe.whitelist()
def create_version(name, version_label=None):
	template = frappe.get_doc(TEMPLATE, name)
	# Writing a version is a change to the template's history, so it needs write, not read.
	template.check_permission("write")
	return template.snapshot_version(version_label).name


@frappe.whitelist()
def list_versions(name):
	frappe.get_doc(TEMPLATE, name).check_permission("read")
	return frappe.get_list(
		"Marketing Template Version",
		filters={"template": name},
		fields=["name", "version_label", "creation", "owner"],
		order_by="creation desc",
	)


@frappe.whitelist()
def publish_template(name):
	doc = frappe.get_doc(TEMPLATE, name)
	doc.check_permission("write")
	doc.status = "Published"
	doc.published_on = frappe.utils.now()
	doc.save()
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=10, seconds=60)
def submit_form(template, data, campaign=None, honeypot=None, captcha_token=None):
	"""Public form endpoint. Untrusted input — everything below is a trust boundary."""
	if honeypot:
		# A hidden field only a bot fills in. Report success so it doesn't retry.
		return {"status": "ok"}

	_verify_captcha(captcha_token)
	payload = _clean_payload(data)

	tpl = frappe.db.get_value(TEMPLATE, template, ["name", "template_type", "status"], as_dict=True)
	if not tpl:
		frappe.throw(_("Form not found"), frappe.DoesNotExistError)
	if tpl.template_type != "Web Form":
		frappe.throw(_("Template is not a Web Form template"))
	if tpl.status != "Published":
		frappe.throw(_("This form is not accepting submissions"))

	email = payload.get("email")
	if email:
		validate_email_address(str(email), throw=True)

	submission = frappe.new_doc(SUBMISSION)
	submission.template = tpl.name
	submission.campaign = campaign
	submission.submitter_name = payload.get("name")
	submission.submitter_email = email
	submission.submitted_data = json.dumps(payload)
	submission.insert(ignore_permissions=True)
	# No frappe.db.commit() — the request teardown commits on success and rolls back on error.
	return {"status": "ok", "submission": submission.name}


def _clean_payload(data):
	"""Parse, size-check and strip markup from a guest-submitted payload."""
	if isinstance(data, str):
		if len(data.encode("utf-8")) > MAX_SUBMISSION_BYTES:
			frappe.throw(_("Submission is too large"), frappe.ValidationError)
		try:
			payload = json.loads(data)
		except ValueError:
			frappe.throw(_("Invalid submission data"), frappe.ValidationError)
	else:
		payload = data

	if not isinstance(payload, dict):
		frappe.throw(_("Invalid submission data"), frappe.ValidationError)
	if len(payload) > MAX_SUBMISSION_FIELDS:
		frappe.throw(_("Too many fields in submission"), frappe.ValidationError)

	return {_clean_key(key): _clean_value(value, 0) for key, value in payload.items()}


def _clean_key(key):
	return strip_html_tags(str(key))[:140]


def _clean_value(value, depth):
	if isinstance(value, bool) or isinstance(value, int | float) or value is None:
		return value
	if depth < MAX_NESTING_DEPTH:
		if isinstance(value, list):
			return [_clean_value(v, depth + 1) for v in value[:MAX_SUBMISSION_FIELDS]]
		if isinstance(value, dict):
			return {
				_clean_key(k): _clean_value(v, depth + 1)
				for k, v in list(value.items())[:MAX_SUBMISSION_FIELDS]
			}
	return strip_html_tags(str(value))[:MAX_VALUE_LENGTH]


def _verify_captcha(token):
	"""No-op unless `marketing_studio_captcha_secret` is set in central config or site config."""
	from msuite_core.central_config import get_central_config

	secret = get_central_config("marketing_studio_captcha_secret")
	if not secret:
		return

	from frappe.integrations.utils import make_post_request

	if not token:
		frappe.throw(_("Captcha verification failed"), frappe.ValidationError)

	url = get_central_config("marketing_studio_captcha_url") or "https://www.google.com/recaptcha/api/siteverify"
	result = make_post_request(
		url,
		data={"secret": secret, "response": token, "remoteip": frappe.local.request_ip},
	)
	if not result.get("success"):
		frappe.throw(_("Captcha verification failed"), frappe.ValidationError)
