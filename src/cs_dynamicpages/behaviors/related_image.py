from plone.app.z3cform.widgets.contentbrowser import ContentBrowserFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope import schema

class IRelatedImageMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IRelatedImage(model.Schema):
    """ """

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
            "upload": True,
        },
    )
    image_position = schema.Choice(
        title="Image Position",
        vocabulary="cs_dynamicpages.ImagePosition",
        required=True,
        default="left",
    )


@implementer(IRelatedImage)
@adapter(IRelatedImageMarker)
class RelatedImage:
    def __init__(self, context):
        self.context = context

    @property
    def related_image(self):
        if safe_hasattr(self.context, "related_image"):
            return self.context.related_image
        return None

    @related_image.setter
    def related_image(self, value):
        self.context.related_image = value

    @property
    def image_position(self):
        if safe_hasattr(self.context, "image_position"):
            return self.context.image_position
        return None

    @image_position.setter
    def image_position(self, value):
        self.context.image_position = value