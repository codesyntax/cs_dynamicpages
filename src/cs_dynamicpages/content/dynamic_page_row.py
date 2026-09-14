# from plone.app.textfield import RichText
# from plone.autoform import directives
from cs_dynamicpages.utils import absolute_target_url
from logging import getLogger
from plone import api
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


log = getLogger(__name__)

# from cs_dynamicpages import _


class IDynamicPageRow(model.Schema):
    """Marker interface and Dexterity Python Schema for DynamicPageRow"""

    row_type = schema.Choice(
        title="Row type",
        required=True,
        default="cs_dynamicpages-horizontal-rule-view",
        vocabulary="cs_dynamicpages.RowType",
    )


@implementer(IDynamicPageRow)
class DynamicPageRow(Container):
    """Content-type class for IPortadakoLerroa"""

    def row_template(self):
        return self.row_type.replace("cs_dynamicpages-", "")

    def review_state(self):
        return api.content.get_state(obj=self)

    def can_edit(self):
        return api.user.has_permission("Modify portal content", obj=self)

    def nested_rows(self):
        return api.content.find(
            context=self,
            portal_type="DynamicPageRow",
            sort_on="getObjPositionInParent",
            depth=1,
        )

    def show_add_child_button(self):
        row_type = self.row_type
        row_type_fields = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        )
        for row_type_field in row_type_fields:
            if row_type_field["row_type"] == row_type:
                return row_type_field["row_type_allows_children"]
        return False

    def render(self, request):
        if not hasattr(request, "render_stack"):
            request.render_stack = set()

        if self.UID() in request.render_stack:
            log.error(
                f"Circular reference detected rendering row {self.absolute_url()}"
            )
            return "CIRCULAR REFERENCE DETECTED"

        request.render_stack.add(self.UID())
        try:
            if self.row_type:
                try:
                    view = api.content.get_view(
                        name=self.row_type,
                        context=self,
                        request=request,
                    )
                    return view()
                except Exception as e:
                    log.error(e)
                    return "ERROR RENDERING THE SELECTED ROW TYPE"
            return "THE SELECTED ROW TYPE IS NO LONGER AVAILABLE"
        finally:
            request.render_stack.remove(self.UID())

    def url(self):
        """Returns the url with link variables replaced."""
        if not self.link_url:
            return ""
        url = replace_link_variables_by_paths(self, self.link_url.strip())
        return absolute_target_url(url)

    def related_image_object(self):
        related_image = getattr(self, "related_image", None)
        if related_image:
            return related_image[0].to_object
        return None
