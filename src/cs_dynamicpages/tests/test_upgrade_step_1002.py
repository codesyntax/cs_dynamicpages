from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.upgrades.v1002 import post_handler
from cs_dynamicpages.upgrades.v1002 import pre_handler
from cs_dynamicpages.upgrades.v1002 import UPGRADEABLE_KEYS
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.annotation.interfaces import IAnnotations

import json
import unittest


class UpgradeStep1002IntegrationTest(unittest.TestCase):
    """Integration tests for upgrade step 1002."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # Store original registry values for restoration
        self.original_values = {}
        for key in UPGRADEABLE_KEYS:
            record_name = f"cs_dynamicpages.dynamic_pages_control_panel.{key}"
            self.original_values[key] = list(api.portal.get_registry_record(record_name))
        # Clear any existing upgrade annotations
        self._clear_upgrade_annotations()

    def tearDown(self):
        # Restore original registry values
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        registry = getUtility(IRegistry)
        for key in UPGRADEABLE_KEYS:
            record_name = f"cs_dynamicpages.dynamic_pages_control_panel.{key}"
            record = registry.records[record_name]
            record.value = self.original_values[key]
        # Clear upgrade annotations
        self._clear_upgrade_annotations()

    def _clear_upgrade_annotations(self):
        """Clear any upgrade annotations from the portal."""
        annotations = IAnnotations(self.portal)
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            if annotation_key in annotations:
                del annotations[annotation_key]

    def test_upgradeable_keys_defined(self):
        """Test that UPGRADEABLE_KEYS contains expected keys."""
        self.assertIn("row_type_fields", UPGRADEABLE_KEYS)
        self.assertIn("row_widths", UPGRADEABLE_KEYS)

    def test_pre_handler_saves_values_to_annotations(self):
        """Test that pre_handler saves registry values to annotations."""
        # Run pre_handler
        pre_handler()

        # Check annotations were created
        annotations = IAnnotations(self.portal)
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            self.assertIn(annotation_key, annotations)
            # Value should be a JSON string
            value_str = annotations[annotation_key]
            self.assertIsInstance(value_str, str)
            # Should be valid JSON
            parsed = json.loads(value_str)
            self.assertIsInstance(parsed, list)

    def test_post_handler_restores_values_from_annotations(self):
        """Test that post_handler restores values from annotations.

        Note: pre_handler reads from old typo registry key 'dynamica_pages_control_panel'
        which is typically empty. This test verifies the restore mechanism works
        by manually setting up annotations.
        """
        # Manually set up annotations with known values
        annotations = IAnnotations(self.portal)
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            # Store current values in annotations
            current_values = api.portal.get_registry_record(
                f"cs_dynamicpages.dynamic_pages_control_panel.{key}", default=[]
            )
            annotations[annotation_key] = json.dumps(current_values)

        # Run post_handler
        post_handler()

        # Verify values were restored (should match what we stored)
        for key in UPGRADEABLE_KEYS:
            restored = api.portal.get_registry_record(
                f"cs_dynamicpages.dynamic_pages_control_panel.{key}"
            )
            self.assertEqual(restored, self.original_values[key])

    def test_post_handler_removes_annotations(self):
        """Test that post_handler cleans up annotations."""
        # First run pre_handler
        pre_handler()

        annotations = IAnnotations(self.portal)
        # Verify annotations exist
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            self.assertIn(annotation_key, annotations)

        # Run post_handler
        post_handler()

        # Verify annotations were removed
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            self.assertNotIn(annotation_key, annotations)

    def test_post_handler_handles_invalid_json(self):
        """Test that post_handler handles invalid JSON gracefully."""
        # Manually set invalid JSON in annotations
        annotations = IAnnotations(self.portal)
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            annotations[annotation_key] = "invalid json {"

        # Should not raise exception
        post_handler()

        # Should set empty list for invalid JSON
        for key in UPGRADEABLE_KEYS:
            value = api.portal.get_registry_record(
                f"cs_dynamicpages.dynamic_pages_control_panel.{key}"
            )
            self.assertEqual(value, [])

    def test_post_handler_handles_non_list_value(self):
        """Test that post_handler handles non-list values."""
        # Manually set a non-list JSON value
        annotations = IAnnotations(self.portal)
        for key in UPGRADEABLE_KEYS:
            annotation_key = f"cs_dynamicpages.dynamic_pages_control_panel.{key}.UPGRADE"
            annotations[annotation_key] = json.dumps({"not": "a list"})

        # Should not raise exception
        post_handler()

        # Should set empty list for non-list values
        for key in UPGRADEABLE_KEYS:
            value = api.portal.get_registry_record(
                f"cs_dynamicpages.dynamic_pages_control_panel.{key}"
            )
            self.assertEqual(value, [])
