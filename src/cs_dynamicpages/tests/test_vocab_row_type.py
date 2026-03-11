from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class RowTypeIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_type_registered(self):
        """Test that RowType vocabulary is registered."""
        vocab_name = "cs_dynamicpages.RowType"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

    def test_vocab_row_type_returns_tokenized_vocabulary(self):
        """Test that vocabulary returns tokenized vocabulary."""
        vocab_name = "cs_dynamicpages.RowType"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

    def test_vocab_row_type_has_terms(self):
        """Test that vocabulary has row type terms."""
        vocab_name = "cs_dynamicpages.RowType"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertTrue(len(vocabulary) > 0)

    def test_vocab_row_type_terms_start_with_prefix(self):
        """Test that all row type terms start with cs_dynamicpages- prefix."""
        vocab_name = "cs_dynamicpages.RowType"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        for term in vocabulary:
            self.assertTrue(
                term.value.startswith("cs_dynamicpages-"),
                f"Term {term.value} does not start with cs_dynamicpages-",
            )
