from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.views.dynamic_page_row_featured_view import (
    IDynamicPageRowFeaturedView,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class DynamicPageRowFeaturedViewsIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a DynamicPageFolder with a DynamicPageRow and Featured item
        self.folder = api.content.create(self.portal, "Folder", "test-folder")
        self.dpf = api.content.create(
            self.folder, "DynamicPageFolder", "rows", title="Rows"
        )
        self.row = api.content.create(
            self.dpf,
            "DynamicPageRow",
            "test-row",
            title="Test Row",
        )
        self.featured = api.content.create(
            self.row,
            "DynamicPageRowFeatured",
            "test-featured",
            title="Test Featured",
        )

    def test_dynamic_page_row_featured_view_is_registered(self):
        """Test that view is registered for DynamicPageRowFeatured."""
        view = getMultiAdapter(
            (self.featured, self.portal.REQUEST),
            name="view",
        )
        self.assertTrue(IDynamicPageRowFeaturedView.providedBy(view))

    def test_dynamic_page_row_featured_view_not_found_for_document(self):
        """Test that view is not registered for Document."""
        doc = api.content.create(self.portal, "Document", "front-page")
        view_found = True
        try:
            view = getMultiAdapter(
                (doc, self.portal.REQUEST),
                name="view",
            )
            view_found = IDynamicPageRowFeaturedView.providedBy(view)
        except ComponentLookupError:
            view_found = False
        self.assertFalse(view_found)


class DynamicPageRowFeaturedViewsFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create full content structure
        self.folder = api.content.create(
            self.portal, "Folder", "test-folder-featured-func"
        )
        self.dpf = api.content.create(
            self.folder, "DynamicPageFolder", "rows", title="Rows"
        )
        self.row = api.content.create(
            self.dpf,
            "DynamicPageRow",
            "test-row",
            title="Test Row",
        )
        self.featured = api.content.create(
            self.row,
            "DynamicPageRowFeatured",
            "test-featured-func",
            title="Test Featured",
        )

    def test_dynamic_page_row_featured_view_renders_without_error(self):
        """Test that DynamicPageRowFeatured view renders without error."""
        view = getMultiAdapter(
            (self.featured, self.request),
            name="view",
        )
        html = view()
        self.assertIsInstance(html, str)
