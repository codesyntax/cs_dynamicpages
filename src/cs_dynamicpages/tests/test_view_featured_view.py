from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.views.featured_view import IFeaturedView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class FeaturedViewsIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a DynamicPageFolder with a DynamicPageRow
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
        self.row.row_type = "cs_dynamicpages-featured-view"

    def test_featured_view_is_registered(self):
        """Test that featured view is registered for DynamicPageRow."""
        view = getMultiAdapter(
            (self.row, self.portal.REQUEST),
            name="cs_dynamicpages-featured-view",
        )
        self.assertTrue(IFeaturedView.providedBy(view))

    def test_featured_view_not_found_for_document(self):
        """Test that featured view is not registered for Document."""
        doc = api.content.create(self.portal, "Document", "front-page")
        view_found = True
        try:
            getMultiAdapter(
                (doc, self.portal.REQUEST),
                name="cs_dynamicpages-featured-view",
            )
        except ComponentLookupError:
            view_found = False
        self.assertFalse(view_found)


class FeaturedViewsFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create content structure
        self.folder = api.content.create(self.portal, "Folder", "test-folder-featured")
        self.dpf = api.content.create(
            self.folder, "DynamicPageFolder", "rows", title="Rows"
        )
        self.row = api.content.create(
            self.dpf,
            "DynamicPageRow",
            "test-row-featured",
            title="Test Row",
        )
        self.row.row_type = "cs_dynamicpages-featured-view"

    def test_featured_view_renders_without_error(self):
        """Test that featured view renders without raising an error."""
        # Set required attributes to avoid None errors
        self.row.link_url = ""
        self.row.link_text = ""
        self.row.image_position = "left"

        view = getMultiAdapter(
            (self.row, self.request),
            name="cs_dynamicpages-featured-view",
        )
        html = view()
        self.assertIsInstance(html, str)

    def test_featured_view_renders_row_structure(self):
        """Test that featured view renders Bootstrap row structure."""
        self.row.link_url = ""
        self.row.link_text = ""
        self.row.image_position = "left"

        view = getMultiAdapter(
            (self.row, self.request),
            name="cs_dynamicpages-featured-view",
        )
        html = view()
        self.assertIn('class="row"', html)
        self.assertIn("col-md-6", html)

    def test_featured_view_renders_title(self):
        """Test that featured view renders the row title."""
        self.row.link_url = ""
        self.row.link_text = ""
        self.row.image_position = "left"

        view = getMultiAdapter(
            (self.row, self.request),
            name="cs_dynamicpages-featured-view",
        )
        html = view()
        self.assertIn("Test Row", html)
