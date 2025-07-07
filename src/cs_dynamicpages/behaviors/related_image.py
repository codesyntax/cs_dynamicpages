# -*- coding: utf-8 -*-

from cs_dynamicpages import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.app.z3cform.widgets.contentbrowser import ContentBrowserFieldWidget
from plone.autoform import directives as form


class IRelatedImageMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IRelatedImage(model.Schema):
    """
    """

    related_image = RelationList(
        title="Related Image",
        default=[],
        max_length=1,
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    form.widget(
        "related_image",
        ContentBrowserFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "recentlyUsed": True,
            "selectableTypes": ["Image"],
        },
    )


@implementer(IRelatedImage)
@adapter(IRelatedImageMarker)
class RelatedImage(object):
    def __init__(self, context):
        self.context = context

    @property
    def related_image(self):
        if safe_hasattr(self.context, 'related_image'):
            return self.context.related_image
        return None

    @related_image.setter
    def related_image(self, value):
        self.context.related_image = value
