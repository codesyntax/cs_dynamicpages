from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import patch

import unittest


class TestPurgeUtils(unittest.TestCase):
    """Tests for the cache purge utility function."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("cs_dynamicpages.cache.utils.notify")
    def test_purge_item_from_cache_notifies_purge_event(self, mock_notify):
        from cs_dynamicpages.cache.utils import purge_item_from_cache
        from z3c.caching.purge import Purge

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-utils-folder",
            title="Test Folder",
        )

        purge_item_from_cache(folder)

        mock_notify.assert_called_once()
        args = mock_notify.call_args[0]
        self.assertIsInstance(args[0], Purge)
        self.assertIs(args[0].object, folder)

        api.content.delete(obj=folder)


class TestPurgeDynamicPageRow(unittest.TestCase):
    """Tests for the DynamicPageRow cache purge handler."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("cs_dynamicpages.cache.dynamic_page_row.purge_item_from_cache")
    def test_purge_row_purges_self_parent_and_grandparent(self, mock_purge):
        from cs_dynamicpages.cache.dynamic_page_row import purge

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-row-folder",
            title="Test Folder",
        )
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

        purge(row, None)

        self.assertEqual(mock_purge.call_count, 3)
        mock_purge.assert_any_call(row)
        mock_purge.assert_any_call(dpf)
        mock_purge.assert_any_call(folder)

        api.content.delete(obj=folder)

    def test_purge_row_smoke(self):
        from cs_dynamicpages.cache.dynamic_page_row import purge

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-row-smoke",
            title="Test Folder",
        )
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

        purge(row, None)

        api.content.delete(obj=folder)


class TestPurgeDynamicPageFolder(unittest.TestCase):
    """Tests for the DynamicPageFolder cache purge handler."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("cs_dynamicpages.cache.dynamic_page_folder.purge_item_from_cache")
    def test_purge_folder_purges_self_and_parent(self, mock_purge):
        from cs_dynamicpages.cache.dynamic_page_folder import purge

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-dpf-folder",
            title="Test Folder",
        )
        dpf = api.content.create(
            container=folder,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )

        purge(dpf, None)

        self.assertEqual(mock_purge.call_count, 2)
        mock_purge.assert_any_call(dpf)
        mock_purge.assert_any_call(folder)

        api.content.delete(obj=folder)

    @patch("cs_dynamicpages.cache.dynamic_page_folder.purge_item_from_cache")
    def test_purge_folder_at_portal_root(self, mock_purge):
        from cs_dynamicpages.cache.dynamic_page_folder import purge

        dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="root-dpf",
            title="Root DPF",
        )

        purge(dpf, None)

        self.assertEqual(mock_purge.call_count, 2)
        mock_purge.assert_any_call(dpf)
        mock_purge.assert_any_call(self.portal)

        api.content.delete(obj=dpf)

    def test_purge_folder_smoke(self):
        from cs_dynamicpages.cache.dynamic_page_folder import purge

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-dpf-smoke",
            title="Test Folder",
        )
        dpf = api.content.create(
            container=folder,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )

        purge(dpf, None)

        api.content.delete(obj=folder)


class TestPurgeSubscriberRegistration(unittest.TestCase):
    """Smoke test: verify purge handlers are wired via ZCML."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_dynamic_page_row_purge_handlers_importable(self):
        from cs_dynamicpages.cache.dynamic_page_folder import purge as purge_folder
        from cs_dynamicpages.cache.dynamic_page_row import purge

        self.assertTrue(callable(purge))
        self.assertTrue(callable(purge_folder))

    def test_purge_subscribers_fire_on_object_modified_event(self):
        from zope.event import notify
        from zope.lifecycleevent import ObjectModifiedEvent

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-subscriber-folder",
            title="Test Folder",
        )
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
        # Test nesting
        nested = api.content.create(
            container=row,
            type="DynamicPageRow",
            id="test-nested",
            title="Test Nested",
        )

        notify(ObjectModifiedEvent(row))
        notify(ObjectModifiedEvent(nested))
        notify(ObjectModifiedEvent(dpf))

        api.content.delete(obj=folder)


class TestPurgeAPIEndpoint(unittest.TestCase):
    """Tests for the @purge REST API endpoint."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("cs_dynamicpages.api.services.purge.post.notify")
    def test_purge_endpoint_fires_purge_event(self, mock_notify):
        from cs_dynamicpages.api.services.purge.post import PurgePost
        from z3c.caching.purge import Purge

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-api-purge",
            title="Test Folder",
        )

        view = PurgePost()
        view.context = folder
        view.request = self.portal.REQUEST
        view.reply()

        mock_notify.assert_called_once()
        args = mock_notify.call_args[0]
        self.assertIsInstance(args[0], Purge)
        self.assertIs(args[0].object, folder)

        api.content.delete(obj=folder)

    def test_purge_endpoint_returns_no_content(self):
        from cs_dynamicpages.api.services.purge.post import PurgePost

        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-api-purge-nc",
            title="Test Folder",
        )

        view = PurgePost()
        view.context = folder
        view.request = self.portal.REQUEST
        view.reply()

        self.assertEqual(self.portal.REQUEST.response.getStatus(), 204)

        api.content.delete(obj=folder)
