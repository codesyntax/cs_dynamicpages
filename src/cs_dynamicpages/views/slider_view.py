from cs_dynamicpages.views.base import RowViewBase
from plone import api
from zope.interface import implementer
from zope.interface import Interface


class ISliderView(Interface):
    """Marker Interface for ISliderView"""


@implementer(ISliderView)
class SliderViewBase(RowViewBase):
    def elements(self):
        # Implement your own actions:
        return api.content.find(
            portal_type="DynamicPageRowFeatured",
            context=self.context,
            sort_on="getObjPositionInParent",
        )


class SliderView(SliderViewBase):
    allowed_fields = (
        "IBasic.title",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
        "IFetchPriorityImage.fetchpriority_image",
    )
    has_featured = True
    icon = "images"


class FeaturesView(SliderViewBase):
    allowed_fields = (
        "IBasic.title",
        "IRowWidth.width",
        "IRowColumns.columns",
        "IExtraClass.extra_class",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
        "IFetchPriorityImage.fetchpriority_image",
    )
    has_featured = True
    icon = "grid"


class AccordionView(SliderViewBase):
    allowed_fields = (
        "IBasic.title",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    has_featured = True
    icon = "chevron-double-down"
