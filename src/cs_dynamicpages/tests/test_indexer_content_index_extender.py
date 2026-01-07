from cs_dynamicpages.indexers.content_index_extender import extract_text_value_to_index
from cs_dynamicpages.indexers.content_index_extender import FIELDS_TO_INDEX
from cs_dynamicpages.indexers.content_index_extender import FolderishItemTextExtender
from cs_dynamicpages.indexers.content_index_extender import (
    get_available_text_from_dynamic_pages,
)
from cs_dynamicpages.indexers.content_index_extender import get_enabled_fields
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue

import unittest


class TestFieldsToIndex(unittest.TestCase):
    """Tests for FIELDS_TO_INDEX constant."""

    def test_contains_title_field(self):
        self.assertIn("IBasic.title", FIELDS_TO_INDEX)

    def test_contains_description_field(self):
        self.assertIn("IBasic.description", FIELDS_TO_INDEX)

    def test_contains_text_field(self):
        self.assertIn("IRichTextBehavior-text", FIELDS_TO_INDEX)

    def test_title_field_is_callable(self):
        self.assertTrue(callable(FIELDS_TO_INDEX["IBasic.title"]))

    def test_description_field_is_callable(self):
        self.assertTrue(callable(FIELDS_TO_INDEX["IBasic.description"]))

    def test_text_field_is_callable(self):
        self.assertTrue(callable(FIELDS_TO_INDEX["IRichTextBehavior-text"]))


class ExtractTextValueToIndexIntegrationTest(unittest.TestCase):
    """Integration tests for extract_text_value_to_index function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_extracts_plain_text_from_html(self):
        doc = api.content.create(
            container=self.portal,
            type="Document",
            id="test-doc-html",
            title="Test Document",
        )
        doc.text = RichTextValue(
            "<p>Hello <strong>World</strong></p>",
            "text/html",
            "text/x-html-safe",
        )

        result = extract_text_value_to_index(doc)
        self.assertIn("Hello", result)
        self.assertIn("World", result)
        self.assertNotIn("<p>", result)
        self.assertNotIn("<strong>", result)

        api.content.delete(obj=doc)

    def test_returns_empty_for_none_text(self):
        doc = api.content.create(
            container=self.portal,
            type="Document",
            id="test-doc-none",
            title="Test Document",
        )
        doc.text = None

        result = extract_text_value_to_index(doc)
        self.assertEqual(result, "")

        api.content.delete(obj=doc)


class GetEnabledFieldsIntegrationTest(unittest.TestCase):
    """Integration tests for get_enabled_fields function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Store original registry value for restoration
        self.record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        self.original_values = list(api.portal.get_registry_record(self.record_name))

    def tearDown(self):
        # Restore original registry values to prevent test pollution
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        registry = getUtility(IRegistry)
        record = registry.records[self.record_name]
        record.value = self.original_values

    def test_returns_list(self):
        result = get_enabled_fields("cs_dynamicpages-horizontal-rule-view")
        self.assertIsInstance(result, list)

    def test_returns_empty_list_for_unknown_row_type(self):
        result = get_enabled_fields("nonexistent-row-type")
        self.assertEqual(result, [])

    def test_returns_fields_for_known_row_type(self):
        # Test with an existing registered view
        result = get_enabled_fields("cs_dynamicpages-slider-view")
        # slider-view should have fields defined
        self.assertIsInstance(result, list)


class FolderishItemTextExtenderIntegrationTest(unittest.TestCase):
    """Integration tests for FolderishItemTextExtender class."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_returns_empty_string_for_non_dynamic_layout(self):
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-non-dynamic",
            title="Test Folder",
        )

        extender = FolderishItemTextExtender(folder)
        result = extender()
        self.assertEqual(result, "")

        api.content.delete(obj=folder)

    def test_calls_get_available_text_for_dynamic_layout(self):
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-dynamic",
            title="Test Folder",
        )
        folder.setLayout("dynamic-view")

        extender = FolderishItemTextExtender(folder)
        result = extender()
        # Should return a string (may be empty if no dynamic page rows)
        self.assertIsInstance(result, str)

        api.content.delete(obj=folder)


class GetAvailableTextFromDynamicPagesIntegrationTest(unittest.TestCase):
    """Integration tests for get_available_text_from_dynamic_pages function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Store original registry value for restoration
        self.record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        self.original_values = list(api.portal.get_registry_record(self.record_name))

    def tearDown(self):
        # Restore original registry values to prevent test pollution
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        registry = getUtility(IRegistry)
        record = registry.records[self.record_name]
        record.value = self.original_values

    def test_returns_string(self):
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-text",
            title="Test Folder",
        )

        result = get_available_text_from_dynamic_pages(folder)
        self.assertIsInstance(result, str)

        api.content.delete(obj=folder)

    def test_returns_empty_for_folder_without_rows(self):
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-empty",
            title="Test Folder",
        )

        result = get_available_text_from_dynamic_pages(folder)
        self.assertEqual(result, "")

        api.content.delete(obj=folder)

    def test_extracts_text_from_published_rows(self):
        # Create folder
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-with-rows",
            title="Test Folder",
        )
        api.content.transition(obj=folder, transition="publish")

        # Create DynamicPageFolder
        dpf = api.content.create(
            container=folder,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )
        api.content.transition(obj=dpf, transition="publish")

        # Use slider-view which has IBasic.title enabled
        view_name = "cs_dynamicpages-slider-view"

        # Create DynamicPageRow
        row = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="test-row",
            title="Indexable Row Title",
        )
        row.row_type = view_name
        api.content.transition(obj=row, transition="publish")

        result = get_available_text_from_dynamic_pages(folder)
        self.assertIn("Indexable Row Title", result)

        api.content.delete(obj=folder)

    def test_ignores_unpublished_rows(self):
        # Create folder
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-unpublished",
            title="Test Folder",
        )

        # Create DynamicPageFolder
        dpf = api.content.create(
            container=folder,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )

        # Use slider-view which has IBasic.title enabled
        view_name = "cs_dynamicpages-slider-view"

        # Create unpublished DynamicPageRow
        row = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="test-row-unpublished",
            title="Should Not Be Indexed",
        )
        row.row_type = view_name
        # Don't publish the row

        result = get_available_text_from_dynamic_pages(folder)
        self.assertNotIn("Should Not Be Indexed", result)

        api.content.delete(obj=folder)
