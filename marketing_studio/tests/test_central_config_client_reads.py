"""Tests for Marketing Studio client reads from central configuration."""

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock, patch

import frappe
from msuite_core.central_config import clear_all, store_snapshot
from marketing_studio.api.template import _verify_captcha


class TestMarketingStudioCentralConfigClientReads(TestCase):
	"""Test suite asserting marketing_studio client reads resolve via central config."""

	def setUp(self) -> None:
		"""Clean up central config and backup frappe.conf."""
		clear_all()
		self._original_conf = dict(frappe.conf)

	def tearDown(self) -> None:
		"""Restore frappe.conf and clean up central config."""
		clear_all()
		frappe.conf = self._original_conf

	@patch("frappe.integrations.utils.make_post_request")
	def test_verify_captcha_resolution(self, mock_post: MagicMock) -> None:
		"""Verify _verify_captcha obeys default -> site_config -> pushed hierarchy."""
		mock_post.return_value = {"success": True}

		# (a) Default: no secret configured -> no-op, make_post_request not called
		with patch.dict(frappe.conf, {"marketing_studio_captcha_secret": None}):
			_verify_captcha("dummy_token")
			mock_post.assert_not_called()

		# (b) site_config honoured
		with patch.dict(
			frappe.conf,
			{
				"marketing_studio_captcha_secret": "conf-secret",
				"marketing_studio_captcha_url": "https://conf.captcha.local/verify",
			},
		):
			_verify_captcha("dummy_token")
			mock_post.assert_called_with(
				"https://conf.captcha.local/verify",
				data={"secret": "conf-secret", "response": "dummy_token", "remoteip": getattr(frappe.local, "request_ip", None)},
			)

		mock_post.reset_mock()

		# (c) Pushed value wins over site_config
		store_snapshot({
			"marketing_studio_captcha_secret": "pushed-secret",
			"marketing_studio_captcha_url": "https://pushed.captcha.local/verify",
		})
		with patch.dict(
			frappe.conf,
			{
				"marketing_studio_captcha_secret": "conf-secret",
				"marketing_studio_captcha_url": "https://conf.captcha.local/verify",
			},
		):
			_verify_captcha("dummy_token")
			mock_post.assert_called_with(
				"https://pushed.captcha.local/verify",
				data={"secret": "pushed-secret", "response": "dummy_token", "remoteip": getattr(frappe.local, "request_ip", None)},
			)
