from cs_dynamicpages.controlpanels.dynamic_pages_control_panel.controlpanel import (
    IDynamicPagesControlPanel,
)
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class DynamicPagesControlPanelIntegrationTest(unittest.TestCase):
    """Integration tests for the Dynamic Pages Control Panel."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.registry = getUtility(IRegistry)

    def test_controlpanel_schema_registered(self):
        """Test that the control panel schema is registered in the registry."""
        records = self.registry.records
        self.assertIn(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields",
            records,
        )

    def test_row_type_fields_record_exists(self):
        """Test that row_type_fields registry record exists."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        )
        self.assertIsInstance(value, list)

    def test_row_widths_record_exists(self):
        """Test that row_widths registry record exists."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_widths"
        )
        self.assertIsInstance(value, list)

    def test_spacer_padding_top_record_exists(self):
        """Test that spacer_padding_top registry record exists."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.spacer_padding_top"
        )
        self.assertIsInstance(value, list)

    def test_spacer_padding_bottom_record_exists(self):
        """Test that spacer_padding_bottom registry record exists."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.spacer_padding_bottom"
        )
        self.assertIsInstance(value, list)

    def test_spacer_margin_top_record_exists(self):
        """Test that spacer_margin_top registry record exists."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.spacer_margin_top"
        )
        self.assertIsInstance(value, list)

    def test_spacer_margin_bottom_record_exists(self):
        """Test that spacer_margin_bottom registry record exists."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.spacer_margin_bottom"
        )
        self.assertIsInstance(value, list)

    def test_row_type_fields_has_default_values(self):
        """Test that row_type_fields has default row types configured."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        )
        row_types = [item["row_type"] for item in value]

        # Check for some expected default row types
        self.assertIn("cs_dynamicpages-horizontal-rule-view", row_types)
        self.assertIn("cs_dynamicpages-spacer-view", row_types)

    def test_row_widths_has_default_values(self):
        """Test that row_widths has default width options."""
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_widths"
        )
        self.assertTrue(len(value) > 0)

        # Check structure of first item
        first_item = value[0]
        self.assertIn("row_width_label", first_item)
        self.assertIn("row_width_class", first_item)

    def test_spacer_values_have_correct_structure(self):
        """Test that spacer values have correct structure."""
        for record_name in [
            "spacer_padding_top",
            "spacer_padding_bottom",
            "spacer_margin_top",
            "spacer_margin_bottom",
        ]:
            value = api.portal.get_registry_record(
                f"cs_dynamicpages.dynamic_pages_control_panel.{record_name}"
            )
            self.assertTrue(len(value) > 0, f"{record_name} should have values")

            # Check structure of first item
            first_item = value[0]
            self.assertIn("spacer_label", first_item)
            self.assertIn("spacer_class", first_item)


class DynamicPagesControlPanelSchemaTest(unittest.TestCase):
    """Tests for the control panel schema interface."""

    def test_schema_has_row_type_fields(self):
        """Test that schema has row_type_fields field."""
        self.assertIn("row_type_fields", IDynamicPagesControlPanel.names())

    def test_schema_has_row_widths(self):
        """Test that schema has row_widths field."""
        self.assertIn("row_widths", IDynamicPagesControlPanel.names())

    def test_schema_has_spacer_fields(self):
        """Test that schema has all spacer fields."""
        names = IDynamicPagesControlPanel.names()
        self.assertIn("spacer_padding_top", names)
        self.assertIn("spacer_padding_bottom", names)
        self.assertIn("spacer_margin_top", names)
        self.assertIn("spacer_margin_bottom", names)
