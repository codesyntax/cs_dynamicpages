
# from cs_dynamicpages import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFeaturedView(Interface):
    """Marker Interface for IFeaturedView"""


@implementer(IFeaturedView)
class FeaturedView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('featured_view.pt')

    def related_image(self):
        related_image = self.context.related_image
        if related_image:
            return related_image[0].to_object
        return None
