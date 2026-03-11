from cs_dynamicpages.behaviors.fetchpriority_image import IFetchPriorityImageMarker
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class FetchPriorityImageIntegrationTest(unittest.TestCase):
    """Integration tests for the fetchpriority_image behavior."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_fetchpriority_image_registered(self):
        """Test that the behavior is properly registered."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.fetchpriority_image")
        self.assertEqual(
            behavior.marker,
            IFetchPriorityImageMarker,
        )

    def test_behavior_fetchpriority_image_interface_name(self):
        """Test the behavior interface name."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.fetchpriority_image")
        self.assertEqual(
            behavior.interface.__name__,
            "IFetchPriorityImage",
        )

    def test_behavior_fetchpriority_image_title(self):
        """Test that the behavior has a title."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.fetchpriority_image")
        self.assertIsNotNone(behavior.title)
