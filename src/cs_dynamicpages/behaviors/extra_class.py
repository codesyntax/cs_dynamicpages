from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class IExtraClassMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IExtraClass(model.Schema):
    """ """

    extra_class = schema.TextLine(
        title="Extra class for row",
        required=False,
    )


@implementer(IExtraClass)
@adapter(IExtraClassMarker)
class ExtraClass:
    def __init__(self, context):
        self.context = context

    @property
    def extra_class(self):
        if safe_hasattr(self.context, "extra_class"):
            return self.context.extra_class
        return None

    @extra_class.setter
    def extra_class(self, value):
        self.context.extra_class = value
