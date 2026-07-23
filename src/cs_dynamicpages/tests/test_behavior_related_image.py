from cs_dynamicpages.behaviors.related_image import IImageRelationList
from cs_dynamicpages.behaviors.related_image import ImageRelationList
from cs_dynamicpages.behaviors.related_image import IRelatedImage
from cs_dynamicpages.behaviors.related_image import IRelatedImageMarker
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class RelatedImageIntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_related_image_registered(self):
        behavior = getUtility(IBehavior, "cs_dynamicpages.related_image")
        self.assertEqual(
            behavior.marker,
            IRelatedImageMarker,
        )

    def test_related_image_field_vocabulary_name(self):
        field = IRelatedImage["related_image"]
        self.assertEqual(
            field.value_type.vocabularyName,
            "cs_dynamicpages.RelatedImageSource",
        )

    def test_related_image_field_max_length(self):
        field = IRelatedImage["related_image"]
        self.assertEqual(field.max_length, 1)

    def test_image_position_field_config(self):
        field = IRelatedImage["image_position"]
        self.assertEqual(field.vocabularyName, "cs_dynamicpages.ImagePosition")
        self.assertEqual(field.default, "left")
        self.assertTrue(field.required)

    def test_image_relation_list_marker(self):
        self.assertTrue(IImageRelationList.providedBy(ImageRelationList()))

    def test_related_image_adapter_getter_setter(self):
        self.portal.invokeFactory("Document", "doc1", title="Doc 1")
        doc = self.portal["doc1"]

        fti = api.portal.get_tool("portal_types").getTypeInfo("Document")
        behaviors = list(fti.behaviors)
        behaviors.append("cs_dynamicpages.related_image")
        fti.behaviors = tuple(behaviors)

        behavior = getUtility(IBehavior, "cs_dynamicpages.related_image")
        adapter = behavior.factory(doc)

        adapter.image_position = "right"
        self.assertEqual(adapter.image_position, "right")
        self.assertEqual(doc.image_position, "right")

        adapter.related_image = []
        self.assertEqual(adapter.related_image, [])
        self.assertEqual(doc.related_image, [])
