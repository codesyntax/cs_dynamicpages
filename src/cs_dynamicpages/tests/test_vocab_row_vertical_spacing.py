from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import unittest


class RowPaddingTopVocabularyIntegrationTest(unittest.TestCase):
    """Integration tests for RowPaddingTop vocabulary."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_padding_top_registered(self):
        """Test that the vocabulary is registered."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowPaddingTop")
        self.assertIsNotNone(factory)

    def test_vocab_row_padding_top_returns_vocabulary(self):
        """Test that the factory returns a SimpleVocabulary."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowPaddingTop")
        vocabulary = factory(self.portal)
        self.assertIsInstance(vocabulary, SimpleVocabulary)


class RowPaddingBottomVocabularyIntegrationTest(unittest.TestCase):
    """Integration tests for RowPaddingBottom vocabulary."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_padding_bottom_registered(self):
        """Test that the vocabulary is registered."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowPaddingBottom")
        self.assertIsNotNone(factory)

    def test_vocab_row_padding_bottom_returns_vocabulary(self):
        """Test that the factory returns a SimpleVocabulary."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowPaddingBottom")
        vocabulary = factory(self.portal)
        self.assertIsInstance(vocabulary, SimpleVocabulary)


class RowMarginTopVocabularyIntegrationTest(unittest.TestCase):
    """Integration tests for RowMarginTop vocabulary."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_margin_top_registered(self):
        """Test that the vocabulary is registered."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowMarginTop")
        self.assertIsNotNone(factory)

    def test_vocab_row_margin_top_returns_vocabulary(self):
        """Test that the factory returns a SimpleVocabulary."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowMarginTop")
        vocabulary = factory(self.portal)
        self.assertIsInstance(vocabulary, SimpleVocabulary)


class RowMarginBottomVocabularyIntegrationTest(unittest.TestCase):
    """Integration tests for RowMarginBottom vocabulary."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_row_margin_bottom_registered(self):
        """Test that the vocabulary is registered."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowMarginBottom")
        self.assertIsNotNone(factory)

    def test_vocab_row_margin_bottom_returns_vocabulary(self):
        """Test that the factory returns a SimpleVocabulary."""
        factory = getUtility(IVocabularyFactory, "cs_dynamicpages.RowMarginBottom")
        vocabulary = factory(self.portal)
        self.assertIsInstance(vocabulary, SimpleVocabulary)
