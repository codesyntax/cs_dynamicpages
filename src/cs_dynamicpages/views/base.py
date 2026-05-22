from cs_dynamicpages.interfaces import IRowTypeMetadata
from Products.Five.browser import BrowserView
from zope.interface import implementer


@implementer(IRowTypeMetadata)
class RowViewBase(BrowserView):
    allowed_fields = ()
    has_featured = False
    icon = "bricks"

    def __call__(self):
        return self.index()
