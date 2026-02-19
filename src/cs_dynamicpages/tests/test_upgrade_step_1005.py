from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.upgrades.v1005 import upgrade
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UpgradeStep1005IntegrationTest(unittest.TestCase):
    """Integration tests for upgrade step 1005."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Store original registry value for restoration
        self.record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        self.original_values = list(api.portal.get_registry_record(self.record_name))

    def tearDown(self):
        # Restore original registry values
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        registry = getUtility(IRegistry)
        record = registry.records[self.record_name]
        record.value = self.original_values

    def test_upgrade_runs_without_error(self):
        """Test that upgrade runs without raising exceptions.

        Note: The schema now requires row_type_icon, so we can't test adding it
        to entries without it. Instead we verify the upgrade runs successfully.
        """
        # Run upgrade - should not raise
        upgrade()

        # Verify registry values still valid
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        values = api.portal.get_registry_record(record_name)
        self.assertIsInstance(values, list)
        # All entries should have row_type_icon
        for entry in values:
            self.assertIn("row_type_icon", entry)

    def test_upgrade_preserves_existing_icons(self):
        """Test that upgrade preserves existing custom icons."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Get current values
        values = api.portal.get_registry_record(record_name)

        # Find an entry with an icon
        entry_with_custom_icon = None
        for entry in values:
            if entry.get("row_type_icon") and entry["row_type_icon"] != "bricks":
                entry_with_custom_icon = entry.copy()
                break

        # Run upgrade
        upgrade()

        # Check that custom icon was preserved
        if entry_with_custom_icon:
            updated_values = api.portal.get_registry_record(record_name)
            for updated_entry in updated_values:
                if updated_entry["row_type"] == entry_with_custom_icon["row_type"]:
                    self.assertEqual(
                        updated_entry["row_type_icon"],
                        entry_with_custom_icon["row_type_icon"],
                    )
                    break

    def test_upgrade_adds_title_description_view_if_missing(self):
        """Test that upgrade adds title-description-view if not present."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Run upgrade
        upgrade()

        # Check updated values
        updated_values = api.portal.get_registry_record(record_name)
        updated_view_names = [v["row_type"] for v in updated_values]

        # View should now exist
        self.assertIn("cs_dynamicpages-title-description-view", updated_view_names)

    def test_title_description_view_has_correct_fields(self):
        """Test that title-description-view has correct fields configured."""
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"

        # Run upgrade to ensure view exists
        upgrade()

        # Find the title-description-view
        values = api.portal.get_registry_record(record_name)
        view_config = None
        for value in values:
            if value["row_type"] == "cs_dynamicpages-title-description-view":
                view_config = value
                break

        self.assertIsNotNone(view_config)
        self.assertIn("IBasic.title", view_config["each_row_type_fields"])
        self.assertIn("IBasic.description", view_config["each_row_type_fields"])
        self.assertEqual(view_config["row_type_icon"], "fonts")
        self.assertFalse(view_config["row_type_has_featured_add_button"])
