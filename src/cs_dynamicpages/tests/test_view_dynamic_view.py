from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.views.dynamic_view import IDynamicView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_dynamic_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="dynamic-view"
        )
        self.assertTrue(IDynamicView.providedBy(view))

    def test_dynamic_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST), name="dynamic-view"
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IDynamicView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_dynamic_view_renders_without_error(self):
        """Test that dynamic view renders without raising an error."""
        folder = api.content.create(self.portal, "Folder", "test-folder-dynamic")
        view = getMultiAdapter(
            (folder, self.request),
            name="dynamic-view",
        )
        html = view()
        self.assertIsInstance(html, str)

    def test_dynamic_view_renders_with_rows(self):
        """Test that dynamic view renders rows correctly."""
        folder = api.content.create(self.portal, "Folder", "test-folder-with-rows")
        # Create DynamicPageFolder with a row
        dpf = api.content.create(folder, "DynamicPageFolder", "rows", title="Rows")
        api.content.transition(obj=dpf, transition="publish")

        row = api.content.create(
            dpf,
            "DynamicPageRow",
            "test-row",
            title="Test Row",
        )
        row.row_type = "cs_dynamicpages-horizontal-rule-view"
        api.content.transition(obj=row, transition="publish")

        view = getMultiAdapter(
            (folder, self.request),
            name="dynamic-view",
        )
        html = view()
        # Should contain main content area
        self.assertIn("content", html)

    def test_dynamic_view_rows_method_returns_rows(self):
        """Test that dynamic view rows() method returns created rows."""
        folder = api.content.create(self.portal, "Folder", "test-folder-rows-method")
        dpf = api.content.create(folder, "DynamicPageFolder", "rows", title="Rows")
        row = api.content.create(
            dpf,
            "DynamicPageRow",
            "test-row",
            title="Test Row",
        )
        row.row_type = "cs_dynamicpages-horizontal-rule-view"

        view = getMultiAdapter(
            (folder, self.request),
            name="dynamic-view",
        )
        rows = view.rows()
        self.assertEqual(len(rows), 1)
