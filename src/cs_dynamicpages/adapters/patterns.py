"""
See for some context: https://community.plone.org/t/customizing-contentbrowser-pattern-options/22812

this adapter provides dynamic pattern_options to allow selecting any Image-ish
content-type that previously is enabled in the TinyMCE control-panel as an
"image object"

"""

from ..behaviors.related_image import IImageRelationChoice
from plone import api
from plone.app.z3cform.interfaces import IContentBrowserWidget
from z3c.form.interfaces import IValue
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IValue)
@adapter(
    Interface,  # IContentListingMarker in the original
    Interface,  # IRequest in the original
    Interface,  # IForm in the original
    IImageRelationChoice,
    IContentBrowserWidget,
)
class RelatedImageContentbrowserPatternOptions:
    """Adapter class for custon pattern options"""

    def __init__(self, context, request, form, field, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget

    def get(self):

        return {
            "recentlyUsed": True,
            "selectableTypes": api.portal.get_registry_record("plone.image_objects"),
            "upload": True,
        }
