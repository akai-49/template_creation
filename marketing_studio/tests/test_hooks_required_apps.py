"""Tests asserting Marketing Studio hooks declare required app dependencies."""

from unittest import TestCase

from marketing_studio import hooks

EXPECTED_REQUIRED_APP = "msuite_campaigns"
DISALLOWED_REQUIRED_APP = "msuite_workspace"


class TestHooksRequiredApps(TestCase):
	"""Verify required_apps hook declarations."""

	def test_required_apps_names_msuite_campaigns(self):
		"""Assert required_apps declares msuite_campaigns and not legacy msuite_workspace."""
		self.assertTrue(hasattr(hooks, "required_apps"), "marketing_studio/hooks.py must define required_apps")
		self.assertEqual(hooks.required_apps, [EXPECTED_REQUIRED_APP])
		self.assertNotIn(DISALLOWED_REQUIRED_APP, hooks.required_apps)


def test_required_apps_names_msuite_campaigns():
	"""Pytest-style test function for required_apps hook declaration."""
	assert hasattr(hooks, "required_apps"), "marketing_studio/hooks.py must define required_apps"
	assert hooks.required_apps == [EXPECTED_REQUIRED_APP]
	assert DISALLOWED_REQUIRED_APP not in hooks.required_apps
