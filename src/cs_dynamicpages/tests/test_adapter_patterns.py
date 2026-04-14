from cs_dynamicpages.adapters.patterns import RelatedImageContentbrowserPatternOptions
from cs_dynamicpages.behaviors.related_image import IImageRelationList
from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


try:
    from plone.app.z3cform.interfaces import IContentBrowserWidget
except ImportError:
    from plone.app.z3cform.interfaces import (
        IRelatedItemsWidget as IContentBrowserWidget,
    )

from z3c.form.interfaces import IValue
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

import unittest


@implementer(Interface)
class DummyContext:
    pass


@implementer(Interface)
class DummyRequest:
    pass


@implementer(Interface)
class DummyForm:
    pass


@implementer(IImageRelationList)
class DummyField:
    pass


@implementer(IContentBrowserWidget)
class DummyWidget:
    pass


class RelatedImageContentbrowserPatternOptionsTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_adapter_registration(self):
        context = DummyContext()
        request = DummyRequest()
        form = DummyForm()
        field = DummyField()
        widget = DummyWidget()

        adapter = getMultiAdapter(
            (context, request, form, field, widget), IValue, name="pattern_options"
        )
        self.assertIsInstance(adapter, RelatedImageContentbrowserPatternOptions)

    def test_adapter_get(self):
        context = DummyContext()
        request = DummyRequest()
        form = DummyForm()
        field = DummyField()
        widget = DummyWidget()

        adapter = getMultiAdapter(
            (context, request, form, field, widget), IValue, name="pattern_options"
        )

        api.portal.set_registry_record("plone.image_objects", ["Image"])
        self.assertEqual(
            adapter.get(),
            {
                "recentlyUsed": True,
                "selectableTypes": ["Image"],
                "upload": True,
            },
        )

        api.portal.set_registry_record("plone.image_objects", ["Image", "CustomImage"])
        self.assertEqual(
            adapter.get(),
            {
                "recentlyUsed": True,
                "selectableTypes": ["Image", "CustomImage"],
                "upload": True,
            },
        )
