import unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING


class TestHowToConfigureRegistry(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_configure_row_widths(self):
        """Test adding a custom row width to the registry."""
        from plone import api

        record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_widths"
        current_widths = list(api.portal.get_registry_record(record_name))

        new_width = {
            "row_width_label": "Extra Narrow",
            "row_width_class": "col-md-4 offset-md-4",
        }

        current_widths.append(new_width)
        api.portal.set_registry_record(record_name, current_widths)

        # Verify it was added
        updated_widths = api.portal.get_registry_record(record_name)
        self.assertEqual(updated_widths[-1]["row_width_label"], "Extra Narrow")
        self.assertEqual(updated_widths[-1]["row_width_class"], "col-md-4 offset-md-4")

        # Test vocabulary behavior
        from zope.schema.interfaces import IVocabularyFactory
        from zope.component import getUtility

        vocab_factory = getUtility(IVocabularyFactory, name="cs_dynamicpages.RowWidth")
        vocab = vocab_factory(self.portal)

        # Check that the new width is in the vocabulary
        self.assertIn("col-md-4 offset-md-4", [term.value for term in vocab])

    def test_configure_spacers(self):
        """Test modifying spacers in the registry (e.g., Tailwind classes)."""
        from plone import api

        record_name = "cs_dynamicpages.dynamic_pages_control_panel.spacer_padding_top"
        current_spacers = list(api.portal.get_registry_record(record_name))

        new_spacer = {
            "spacer_label": "Large (Tailwind)",
            "spacer_class": "pt-12",
        }

        current_spacers.append(new_spacer)
        api.portal.set_registry_record(record_name, current_spacers)

        # Verify it was added
        updated_spacers = api.portal.get_registry_record(record_name)
        self.assertEqual(updated_spacers[-1]["spacer_label"], "Large (Tailwind)")
        self.assertEqual(updated_spacers[-1]["spacer_class"], "pt-12")

        # Test vocabulary behavior
        from zope.schema.interfaces import IVocabularyFactory
        from zope.component import getUtility

        vocab_factory = getUtility(
            IVocabularyFactory, name="cs_dynamicpages.RowPaddingTop"
        )
        vocab = vocab_factory(self.portal)

        # Check that the new spacer is in the vocabulary
        self.assertIn("pt-12", [term.value for term in vocab])
