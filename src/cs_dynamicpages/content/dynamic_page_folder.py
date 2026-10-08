from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDynamicPageFolder(model.Schema):
    """Marker interface and Dexterity Python Schema for DynamicPageFolder"""


@implementer(IDynamicPageFolder)
class DynamicPageFolder(Container):
    """Content-type class for IDynamicPageFolder"""
