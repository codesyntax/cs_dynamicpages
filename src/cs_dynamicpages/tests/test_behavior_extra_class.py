from cs_dynamicpages.behaviors.extra_class import IExtraClassMarker
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class ExtraClassIntegrationTest(unittest.TestCase):
    """Integration tests for the extra_class behavior."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_extra_class_registered(self):
        """Test that the behavior is properly registered."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.extra_class")
        self.assertEqual(
            behavior.marker,
            IExtraClassMarker,
        )

    def test_behavior_extra_class_interface_name(self):
        """Test the behavior interface name."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.extra_class")
        self.assertEqual(
            behavior.interface.__name__,
            "IExtraClass",
        )

    def test_behavior_extra_class_title(self):
        """Test that the behavior has a title."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.extra_class")
        self.assertIsNotNone(behavior.title)
