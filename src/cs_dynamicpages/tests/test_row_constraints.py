from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.utils import get_available_views_for_row
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestRowConstraints(unittest.TestCase):
    """Integration tests for row type constraints."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.registry = api.portal.get_tool("portal_registry")
        self.record_name = "cs_dynamicpages.dynamic_pages_control_panel.top_level_row_types"
        self.fields_record = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        
        # Store original registry values for restoration
        try:
            self.original_top_level = list(self.registry.get(self.record_name, []))
        except (KeyError, AttributeError):
            self.original_top_level = []
            
        # Ensure we have clean dicts to restore
        self.original_fields = [dict(v) for v in self.registry.get(self.fields_record, [])]

    def tearDown(self):
        # Restore original registry values
        # We need to bypass validation because original_fields might not match the NEW schema
        # if the test failed mid-way or if we're in a transitional state.
        # But actually, I updated the defaults in controlpanel.py, so it should be fine.
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        
        try:
            if self.record_name in registry:
                registry.records[self.record_name].value = self.original_top_level
        except (KeyError, AttributeError):
            pass
            
        if self.fields_record in registry:
            # Add missing keys to original fields for validation to pass
            for item in self.original_fields:
                if "allowed_child_row_types" not in item:
                    item["allowed_child_row_types"] = []
            registry.records[self.fields_record].value = self.original_fields

    def test_get_available_views_for_row_filters_top_level(self):
        """Test filtering of top-level row types."""
        # 1. Setup a DynamicPageFolder (top-level container)
        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="rows-top",
            title="Rows",
        )

        # 2. Get all available views (no constraints yet)
        all_views = get_available_views_for_row(dpf)
        all_types = [v["row_type"] for v in all_views]
        self.assertGreater(len(all_types), 2)

        # 3. Set a constraint in the registry
        allowed = [
            "cs_dynamicpages-title-description-view",
            "cs_dynamicpages-horizontal-rule-view"
        ]
        
        self.registry[self.record_name] = allowed

        # 4. Verify filtering
        filtered_views = get_available_views_for_row(dpf)
        filtered_types = [v["row_type"] for v in filtered_views]
        
        self.assertEqual(len(filtered_types), 2)
        self.assertIn("cs_dynamicpages-title-description-view", filtered_types)
        self.assertIn("cs_dynamicpages-horizontal-rule-view", filtered_types)
        self.assertNotIn("cs_dynamicpages-slider-view", filtered_types)

    def test_get_available_views_for_row_filters_child_level(self):
        """Test filtering of child row types."""
        # 1. Setup a Slider row
        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="rows-child",
            title="Rows",
        )
        slider = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="slider",
            title="Slider",
            row_type="cs_dynamicpages-slider-view",
        )

        # 2. Get all available views for slider (no constraints yet)
        all_views = get_available_views_for_row(slider)
        all_types = [v["row_type"] for v in all_views]
        self.assertGreater(len(all_types), 2)

        # 3. Set a constraint for slider in registry
        # Sliders only allow image-view
        row_type_fields = [dict(v) for v in self.original_fields]
        for item in row_type_fields:
            # Ensure key exists for all
            if "allowed_child_row_types" not in item:
                item["allowed_child_row_types"] = []
            if item["row_type"] == "cs_dynamicpages-slider-view":
                item["allowed_child_row_types"] = ["cs_dynamicpages-image-view"]
        
        self.registry[self.fields_record] = row_type_fields

        # 4. Verify filtering
        filtered_views = get_available_views_for_row(slider)
        filtered_types = [v["row_type"] for v in filtered_views]
        
        self.assertEqual(len(filtered_types), 1)
        self.assertIn("cs_dynamicpages-image-view", filtered_types)
        self.assertNotIn("cs_dynamicpages-text-view", filtered_types)
