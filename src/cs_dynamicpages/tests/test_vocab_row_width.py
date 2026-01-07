from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class RowWidthIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_width_registered(self):
        """Test that RowWidth vocabulary is registered."""
        vocab_name = "cs_dynamicpages.RowWidth"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

    def test_vocab_row_width_returns_tokenized_vocabulary(self):
        """Test that vocabulary returns tokenized vocabulary."""
        vocab_name = "cs_dynamicpages.RowWidth"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

    def test_vocab_row_width_has_terms(self):
        """Test that vocabulary has terms from registry defaults."""
        vocab_name = "cs_dynamicpages.RowWidth"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        # Default registry has terms like "col-md-6 offset-md-3" (Narrow)
        self.assertTrue(len(vocabulary) > 0)

    def test_vocab_row_width_term_structure(self):
        """Test that vocabulary terms have correct structure."""
        vocab_name = "cs_dynamicpages.RowWidth"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        if len(vocabulary) > 0:
            term = list(vocabulary)[0]
            self.assertIsNotNone(term.value)
            self.assertIsNotNone(term.token)
            self.assertIsNotNone(term.title)
