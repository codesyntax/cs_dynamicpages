# from cs_dynamicpages import _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IDynamicView(Interface):
    """Marker Interface for IDynamicView"""


@implementer(IDynamicView)
class DynamicView(BrowserView):
    def features(self):
        dynamic_page_folder = api.content.find(
            portal_type="DynamicPageFolder", context=self.context
        )
        if dynamic_page_folder:
            return api.content.find(
                portal_type="DynamicPageRow",
                sort_on="getObjPositionInParent",
                context=dynamic_page_folder[0].getObject(),
            )
        return []
