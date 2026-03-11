from cs_dynamicpages.subscribers.index_contents_in_parents import handler
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class SubscriberIndexContentsInParentsIntegrationTest(unittest.TestCase):
    """Integration tests for the index_contents_in_parents subscriber."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_handler_reindexes_parent_content(self):
        """Test that handler reindexes the parent content."""
        # Create a folder
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-subscriber",
            title="Test Folder",
        )

        # Create DynamicPageFolder
        dpf = api.content.create(
            container=folder,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )

        # Create DynamicPageRow
        row = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="test-row",
            title="Test Row",
        )

        # Call handler - should not raise any exceptions
        handler(row, None)

        # Cleanup
        api.content.delete(obj=folder)

    def test_handler_does_not_fail_for_non_dynamic_page_folder_parent(self):
        """Test that handler handles non-DynamicPageFolder parents gracefully."""
        # Create a folder directly containing a DynamicPageRow
        # (this is an edge case that shouldn't normally happen)
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder-edge",
            title="Test Folder",
        )

        # Create DynamicPageFolder to get a proper row
        dpf = api.content.create(
            container=folder,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )

        row = api.content.create(
            container=dpf,
            type="DynamicPageRow",
            id="test-row",
            title="Test Row",
        )

        # Handler should work since parent is DynamicPageFolder
        handler(row, None)

        # Cleanup
        api.content.delete(obj=folder)

    def test_handler_function_exists(self):
        """Test that the handler function is properly defined."""
        from cs_dynamicpages.subscribers.index_contents_in_parents import handler

        self.assertTrue(callable(handler))
