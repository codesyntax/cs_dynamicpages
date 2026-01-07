from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.views.query_columns_view import IQueryColumnsView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class QueryColumnsViewsIntegrationTest(unittest.TestCase):
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
        self.row.row_type = "cs_dynamicpages-query-columns-view"

    def test_query_columns_view_is_registered(self):
        """Test that query columns view is registered for DynamicPageRow."""
        view = getMultiAdapter(
            (self.row, self.portal.REQUEST),
            name="cs_dynamicpages-query-columns-view",
        )
        self.assertTrue(IQueryColumnsView.providedBy(view))

    def test_query_columns_view_not_found_for_document(self):
        """Test that query columns view is not registered for Document."""
        doc = api.content.create(self.portal, "Document", "front-page")
        view_found = True
        try:
            getMultiAdapter(
                (doc, self.portal.REQUEST),
                name="cs_dynamicpages-query-columns-view",
            )
        except ComponentLookupError:
            view_found = False
        self.assertFalse(view_found)


class QueryColumnsViewsFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
