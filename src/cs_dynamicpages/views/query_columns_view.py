# from cs_dynamicpages import _
from cs_dynamicpages.views.base import RowViewBase
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import implementer
from zope.interface import Interface


class IQueryColumnsView(Interface):
    """Marker Interface for IQueryColumnsView"""


@implementer(IQueryColumnsView)
class QueryColumnsView(CollectionView, RowViewBase):
    allowed_fields = (
        "IBasic.title",
        "IRowWidth.width",
        "IExtraClass.extra_class",
        "ICollection.query",
        "ICollection.sort_on",
        "ICollection.sort_order",
        "ICollection.betweeen",
        "ICollection.limit",
        "IRowColumns.columns",
        "IRowVerticalSpacing.padding_top",
        "IRowVerticalSpacing.padding_bottom",
        "IRowVerticalSpacing.margin_top",
        "IRowVerticalSpacing.margin_bottom",
        "IFetchPriorityImage.fetchpriority_image",
    )
    icon = "funnel"

    def __call__(self):
        # Implement your own actions:
        return self.index()
