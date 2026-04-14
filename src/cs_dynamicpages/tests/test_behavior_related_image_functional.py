from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import Browser

import transaction
import unittest


class RelatedImageFunctionalTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a document and apply the behavior to be able to test the form
        self.portal.invokeFactory("Document", "doc1", title="Doc 1")
        self.doc1 = self.portal["doc1"]

        # Apply the behavior to Document type
        fti = api.portal.get_tool("portal_types").getTypeInfo("Document")
        behaviors = list(fti.behaviors)
        behaviors.append("cs_dynamicpages.related_image")
        fti.behaviors = tuple(behaviors)

        transaction.commit()

        self.browser = Browser(self.layer["app"])
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization", f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}"
        )

    def test_related_image_pattern_options_in_browser(self):
        # We set the registry record
        api.portal.set_registry_record("plone.image_objects", ["Image", "CustomImage"])
        transaction.commit()

        # Open the edit form of the document
        self.browser.open(self.doc1.absolute_url() + "/edit")

        # The pattern options should be rendered in the HTML for the related_image field
        try:
            self.assertIn("data-pat-contentbrowser", self.browser.contents)
        except AssertionError:
            self.assertIn("data-pat-relateditems", self.browser.contents)

        self.assertIn(
            "&quot;selectableTypes&quot;: [&quot;Image&quot;, &quot;CustomImage&quot;]",
            self.browser.contents,
        )

        # We change the registry record
        api.portal.set_registry_record("plone.image_objects", ["Image"])
        transaction.commit()

        # Open the edit form again
        self.browser.open(self.doc1.absolute_url() + "/edit")

        # The pattern options should be updated
        self.assertIn(
            "&quot;selectableTypes&quot;: [&quot;Image&quot;]", self.browser.contents
        )
