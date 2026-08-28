from plone import api
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


class IRowTypeControlPanelView(Interface):
    """Marker Interface for IRowTypeControlPanelView"""


@implementer(IRowTypeControlPanelView)
class RowTypeControlPanelView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('row_type_control_panel_view.pt')

    def row_types(self):
        vocabulary = getUtility(IVocabularyFactory, name="cs_dynamicpages.RowType")
        values = vocabulary(self.context)

        def expand_item(item):
            breadcrumbs_view = api.content.get_view(
                context=item.getObject().aq_parent.aq_parent, name="breadcrumbs_view"
            )
            dynamic_page = item.getObject().aq_parent.aq_parent
            return {
                "absolute_url": item.getURL(),
                "title": dynamic_page.Title(),
                "breadcrumbs": breadcrumbs_view.breadcrumbs(),
                "item": dynamic_page,
            }

        def term_to_dict(term):
            items = api.content.find(row_type=term.value, portal_type="DynamicPageRow")
            return {
                "title": term.title,
                "token": term.token,
                "value": term.value,
                "used_in": [expand_item(item) for item in items],
                "count": len(items),
            }

        return sorted(
            [term_to_dict(item) for item in values],
            key=lambda item: item.get("title").lower(),
        )

    def navroot(self, item):
        """get the navigation root of a given item"""
        return api.portal.get_navigation_root(context=item)
