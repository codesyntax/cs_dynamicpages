from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class RowColumnsIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_columns_registered(self):
        """Test that RowColumns vocabulary is registered."""
        vocab_name = "cs_dynamicpages.RowColumns"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

    def test_vocab_row_columns_returns_tokenized_vocabulary(self):
        """Test that vocabulary returns tokenized vocabulary."""
        vocab_name = "cs_dynamicpages.RowColumns"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

    def test_vocab_row_columns_has_four_terms(self):
        """Test that vocabulary has 4 column options."""
        vocab_name = "cs_dynamicpages.RowColumns"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertEqual(len(vocabulary), 4)

    def test_vocab_row_columns_contains_expected_values(self):
        """Test that vocabulary contains expected column values."""
        vocab_name = "cs_dynamicpages.RowColumns"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        values = [term.value for term in vocabulary]
        self.assertIn("col-md-12", values)
        self.assertIn("col-md-6", values)
        self.assertIn("col-md-4", values)
        self.assertIn("col-md-3", values)
