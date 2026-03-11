# from cs_dynamicpages import _
from cs_dynamicpages.templates import Manager
from cs_dynamicpages.utils import get_available_views_for_row
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.uuid.interfaces import IUUID
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from Acquisition import aq_parent
from zope.i18n import translate
from plone.app.uuid.utils import uuidToObject


class IDynamicView(Interface):
    """Marker Interface for IDynamicView"""


@implementer(IDynamicView)
class DynamicView(BrowserView):
    def rows(self):
        dynamic_page_folder = self.dynamic_page_folder_element()
        if dynamic_page_folder:
            return api.content.find(
                portal_type="DynamicPageRow",
                sort_on="getObjPositionInParent",
                context=dynamic_page_folder,
            )
        return []

    def dynamic_page_folder_element(self):
        page_folders = api.content.find(
            portal_type="DynamicPageFolder",
            context=self.context,
            depth=1,
            sort_on="getObjPositionInParent",
        )
        if page_folders:
            return page_folders[0].getObject()
        else:
            if self.can_edit():
                alsoProvides(self.request, IDisableCSRFProtection)
                api.content.create(
                    container=self.context,
                    type="DynamicPageFolder",
                    title="Rows",
                )
                created_elements_find = api.content.find(
                    portal_type="DynamicPageFolder",
                    context=self.context,
                    depth=1,
                    sort_on="getObjPositionInParent",
                )
                created_element = created_elements_find[0].getObject()
                api.content.transition(created_element, transition="publish")
                return created_element

    def dynamic_page_folder_element_url(self):
        dynamic_page_folder = self.dynamic_page_folder_element()
        if dynamic_page_folder:
            return dynamic_page_folder.absolute_url()
        return ""

    def can_edit(self):
        return api.user.has_permission("Modify portal content", obj=self.context)

    def available_views_for_row(self):
        return get_available_views_for_row()

    def normalize_title(self, title):
        return (
            title
            .replace("cs_dynamicpages-", " ")
            .replace("-", " ")
            .replace("_", " ")
            .replace("view", "")
            .lower()
        )

    def available_templates(self):
        portal_types = api.portal.get_tool("portal_types")
        manager = Manager(self.context)
        templates = []
        for template in manager.get_templates():
            obj = uuidToObject(template.get("uid"))
            if obj:
                parent = aq_parent(obj)
                template.update({
                    "Title": parent.Title(),
                    "Description": parent.Description(),
                    "absolute_url": parent.absolute_url(),
                    "portal_type": parent.portal_type,
                    "translated_portal_type": translate(
                        portal_types.get(parent.portal_type).title,
                        domain=portal_types.get(parent.portal_type).i18n_domain,
                        context=self.request,
                    ),
                })
                templates.append(template)
        return templates

    def self_in_templates(self):
        if "rows" in self.context:
            return IUUID(self.context.rows) in [
                template.get("uid") for template in self.available_templates()
            ]
        return False
