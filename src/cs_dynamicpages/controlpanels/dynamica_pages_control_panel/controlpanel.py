# -*- coding: utf-8 -*-
from cs_dynamicpages import _
from cs_dynamicpages.interfaces import IBrowserLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface
from zope import schema

class IDynamicaPagesControlPanel(Interface):
    myfield_name = schema.TextLine(
        title=_(
            "This is an example field for this control panel",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
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
