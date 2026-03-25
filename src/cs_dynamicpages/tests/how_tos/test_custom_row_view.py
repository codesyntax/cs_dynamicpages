import unittest
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from cs_dynamicpages.controlpanels.dynamic_pages_control_panel.controlpanel import (
    IDynamicPagesControlPanel,
)


class TestHowToCustomRowView(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a dynamic page folder and row
        self.portal.invokeFactory("DynamicPageFolder", "page1", title="Page 1")
        self.page = self.portal["page1"]
        self.page.invokeFactory("DynamicPageRow", "row1", title="Row 1")
        self.row = self.page["row1"]

    def test_add_custom_row_view_to_registry(self):
        """Test step 3 from custom-row-view.md how-to."""
        from plone import api

        # This is the dict we want to add to the registry according to the docs
        new_row_type = {
            "row_type": "cs_dynamicpages-myaddon-video-embed-view",
            "row_type_icon": "play-btn",
            "row_type_has_featured_add_button": False,
            "each_row_type_fields": [
                "IBasic.title",
                "IBasic.description",
                "IRichTextBehavior-text",
                "IRowWidth.width",
                "IExtraClass.extra_class",
                "IRowVerticalSpacing.padding_top",
                "IRowVerticalSpacing.padding_bottom",
                "IRowVerticalSpacing.margin_top",
                "IRowVerticalSpacing.margin_bottom",
            ],
        }

        # To make schema validation pass during test, we need to register a dummy view adapter
        # so the vocabulary finds it when checking the 'row_type' value constraints
        from zope.component import getSiteManager
        from zope.interface import Interface
        from zope.publisher.interfaces.browser import IBrowserRequest
        from cs_dynamicpages.content.dynamic_page_row import IDynamicPageRow

        class DummyView:
            pass

        sm = getSiteManager()
        sm.registerAdapter(
            DummyView,
            (IDynamicPageRow, IBrowserRequest),
            Interface,
            name="cs_dynamicpages-myaddon-video-embed-view",
        )

        # Append it to the existing record using plone.api
        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        current_rows = list(api.portal.get_registry_record(record_name))
        current_rows.append(new_row_type)
        api.portal.set_registry_record(record_name, current_rows)

        # Verify it was added
        updated_rows = api.portal.get_registry_record(record_name)
        self.assertEqual(
            updated_rows[-1]["row_type"], "cs_dynamicpages-myaddon-video-embed-view"
        )
        self.assertEqual(updated_rows[-1]["row_type_icon"], "play-btn")
        self.assertFalse(updated_rows[-1]["row_type_has_featured_add_button"])

        # Test vocabulary behavior
        from zope.schema.interfaces import IVocabularyFactory
        from zope.component import getUtility

        vocab_factory = getUtility(IVocabularyFactory, name="cs_dynamicpages.RowType")
        vocab = vocab_factory(self.portal)

        # Check that the new row type is in the vocabulary
        self.assertIn(
            "cs_dynamicpages-myaddon-video-embed-view", [term.value for term in vocab]
        )
