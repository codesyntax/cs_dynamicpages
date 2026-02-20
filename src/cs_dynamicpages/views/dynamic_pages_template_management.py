from Acquisition import aq_parent
from cs_dynamicpages.templates import Manager
from plone import api
from plone.app.uuid.utils import uuidToObject
from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface


class IDynamicPagesTemplateManagement(Interface):
    """Marker Interface for IDynamicPagesTemplateManagement"""


@implementer(IDynamicPagesTemplateManagement)
class DynamicPagesTemplateManagement(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('dynamic_pages_template_management.pt')

    def available_templates(self):
        portal_types = api.portal.get_tool("portal_types")
        manager = Manager(self.context)
        templates = []
        for template in manager.get_templates():
            obj = uuidToObject(template.get("uid"))
            if obj:
                parent = aq_parent(obj)
                template.update(
                    {
                        "Title": parent.Title(),
                        "Description": parent.Description(),
                        "absolute_url": parent.absolute_url(),
                        "portal_type": parent.portal_type,
                        "translated_portal_type": translate(
                            portal_types.get(parent.portal_type).title,
                            domain=portal_types.get(parent.portal_type).i18n_domain,
                            context=self.request,
                        ),
                    }
                )
                templates.append(template)
        return templates
