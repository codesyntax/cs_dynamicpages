from cs_dynamicpages import _
from cs_dynamicpages.interfaces import IBrowserLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform.directives import widget

class IRowTypeFieldsSchema(Interface):
    row_type = schema.Choice(
        title="Row type",
        required=True,
        vocabulary="cs_dynamicpages.RowType",
    )

    each_row_type_fields = schema.List(
        title="Row type fields",
        required=True,
        value_type=schema.TextLine(),
        default=[],
    )


class IDynamicaPagesControlPanel(Interface):
    widget(row_type_fields=DataGridFieldFactory)
    row_type_fields = schema.List(
        title=u"Row Type Fields",
        required=True,
        value_type=DictRow(title=u"Row Type Fields", schema=IRowTypeFieldsSchema),
        default=[
            {
                "row_type": "cs_dynamicpages-featured-view",
                "each_row_type_fields": ["IBasic.title", "IBasic.description", "IRelatedImage.image", "ILinkInfo.link_text", "ILinkInfo.link_url"],
            }
        ],
    )


class DynamicaPagesControlPanel(RegistryEditForm):
    schema = IDynamicaPagesControlPanel
    schema_prefix = "cs_dynamicpages.dynamica_pages_control_panel"
    label = _("Dynamica Pages Control Panel")


DynamicaPagesControlPanelView = layout.wrap_form(
    DynamicaPagesControlPanel, ControlPanelFormWrapper
)


@adapter(Interface, IBrowserLayer)
class DynamicaPagesControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IDynamicaPagesControlPanel
    configlet_id = "dynamica_pages_control_panel-controlpanel"
    configlet_category_id = "Products"
    title = _("Dynamica Pages Control Panel")
    group = ""
    schema_prefix = "cs_dynamicpages.dynamica_pages_control_panel"
