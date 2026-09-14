# from cs_dynamicpages import _
from cs_dynamicpages.views.dynamic_page_row_view import DynamicPageRowView
from plone import api
from zope.interface import implementer
from zope.interface import Interface


class ISliderView(Interface):
    """Marker Interface for ISliderView"""


@implementer(ISliderView)
class SliderView(DynamicPageRowView):
    def elements(self):
        return api.content.find(
            portal_type="DynamicPageRow",
            context=self.context,
            sort_on="getObjPositionInParent",
            depth=1,
        )


class AccordionView(DynamicPageRowView):
    def elements(self):
        return api.content.find(
            portal_type="DynamicPageRow",
            context=self.context,
            sort_on="getObjPositionInParent",
            depth=1,
        )


class FeaturesView(DynamicPageRowView):
    def elements(self):
        return api.content.find(
            portal_type="DynamicPageRow",
            context=self.context,
            sort_on="getObjPositionInParent",
            depth=1,
        )
