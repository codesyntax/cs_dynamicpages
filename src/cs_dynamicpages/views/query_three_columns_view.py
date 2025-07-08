
# from cs_dynamicpages import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IQueryThreeColumnsView(Interface):
    """Marker Interface for IQueryThreeColumnsView"""


@implementer(IQueryThreeColumnsView)
class QueryThreeColumnsView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('query_three_columns_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
