from cs_dynamicpages.browser.forms import RowEditForm
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestBlockEditingForms(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.container = self.portal[
            self.portal.invokeFactory("DynamicPageFolder", "f1")
        ]
        self.row = self.portal.f1[
            self.portal.f1.invokeFactory(
                "DynamicPageRow", "r1", row_type="cs_dynamicpages-text-view"
            )
        ]

    def test_metadata_extraction(self):
        from cs_dynamicpages.utils import get_row_config

        config = get_row_config("cs_dynamicpages-text-view")
        self.assertIsNotNone(config)
        self.assertIn("IRichTextBehavior-text", config["each_row_type_fields"])
        self.assertEqual(config["row_type_icon"], "body-text")

    def test_edit_form_filters_widgets(self):
        from plone.app.z3cform.interfaces import IPloneFormLayer
        from zope.interface import alsoProvides

        request = self.portal.REQUEST.clone()
        alsoProvides(request, IPloneFormLayer)

        form = RowEditForm(self.row, request)
        form.update()

        def get_widget(form, name):
            widget = form.widgets.get(name)
            if widget:
                return widget
            for group in form.groups:
                widget = group.widgets.get(name)
                if widget:
                    return widget
            return None

        # In text-view, IRichTextBehavior.text should be visible
        text_widget = get_widget(form, "IRichTextBehavior.text")
        if not text_widget:
            text_widget = get_widget(form, "IRichTextBehavior-text")

        self.assertIsNotNone(text_widget)

        # IRelatedImage.related_image should be GONE in text-view
        image_widget = get_widget(form, "IRelatedImage.related_image")
        if not image_widget:
            image_widget = get_widget(form, "IRelatedImage-related_image")
        self.assertIsNone(image_widget)

    def test_registry_override(self):
        from plone import api

        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        registry_values = api.portal.get_registry_record(record_name)

        # Find text-view and change its icon in registry
        for val in registry_values:
            if val["row_type"] == "cs_dynamicpages-text-view":
                val["row_type_icon"] = "override-icon"
                break

        api.portal.set_registry_record(record_name, registry_values)

        from cs_dynamicpages.utils import get_row_config

        config = get_row_config("cs_dynamicpages-text-view")
        self.assertEqual(config["row_type_icon"], "override-icon")

    def test_complex_widget_hidden_crash(self):
        # Test that widgets like OrderedSelectWidget don't crash the form
        # when they are supposed to be hidden.
        from plone.app.z3cform.interfaces import IPloneFormLayer
        from zope.interface import alsoProvides

        self.row.row_type = "cs_dynamicpages-text-view"  # Hide ICollection fields

        request = self.portal.REQUEST.clone()
        alsoProvides(request, IPloneFormLayer)

        form = RowEditForm(self.row, request)
        form.update()
        # This should trigger the rendering which might crash
        try:
            rendered = form()
            self.assertIn("IRichTextBehavior-text", rendered)
        except Exception as e:
            self.fail(f"Form rendering failed with {type(e).__name__}: {e}")
