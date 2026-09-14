from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.views.dynamic_page_folder_view import IDynamicPageFolderView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class DynamicPageFolderViewsIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a DynamicPageFolder
        self.folder = api.content.create(self.portal, "Folder", "test-folder")
        self.dpf = api.content.create(
            self.folder, "DynamicPageFolder", "rows", title="Rows"
        )

    def test_dynamic_page_folder_view_is_registered(self):
        """Test that view is registered for DynamicPageFolder."""
        view = getMultiAdapter(
            (self.dpf, self.portal.REQUEST),
            name="view",
        )
        self.assertTrue(IDynamicPageFolderView.providedBy(view))

    def test_dynamic_page_folder_view_not_found_for_document(self):
        """Test that view is not registered for Document."""
        doc = api.content.create(self.portal, "Document", "front-page")
        view_found = True
        try:
            view = getMultiAdapter(
                (doc, self.portal.REQUEST),
                name="view",
            )
            view_found = IDynamicPageFolderView.providedBy(view)
        except ComponentLookupError:
            view_found = False
        self.assertFalse(view_found)


class DynamicPageFolderViewsFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a DynamicPageFolder
        self.folder = api.content.create(self.portal, "Folder", "test-folder-dpf-func")
        self.dpf = api.content.create(
            self.folder, "DynamicPageFolder", "rows", title="Rows"
        )

    def test_dynamic_page_folder_view_renders_without_error(self):
        """Test that DynamicPageFolder view renders without raising an error."""
        view = getMultiAdapter(
            (self.dpf, self.request),
            name="view",
        )
        html = view()
        self.assertIsInstance(html, str)

    def test_dynamic_page_add_row_content_view(self):
        """Test adding a row via the add_row view without featured elements."""
        self.request.form["row_type"] = "dynamic_page_row"
        view = getMultiAdapter((self.dpf, self.request), name="add-row-content")

        # We need to mock get_available_views_for_row
        from unittest.mock import patch

        with patch(
            "cs_dynamicpages.views.dynamic_page_folder_view.get_available_views_for_row"
        ) as mock_get_views:
            mock_get_views.return_value = [
                {
                    "row_type": "dynamic_page_row",
                    "row_type_allows_children": False,
                }
            ]
            view()

            # Should have added a row
            rows = self.dpf.objectValues()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].portal_type, "DynamicPageRow")
            self.assertEqual(rows[0].row_type, "dynamic_page_row")

            # Should have redirected to parent url + anchor
            self.assertEqual(self.request.response.status, 302)
            self.assertIn(
                self.folder.absolute_url(), self.request.response.getHeader("Location")
            )

    def test_dynamic_page_add_row_content_view_with_featured(self):
        """Test adding a row via the add_row view with featured elements."""
        self.request.form["row_type"] = "dynamic_page_row_text"
        view = getMultiAdapter((self.dpf, self.request), name="add-row-content")

        from unittest.mock import patch

        with patch(
            "cs_dynamicpages.views.dynamic_page_folder_view.get_available_views_for_row"
        ) as mock_get_views:
            mock_get_views.return_value = [
                {
                    "row_type": "dynamic_page_row_text",
                    "row_type_allows_children": True,
                }
            ]
            view()

            # Should have added a row
            rows = self.dpf.objectValues()
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row.portal_type, "DynamicPageRow")
            self.assertEqual(row.row_type, "dynamic_page_row_text")

            # Should have added two rows inside the row
            featured = row.objectValues()
            self.assertEqual(len(featured), 2)
            self.assertEqual(featured[0].portal_type, "DynamicPageRow")
            self.assertEqual(featured[0].title, "New Nested Row")
            self.assertEqual(featured[1].portal_type, "DynamicPageRow")
            self.assertEqual(featured[1].title, "New Nested Row 2")

    def test_dynamic_page_add_row_content_view_no_row_type(self):
        """Test the view when no row_type is provided."""
        # Clean form just in case
        if "row_type" in self.request.form:
            del self.request.form["row_type"]

        view = getMultiAdapter((self.dpf, self.request), name="add-row-content")
        response = view()

        # No row should be added
        self.assertEqual(len(self.dpf.objectValues()), 0)
        # Should return None because __call__ returns implicit None if no row_type
        self.assertIsNone(response)

    def test_dynamic_page_add_row_content_view_with_position(self):
        """Test adding a row at a specific position."""
        # Create an existing row
        api.content.create(
            self.dpf, "DynamicPageRow", "row1", title="Row 1", row_type="type1"
        )
        api.content.create(
            self.dpf, "DynamicPageRow", "row2", title="Row 2", row_type="type1"
        )

        self.request.form["row_type"] = "type1"
        self.request.form["position"] = "1"
        view = getMultiAdapter((self.dpf, self.request), name="add-row-content")

        from unittest.mock import patch

        with patch(
            "cs_dynamicpages.views.dynamic_page_folder_view.get_available_views_for_row"
        ) as mock_get_views:
            mock_get_views.return_value = [
                {
                    "row_type": "type1",
                    "row_type_allows_children": False,
                }
            ]
            view()

            # Should have added a row at position 1
            row_ids = self.dpf.objectIds()
            self.assertEqual(len(row_ids), 3)
            # The new row has a random UUID as ID, so we check the second element
            self.assertEqual(row_ids[0], "row1")
            self.assertEqual(row_ids[2], "row2")
            # The middle one should be the new one
            self.assertNotEqual(row_ids[1], "row1")
            self.assertNotEqual(row_ids[1], "row2")
