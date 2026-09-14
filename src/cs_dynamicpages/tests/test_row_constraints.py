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
        self.record_name = (
            "cs_dynamicpages.dynamic_pages_control_panel.top_level_row_types"
        )
        self.fields_record = (
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        )

        # Store original registry values for restoration
        try:
            self.original_top_level = list(self.registry.get(self.record_name, []))
        except (KeyError, AttributeError):
            self.original_top_level = []

        # Ensure we have clean dicts to restore
        self.original_fields = [
            dict(v) for v in self.registry.get(self.fields_record, [])
        ]

    def tearDown(self):
        # Restore original registry values
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
            "cs_dynamicpages-horizontal-rule-view",
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

    def test_row_types_constraints_json(self):
        """Test that constraints are correctly exported as JSON."""
        from cs_dynamicpages.views.dynamic_view import DynamicView

        view = DynamicView(self.portal, self.layer["request"])

        # Set a top-level constraint
        self.registry[self.record_name] = ["cs_dynamicpages-text-view"]

        import json

        constraints = json.loads(view.row_types_constraints())
        self.assertIn("top_level", constraints)
        self.assertEqual(constraints["top_level"], ["cs_dynamicpages-text-view"])
        self.assertIn("cs_dynamicpages-slider-view", constraints)

    def test_row_type_vocabulary_top_level(self):
        """Test vocabulary filtering at top level."""
        from zope.component import getUtility
        from zope.schema.interfaces import IVocabularyFactory

        # 1. Setup container
        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="rows-vocab-top",
            title="Rows",
        )

        # 2. Set constraint
        self.registry[self.record_name] = ["cs_dynamicpages-text-view"]

        # 3. Call vocabulary
        factory = getUtility(IVocabularyFactory, name="cs_dynamicpages.RowType")
        vocab = factory(dpf)

        # 4. Verify
        self.assertEqual(len(vocab), 1)
        self.assertEqual(
            vocab.getTerm("cs_dynamicpages-text-view").value,
            "cs_dynamicpages-text-view",
        )

    def test_row_type_vocabulary_nested(self):
        """Test vocabulary filtering for nested rows."""
        from zope.component import getUtility
        from zope.schema.interfaces import IVocabularyFactory

        # 1. Setup hierarchy
        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="rows-vocab-nested",
            title="Rows",
        )
        slider = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="slider",
            title="Slider",
            row_type="cs_dynamicpages-slider-view",
        )

        # 2. Set constraint for sliders
        row_type_fields = [dict(v) for v in self.original_fields]
        for item in row_type_fields:
            if item["row_type"] == "cs_dynamicpages-slider-view":
                item["allowed_child_row_types"] = ["cs_dynamicpages-image-view"]
                break
        self.registry[self.fields_record] = row_type_fields

        # 3. Call vocabulary with slider as context (Add scenario)
        # We need to simulate being in an add form so the vocabulary
        # treats slider as container
        self.layer["request"].set(
            "ACTUAL_URL", slider.absolute_url() + "/++add++DynamicPageRow"
        )

        factory = getUtility(IVocabularyFactory, name="cs_dynamicpages.RowType")
        vocab = factory(slider)

        # 4. Verify
        self.assertIn("cs_dynamicpages-image-view", vocab)
        self.assertNotIn("cs_dynamicpages-text-view", vocab)

        # Cleanup request
        self.layer["request"].set("ACTUAL_URL", "")

    def test_row_type_vocabulary_edit_preserves_current(self):
        """Test that editing a row preserves its current value.

        It should stay in vocab even if forbidden by constraints.
        """
        from zope.component import getUtility
        from zope.schema.interfaces import IVocabularyFactory

        # 1. Setup row at top level
        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="rows-vocab-edit",
            title="Rows",
        )
        row = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="row",
            title="Legacy Row",
            row_type="cs_dynamicpages-slider-view",  # Current type
        )

        # 2. Restrict top level to ONLY text-view
        self.registry[self.record_name] = ["cs_dynamicpages-text-view"]

        # 3. Call vocabulary with the row itself (Edit scenario)
        factory = getUtility(IVocabularyFactory, name="cs_dynamicpages.RowType")
        vocab = factory(row)

        # 4. Verify both the allowed and the current are there
        self.assertIn("cs_dynamicpages-text-view", vocab)
        self.assertIn("cs_dynamicpages-slider-view", vocab)
        self.assertEqual(len(vocab), 2)

    def test_debug_adapters_lookup(self):
        from cs_dynamicpages.content.dynamic_page_row import IDynamicPageRow
        from zope.component import getSiteManager
        from zope.interface import Interface
        from zope.publisher.interfaces.browser import IBrowserRequest

        sm = getSiteManager()
        print("\nDEBUG ADAPTERS LOOKUP:")

        # Try different required interfaces
        lookups = [
            (IDynamicPageRow, Interface),
            (IDynamicPageRow, IBrowserRequest),
        ]

        for required in lookups:
            adapters = sm.adapters.lookupAll(required, Interface)
            count = len([a for a in adapters if a[0].startswith("cs_dynamicpages-")])
            print(f"Lookup {required}: {count} prefixed adapters found")

        self.assertTrue(True)
