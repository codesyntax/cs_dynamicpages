from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import json
import unittest


class DynamicPagesControlPanelImportExportTest(unittest.TestCase):
    """Integration tests for Export/Import in Dynamic Pages Control Panel."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_export(self):
        """Test the export functionality."""
        view = getMultiAdapter(
            (self.portal, self.request),
            name="dynamic_pages_export_config",
        )
        output = view()

        # Verify output is valid JSON and contains expected keys
        data = json.loads(output)
        self.assertIn("row_type_fields", data)
        self.assertIn("row_widths", data)
        self.assertEqual(
            self.request.response.getHeader("Content-Type"), "application/json"
        )
        self.assertIn(
            "attachment; filename=dynamic_pages_config.json",
            self.request.response.getHeader("Content-Disposition"),
        )

    def test_export_button_redirects(self):
        """Test that the export button in the control panel redirects to export view."""
        view = getMultiAdapter(
            (self.portal, self.request),
            name="dynamic_pages_control_panel-controlpanel",
        )
        view.update()
        form = view.form_instance
        form.handleExport(form, None)

        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertIn(
            "@@dynamic_pages_export_config", self.request.response.getHeader("Location")
        )

    def test_import(self):
        """Test the import functionality."""
        # 1. Prepare some custom data to import
        custom_data = {
            "row_widths": [
                {"row_width_label": "Test Width", "row_width_class": "test-class"}
            ]
        }
        json_data = json.dumps(custom_data)

        # 2. Get the import form
        view = getMultiAdapter(
            (self.portal, self.request),
            name="dynamic_pages_import_form",
        )
        view.update()
        form = view.form_instance

        # 3. Mock the extractData to return our custom JSON
        # In a real form submission, this would come from the uploaded file
        form.extractData = lambda: ({"import_file": json_data}, [])

        # 4. Call handleImport
        form.handleImport(form, None)

        # 5. Verify the registry was updated
        value = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_widths"
        )
        self.assertEqual(len(value), 1)
        self.assertEqual(value[0]["row_width_label"], "Test Width")
        self.assertEqual(value[0]["row_width_class"], "test-class")
