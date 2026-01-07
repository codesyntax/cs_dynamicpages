from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.utils import _url_uses_scheme
from cs_dynamicpages.utils import absolute_target_url
from cs_dynamicpages.utils import add_custom_view
from cs_dynamicpages.utils import enable_behavior
from cs_dynamicpages.utils import get_available_views_for_row
from cs_dynamicpages.utils import NON_REDIRECTABLE_URL_SCHEMES
from cs_dynamicpages.utils import NON_RESOLVABLE_URL_SCHEMES
from cs_dynamicpages.utils import normalize_uid_from_path
from cs_dynamicpages.utils import VIEW_PREFIX
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestNormalizeUidFromPath(unittest.TestCase):
    """Tests for normalize_uid_from_path function."""

    def test_returns_none_tuple_for_empty_url(self):
        uid, fragment = normalize_uid_from_path(None)
        self.assertIsNone(uid)
        self.assertIsNone(fragment)

    def test_returns_none_tuple_for_empty_string(self):
        uid, fragment = normalize_uid_from_path("")
        self.assertIsNone(uid)
        self.assertIsNone(fragment)

    def test_extracts_uid_from_resolveuid_path(self):
        uid, fragment = normalize_uid_from_path("/resolveuid/abc123")
        self.assertEqual(uid, "abc123")
        self.assertIsNone(fragment)

    def test_extracts_uid_case_insensitive(self):
        uid, fragment = normalize_uid_from_path("/ResolveUid/abc123")
        self.assertEqual(uid, "abc123")
        self.assertIsNone(fragment)

    def test_extracts_uid_and_fragment(self):
        uid, fragment = normalize_uid_from_path("/resolveuid/abc123#section1")
        self.assertEqual(uid, "abc123")
        self.assertEqual(fragment, "#section1")

    def test_returns_none_when_resolveuid_at_end(self):
        uid, fragment = normalize_uid_from_path("/resolveuid/")
        self.assertIsNone(uid)
        self.assertIsNone(fragment)

    def test_returns_none_for_url_without_resolveuid(self):
        uid, fragment = normalize_uid_from_path("/some/path/to/content")
        self.assertIsNone(uid)
        self.assertIsNone(fragment)

    def test_handles_full_url_with_resolveuid(self):
        uid, fragment = normalize_uid_from_path(
            "http://example.com/resolveuid/abc123#anchor"
        )
        self.assertEqual(uid, "abc123")
        self.assertEqual(fragment, "#anchor")


class TestUrlUsesScheme(unittest.TestCase):
    """Tests for _url_uses_scheme function."""

    def test_returns_true_for_mailto(self):
        self.assertTrue(_url_uses_scheme(NON_REDIRECTABLE_URL_SCHEMES, "mailto:test@example.com"))

    def test_returns_true_for_tel(self):
        self.assertTrue(_url_uses_scheme(NON_REDIRECTABLE_URL_SCHEMES, "tel:+1234567890"))

    def test_returns_true_for_callto(self):
        self.assertTrue(_url_uses_scheme(NON_REDIRECTABLE_URL_SCHEMES, "callto:username"))

    def test_returns_false_for_http(self):
        self.assertFalse(_url_uses_scheme(NON_REDIRECTABLE_URL_SCHEMES, "http://example.com"))

    def test_returns_false_for_https(self):
        self.assertFalse(_url_uses_scheme(NON_REDIRECTABLE_URL_SCHEMES, "https://example.com"))

    def test_returns_true_for_file_in_non_resolvable(self):
        self.assertTrue(_url_uses_scheme(NON_RESOLVABLE_URL_SCHEMES, "file:///path/to/file"))

    def test_returns_true_for_ftp_in_non_resolvable(self):
        self.assertTrue(_url_uses_scheme(NON_RESOLVABLE_URL_SCHEMES, "ftp://server/path"))

    def test_returns_false_for_empty_schemes_list(self):
        self.assertFalse(_url_uses_scheme([], "mailto:test@example.com"))


class TestViewPrefix(unittest.TestCase):
    """Tests for VIEW_PREFIX constant."""

    def test_view_prefix_value(self):
        self.assertEqual(VIEW_PREFIX, "cs_dynamicpages-")


class AddCustomViewIntegrationTest(unittest.TestCase):
    """Integration tests for add_custom_view function.

    Note: add_custom_view modifies registry with values that may not satisfy
    schema constraints. These tests verify the function works but we cannot
    easily test the actual registry modification due to schema validation.
    """

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
        # Direct assignment to bypass validation for cleanup
        record = registry.records[self.record_name]
        record.value = self.original_values

    def test_add_custom_view_returns_true(self):
        # Use an existing view name to avoid schema constraint issues
        existing_views = get_available_views_for_row()
        if existing_views:
            # Test with existing view - function should still work
            result = add_custom_view(
                existing_views[0]["row_type"],
                ["title", "description"],
                has_button=False,
                icon="star",
            )
            # Function returns True even if view already exists
            self.assertTrue(result)
        else:
            self.skipTest("No existing views to test with")

    def test_add_custom_view_structure(self):
        """Test that add_custom_view creates correct structure."""
        # Test using slider-view which is registered
        view_name = "cs_dynamicpages-slider-view"
        original_len = len(api.portal.get_registry_record(self.record_name))

        add_custom_view(view_name, ["title"], has_button=True, icon="heart")

        values = api.portal.get_registry_record(self.record_name)
        # Should have added one entry
        self.assertEqual(len(values), original_len + 1)

        # Last entry should be our new one
        matching = [v for v in values if v["row_type"] == view_name and v["row_type_icon"] == "heart"]
        self.assertTrue(len(matching) >= 1)

    def test_add_custom_view_default_icon_is_bricks(self):
        """Test that default icon is 'bricks'."""
        view_name = "cs_dynamicpages-featured-view"

        add_custom_view(view_name, ["title"])

        values = api.portal.get_registry_record(self.record_name)
        matching = [v for v in values if v["row_type"] == view_name]
        # Should find at least one entry (original + new)
        last_match = matching[-1]  # Get the last added one
        self.assertEqual(last_match["row_type_icon"], "bricks")


class EnableBehaviorIntegrationTest(unittest.TestCase):
    """Integration tests for enable_behavior function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_enable_behavior_adds_to_fti(self):
        behavior_name = "plone.basic"
        portal_types = api.portal.get_tool("portal_types")
        fti = getattr(portal_types, "DynamicPageRow", None)

        # Store original behaviors
        original_behaviors = fti.behaviors

        # Only test if behavior not already present
        if behavior_name not in fti.behaviors:
            enable_behavior(behavior_name)
            self.assertIn(behavior_name, fti.behaviors)

            # Restore original behaviors
            fti.behaviors = original_behaviors

    def test_enable_behavior_does_not_duplicate(self):
        portal_types = api.portal.get_tool("portal_types")
        fti = getattr(portal_types, "DynamicPageRow", None)

        # Get a behavior that's already enabled
        if fti.behaviors:
            existing_behavior = fti.behaviors[0]
            original_count = fti.behaviors.count(existing_behavior)

            enable_behavior(existing_behavior)

            # Count should remain the same
            self.assertEqual(fti.behaviors.count(existing_behavior), original_count)


class GetAvailableViewsForRowIntegrationTest(unittest.TestCase):
    """Integration tests for get_available_views_for_row function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_returns_list(self):
        result = get_available_views_for_row()
        self.assertIsInstance(result, list)

    def test_all_items_have_required_keys(self):
        result = get_available_views_for_row()
        required_keys = [
            "row_type",
            "each_row_type_fields",
            "row_type_has_featured_add_button",
            "row_type_icon",
        ]
        for item in result:
            for key in required_keys:
                self.assertIn(key, item)

    def test_all_row_types_start_with_prefix(self):
        result = get_available_views_for_row()
        for item in result:
            self.assertTrue(
                item["row_type"].startswith(VIEW_PREFIX),
                f"Row type {item['row_type']} does not start with {VIEW_PREFIX}",
            )


class AbsoluteTargetUrlIntegrationTest(unittest.TestCase):
    """Integration tests for absolute_target_url function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_returns_mailto_unchanged(self):
        url = "mailto:test@example.com"
        result = absolute_target_url(url)
        self.assertEqual(result, url)

    def test_returns_tel_unchanged(self):
        url = "tel:+1234567890"
        result = absolute_target_url(url)
        self.assertEqual(result, url)

    def test_returns_file_unchanged(self):
        url = "file:///path/to/file"
        result = absolute_target_url(url)
        self.assertEqual(result, url)

    def test_returns_ftp_unchanged(self):
        url = "ftp://server/path"
        result = absolute_target_url(url)
        self.assertEqual(result, url)

    def test_returns_url_unchanged_when_no_resolveuid(self):
        url = "http://example.com/page"
        result = absolute_target_url(url)
        self.assertEqual(result, url)

    def test_returns_original_url_for_invalid_uid(self):
        url = "/resolveuid/nonexistent-uid-12345"
        result = absolute_target_url(url)
        self.assertEqual(result, url)

    def test_resolves_valid_uid_to_url(self):
        # Create a document to resolve
        doc = api.content.create(
            container=self.portal,
            type="Document",
            id="test-doc-for-url",
            title="Test Document",
        )
        uid = doc.UID()

        url = f"/resolveuid/{uid}"
        result = absolute_target_url(url)
        self.assertEqual(result, doc.absolute_url())

        # Cleanup
        api.content.delete(obj=doc)

    def test_resolves_uid_with_fragment(self):
        # Create a document to resolve
        doc = api.content.create(
            container=self.portal,
            type="Document",
            id="test-doc-for-fragment",
            title="Test Document",
        )
        uid = doc.UID()

        url = f"/resolveuid/{uid}#section1"
        result = absolute_target_url(url)
        self.assertEqual(result, f"{doc.absolute_url()}#section1")

        # Cleanup
        api.content.delete(obj=doc)
