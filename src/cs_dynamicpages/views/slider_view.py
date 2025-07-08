# from cs_dynamicpages import _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ISliderView(Interface):
    """Marker Interface for ISliderView"""


@implementer(ISliderView)
class SliderView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('slider_view.pt')

    def elements(self):
        # Implement your own actions:
        return api.content.find(
            portal_type="DynamicPageRowFeatured",
            context=self.context,
            sort_on="getObjPositionInParent",
        )
