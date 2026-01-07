from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.views.slider_view import ISliderView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class SliderViewsIntegrationTest(unittest.TestCase):
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
        self.row.row_type = "cs_dynamicpages-slider-view"

    def test_slider_view_is_registered(self):
        """Test that slider view is registered for DynamicPageRow."""
        view = getMultiAdapter(
            (self.row, self.portal.REQUEST),
            name="cs_dynamicpages-slider-view",
        )
        self.assertTrue(ISliderView.providedBy(view))

    def test_slider_view_not_found_for_document(self):
        """Test that slider view is not registered for Document."""
        doc = api.content.create(self.portal, "Document", "front-page")
        view_found = True
        try:
            getMultiAdapter(
                (doc, self.portal.REQUEST),
                name="cs_dynamicpages-slider-view",
            )
        except ComponentLookupError:
            view_found = False
        self.assertFalse(view_found)


class SliderViewsFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create content structure
        self.folder = api.content.create(self.portal, "Folder", "test-folder-slider")
        self.dpf = api.content.create(
            self.folder, "DynamicPageFolder", "rows", title="Rows"
        )
        self.row = api.content.create(
            self.dpf,
            "DynamicPageRow",
            "test-row-slider",
            title="Test Row",
        )
        self.row.row_type = "cs_dynamicpages-slider-view"

    def test_slider_view_renders_without_error(self):
        """Test that slider view renders without raising an error."""
        view = getMultiAdapter(
            (self.row, self.request),
            name="cs_dynamicpages-slider-view",
        )
        html = view()
        self.assertIsInstance(html, str)

    def test_slider_view_renders_carousel_with_elements(self):
        """Test that slider view renders carousel structure when elements exist."""
        # Create a featured item for the slider with required attributes
        featured = api.content.create(
            self.row,
            "DynamicPageRowFeatured",
            "featured-1",
            title="Featured Item",
        )
        # Set required attributes to avoid None errors
        featured.link_url = ""
        featured.link_text = ""
        api.content.transition(obj=featured, transition="publish")

        view = getMultiAdapter(
            (self.row, self.request),
            name="cs_dynamicpages-slider-view",
        )
        html = view()
        self.assertIn("carousel", html)
        self.assertIn("carousel-inner", html)
