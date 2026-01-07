from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class ImagePositionIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_image_position_registered(self):
        """Test that ImagePosition vocabulary is registered."""
        vocab_name = "cs_dynamicpages.ImagePosition"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

    def test_vocab_image_position_returns_tokenized_vocabulary(self):
        """Test that vocabulary returns tokenized vocabulary."""
        vocab_name = "cs_dynamicpages.ImagePosition"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

    def test_vocab_image_position_has_two_terms(self):
        """Test that vocabulary has 2 position options."""
        vocab_name = "cs_dynamicpages.ImagePosition"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        self.assertEqual(len(vocabulary), 2)

    def test_vocab_image_position_contains_left_and_right(self):
        """Test that vocabulary contains left and right values."""
        vocab_name = "cs_dynamicpages.ImagePosition"
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.portal)
        values = [term.value for term in vocabulary]
        self.assertIn("left", values)
        self.assertIn("right", values)
