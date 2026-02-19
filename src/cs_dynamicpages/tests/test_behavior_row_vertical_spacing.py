from cs_dynamicpages.behaviors.row_vertical_spacing import IRowVerticalSpacingMarker
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class RowVerticalSpacingIntegrationTest(unittest.TestCase):
    """Integration tests for the row_vertical_spacing behavior."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_row_vertical_spacing_registered(self):
        """Test that the behavior is properly registered."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertEqual(
            behavior.marker,
            IRowVerticalSpacingMarker,
        )

    def test_behavior_row_vertical_spacing_interface_name(self):
        """Test the behavior interface name."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertEqual(
            behavior.interface.__name__,
            "IRowVerticalSpacing",
        )

    def test_behavior_row_vertical_spacing_title(self):
        """Test that the behavior has a title."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertIsNotNone(behavior.title)

    def test_behavior_has_padding_top_field(self):
        """Test that the behavior schema has padding_top field."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertIn("padding_top", behavior.interface.names())

    def test_behavior_has_padding_bottom_field(self):
        """Test that the behavior schema has padding_bottom field."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertIn("padding_bottom", behavior.interface.names())

    def test_behavior_has_margin_top_field(self):
        """Test that the behavior schema has margin_top field."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertIn("margin_top", behavior.interface.names())

    def test_behavior_has_margin_bottom_field(self):
        """Test that the behavior schema has margin_bottom field."""
        behavior = getUtility(IBehavior, "cs_dynamicpages.row_vertical_spacing")
        self.assertIn("margin_bottom", behavior.interface.names())
