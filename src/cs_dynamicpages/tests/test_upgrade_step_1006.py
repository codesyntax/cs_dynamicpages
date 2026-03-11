from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.upgrades.v1006 import upgrade
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UpgradeStep1006IntegrationTest(unittest.TestCase):
    """Integration tests for upgrade step 1006."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_upgrade_enables_row_vertical_spacing_behavior(self):
        """Test that upgrade enables the row_vertical_spacing behavior."""
        portal_types = api.portal.get_tool("portal_types")
        fti = getattr(portal_types, "DynamicPageRow", None)

        # Run upgrade
        upgrade()

        # Check behavior is enabled
        self.assertIn("cs_dynamicpages.row_vertical_spacing", fti.behaviors)

    def test_upgrade_adds_vertical_spacing_fields_to_all_row_types(self):
        """Test that upgrade adds vertical spacing fields to all row types."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Run upgrade
        upgrade()

        # Check all row types have the new fields
        values = api.portal.get_registry_record(record_name)
        expected_fields = [
            "IRowVerticalSpacing.padding_top",
            "IRowVerticalSpacing.padding_bottom",
            "IRowVerticalSpacing.margin_top",
            "IRowVerticalSpacing.margin_bottom",
        ]

        for value in values:
            fields = value["each_row_type_fields"]
            for expected_field in expected_fields:
                self.assertIn(
                    expected_field,
                    fields,
                    f"Field {expected_field} not found in row type {value['row_type']}",
                )

    def test_upgrade_preserves_existing_fields(self):
        """Test that upgrade preserves existing fields in row types."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Get original fields for first row type
        values = api.portal.get_registry_record(record_name)
        if values:
            original_fields = values[0]["each_row_type_fields"].copy()
            original_row_type = values[0]["row_type"]

            # Run upgrade
            upgrade()

            # Check original fields are preserved
            updated_values = api.portal.get_registry_record(record_name)
            for updated in updated_values:
                if updated["row_type"] == original_row_type:
                    for field in original_fields:
                        self.assertIn(field, updated["each_row_type_fields"])
                    break
