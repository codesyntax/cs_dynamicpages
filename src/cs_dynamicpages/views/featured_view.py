from cs_dynamicpages.views.base import RowViewBase
from zope.interface import implementer
from zope.interface import Interface


class IFeaturedView(Interface):
    """Marker Interface for IFeaturedView"""


@implementer(IFeaturedView)
class FeaturedView(RowViewBase):
    def related_image(self):
        related_image = getattr(self.context, "related_image", None)
        if related_image:
            return related_image[0].to_object
        return None


class TitleDescriptionView(RowViewBase):
    allowed_fields = (
        "IBasic.title",
        "IBasic.description",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    icon = "fonts"


class FeaturedViewDefault(FeaturedView):
    allowed_fields = (
        "IBasic.title",
        "IBasic.description",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRelatedImage.related_image",
        "IFetchPriorityImage.fetchpriority_image",
        "IRelatedImage.image_position",
        "ILinkInfo.link_text",
        "ILinkInfo.link_url",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    icon = "card-image"


class FeaturedOverlayView(FeaturedView):
    allowed_fields = (
        "IBasic.title",
        "IBasic.description",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRelatedImage.related_image",
        "IFetchPriorityImage.fetchpriority_image",
        "ILinkInfo.link_text",
        "ILinkInfo.link_url",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    icon = "image-fill"


class HorizontalRuleView(RowViewBase):
    allowed_fields = (
        "IBasic.title",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    icon = "hr"


class SpacerView(RowViewBase):
    allowed_fields = (
        "IBasic.title",
        "IExtraClass.extra_class",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    icon = "arrows-vertical"


class TextView(RowViewBase):
    allowed_fields = (
        "IBasic.title",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "IRichTextBehavior-text",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
    )
    icon = "body-text"
