from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.upgrades.v1007 import upgrade
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UpgradeStep1007IntegrationTest(unittest.TestCase):
    """Integration tests for upgrade step 1007."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    # Row types that should get the fetchpriority_image field
    TARGET_ROW_TYPES = [
        "cs_dynamicpages-slider-view",
        "cs_dynamicpages-features-view",
        "cs_dynamicpages-query-columns-view",
        "cs_dynamicpages-featured-overlay-view",
        "cs_dynamicpages-featured-view",
    ]

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_upgrade_enables_fetchpriority_image_behavior(self):
        """Test that upgrade enables the fetchpriority_image behavior."""
        portal_types = api.portal.get_tool("portal_types")
        fti = getattr(portal_types, "DynamicPageRow", None)

        # Run upgrade
        upgrade()

        # Check behavior is enabled
        self.assertIn("cs_dynamicpages.fetchpriority_image", fti.behaviors)

    def test_upgrade_adds_fetchpriority_field_to_target_row_types(self):
        """Test that upgrade adds fetchpriority field to specific row types."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Run upgrade
        upgrade()

        # Check target row types have the new field
        values = api.portal.get_registry_record(record_name)

        for value in values:
            if value["row_type"] in self.TARGET_ROW_TYPES:
                self.assertIn(
                    "IFetchPriorityImage.fetchpriority_image",
                    value["each_row_type_fields"],
                    f"Field not found in target row type {value['row_type']}",
                )

    def test_upgrade_does_not_add_field_to_other_row_types(self):
        """Test that upgrade does not add field to non-target row types."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Get original state
        original_values = api.portal.get_registry_record(record_name)
        non_target_types_fields = {}
        for value in original_values:
            if value["row_type"] not in self.TARGET_ROW_TYPES:
                # Check if fetchpriority field is already present
                has_field = "IFetchPriorityImage.fetchpriority_image" in value.get(
                    "each_row_type_fields", []
                )
                non_target_types_fields[value["row_type"]] = has_field

        # Run upgrade
        upgrade()

        # Check non-target row types do not have the field (unless they had it before)
        updated_values = api.portal.get_registry_record(record_name)
        for value in updated_values:
            if value["row_type"] not in self.TARGET_ROW_TYPES:
                if not non_target_types_fields.get(value["row_type"], False):
                    self.assertNotIn(
                        "IFetchPriorityImage.fetchpriority_image",
                        value["each_row_type_fields"],
                        f"Field unexpectedly added to non-target row type {value['row_type']}",
                    )

    def test_upgrade_preserves_existing_fields_in_target_types(self):
        """Test that upgrade preserves existing fields in target row types."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Get original fields for a target row type
        values = api.portal.get_registry_record(record_name)
        target_type_fields = None
        target_row_type = None

        for value in values:
            if value["row_type"] in self.TARGET_ROW_TYPES:
                target_row_type = value["row_type"]
                target_type_fields = value["each_row_type_fields"].copy()
                break

        if target_type_fields is None:
            self.skipTest("No target row types found in registry")

        # Run upgrade
        upgrade()

        # Check original fields are preserved
        updated_values = api.portal.get_registry_record(record_name)
        for updated in updated_values:
            if updated["row_type"] == target_row_type:
                for field in target_type_fields:
                    self.assertIn(field, updated["each_row_type_fields"])
                break
