from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.upgrades.v1011 import upgrade
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UpgradeStep1011IntegrationTest(unittest.TestCase):
    """Integration tests for upgrade step 1011."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        self.registry = api.portal.get_tool("portal_registry")
        # Store original registry value for restoration
        self.original_values = list(self.registry.get(self.record_name, []))

    def tearDown(self):
        # Restore original registry values
        self.registry[self.record_name] = self.original_values

    def test_upgrade_migrates_registry_keys(self):
        """Test that upgrade renames row_type_has_featured_add_button.

        Renames to row_type_allows_children.
        """
        # Manually set "old" data. We use a list of dicts.
        # We need to temporarily bypass schema validation because we want to
        # insert data that matches the OLD schema.
        from plone.registry.field import Dict
        from plone.registry.field import List

        record = self.registry.records[self.record_name]
        original_field = record.field
        record.field = List(value_type=Dict())

        old_data = [
            {
                "row_type": "cs_dynamicpages-text-view",
                "each_row_type_fields": ["IBasic.title"],
                "row_type_has_featured_add_button": True,
                "row_type_icon": "body-text",
            },
            {
                "row_type": "cs_dynamicpages-horizontal-rule-view",
                "each_row_type_fields": ["IBasic.title"],
                "row_type_has_featured_add_button": False,
                "row_type_icon": "hr",
            },
        ]

        try:
            self.registry[self.record_name] = old_data

            # Restore the field so the upgrade step sees the "real" registry state
            # (though the upgrade step uses registry.get() which might bypass
            # field validation)
            record.field = original_field

            # Run upgrade
            upgrade()

            # Verify results
            new_data = self.registry.get(self.record_name)

            # Find the text-view entry
            text_view = None
            hr_view = None
            for entry in new_data:
                if entry["row_type"] == "cs_dynamicpages-text-view":
                    text_view = entry
                if entry["row_type"] == "cs_dynamicpages-horizontal-rule-view":
                    hr_view = entry

            self.assertIsNotNone(text_view)
            self.assertIsNotNone(hr_view)

            # Check that old key is gone and new key exists with correct value
            self.assertNotIn("row_type_has_featured_add_button", text_view)
            self.assertIn("row_type_allows_children", text_view)
            self.assertTrue(text_view["row_type_allows_children"])

            self.assertNotIn("row_type_has_featured_add_button", hr_view)
            self.assertIn("row_type_allows_children", hr_view)
            self.assertFalse(hr_view["row_type_allows_children"])
        finally:
            record.field = original_field

    def test_upgrade_adds_new_primitives(self):
        """Test that upgrade adds image-view and card-view if missing."""
        # Ensure we start with a registry that doesn't have them
        current_values = [
            v
            for v in self.original_values
            if v["row_type"]
            not in ["cs_dynamicpages-image-view", "cs_dynamicpages-card-view"]
        ]
        self.registry[self.record_name] = current_values

        # Run upgrade
        upgrade()

        # Verify results
        new_data = self.registry.get(self.record_name)
        new_types = [v["row_type"] for v in new_data]

        self.assertIn("cs_dynamicpages-image-view", new_types)
        self.assertIn("cs_dynamicpages-card-view", new_types)

        # Verify they use the new key
        image_view = next(
            v for v in new_data if v["row_type"] == "cs_dynamicpages-image-view"
        )
        self.assertIn("row_type_allows_children", image_view)
        self.assertFalse(image_view["row_type_allows_children"])

    def test_upgrade_migrates_content(self):
        """Test that DynamicPageRowFeatured items are migrated to DynamicPageRow."""
        # 1. Manually create an FTI for the old type so we can create objects
        types_tool = api.portal.get_tool("portal_types")
        from plone.dexterity.fti import DexterityFTI

        if "DynamicPageRowFeatured" not in types_tool.objectIds():
            fti = DexterityFTI("DynamicPageRowFeatured")
            fti.klass = "plone.dexterity.content.Item"  # Generic class
            types_tool._setObject("DynamicPageRowFeatured", fti)

        # 2. Create parent and old content
        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="page",
            title="Page",
        )
        row = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="row",
            title="Parent Row",
            row_type="cs_dynamicpages-slider-view",
        )

        # 2b. Temporarily allow DynamicPageRowFeatured in DynamicPageRow FTI
        row_fti = types_tool.getTypeInfo("DynamicPageRow")
        original_allowed = row_fti.allowed_content_types
        row_fti.allowed_content_types = (*original_allowed, "DynamicPageRowFeatured")

        # We use invokeFactory directly because api.content.create checks
        # for FTI validity in ways that might fail if we don't set up the
        # FTI perfectly.
        row.invokeFactory("DynamicPageRowFeatured", "feat", title="Old Featured")
        feat = row["feat"]
        feat.text = "Some text"
        feat.reindexObject()

        self.assertEqual(len(row.objectValues()), 1)
        self.assertEqual(row.objectValues()[0].portal_type, "DynamicPageRowFeatured")

        # 3. Run upgrade
        upgrade()

        # 3b. Run the XML profile manually to simulate the full upgrade step
        setup = api.portal.get_tool("portal_setup")
        setup.runAllImportStepsFromProfile("profile-cs_dynamicpages.upgrades:1011")

        # 4. Verify migration
        # The old object should be gone, new one should exist
        self.assertEqual(len(row.objectValues()), 1)
        new_feat = row.objectValues()[0]
        self.assertEqual(new_feat.portal_type, "DynamicPageRow")
        self.assertEqual(new_feat.Title(), "Old Featured")
        self.assertEqual(
            new_feat.row_type, "cs_dynamicpages-image-view"
        )  # Sliders get image-view
        self.assertEqual(new_feat.text, "Some text")

        # 5. Verify FTI removal
        self.assertNotIn("DynamicPageRowFeatured", types_tool.objectIds())

        # Cleanup FTI if it still exists (it shouldn't)
        row_fti.allowed_content_types = original_allowed
        if "DynamicPageRowFeatured" in types_tool.objectIds():
            types_tool._delObject("DynamicPageRowFeatured")
