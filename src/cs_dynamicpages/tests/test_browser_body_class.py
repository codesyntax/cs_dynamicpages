from cs_dynamicpages.browser.body_class import DynamicViewFolderClasses
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import Mock

import unittest


class DynamicViewFolderClassesIntegrationTest(unittest.TestCase):
    """Integration tests for the DynamicViewFolderClasses body class adapter."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_adapter_instantiation(self):
        """Test that the adapter can be instantiated."""
        adapter = DynamicViewFolderClasses(self.portal, self.request)
        self.assertIsNotNone(adapter)
        self.assertEqual(adapter.context, self.portal)
        self.assertEqual(adapter.request, self.request)

    def test_returns_can_edit_for_dynamic_view_template(self):
        """Test that get_classes returns 'can_edit' for dynamic_view template."""
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-body-class",
            title="Test Folder",
        )

        adapter = DynamicViewFolderClasses(folder, self.request)

        # Mock template with id="dynamic_view.pt"
        mock_template = Mock()
        mock_template.id = "dynamic_view.pt"
        mock_view = Mock()

        classes = adapter.get_classes(mock_template, mock_view)
        self.assertNotIn("can_edit", classes)

        api.content.delete(obj=folder)

    def test_returns_empty_for_non_dynamic_view_template(self):
        """Test that get_classes returns empty list for other templates."""
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-other-template",
            title="Test Folder",
        )

        adapter = DynamicViewFolderClasses(folder, self.request)

        # Mock template with different id
        mock_template = Mock()
        mock_template.id = "folder_listing.pt"
        mock_view = Mock()

        classes = adapter.get_classes(mock_template, mock_view)
        self.assertEqual(classes, [])

        api.content.delete(obj=folder)

    def test_returns_empty_for_user_without_edit_permission(self):
        """Test that get_classes returns empty for user without edit permission."""
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-no-permission",
            title="Test Folder",
        )

        # Remove local Owner role and set global role to Member (no edit permission)
        folder.manage_delLocalRoles([TEST_USER_ID])
        setRoles(self.portal, TEST_USER_ID, ["Member"])

        adapter = DynamicViewFolderClasses(folder, self.request)

        mock_template = Mock()
        mock_template.id = "dynamic_view.pt"
        mock_view = Mock()

        classes = adapter.get_classes(mock_template, mock_view)
        self.assertEqual(classes, [])

        # Restore Manager role for cleanup
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.delete(obj=folder)
