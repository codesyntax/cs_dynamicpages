# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from logging import getLogger
from plone import api
log = getLogger(__name__)

# from cs_dynamicpages import _


class IDynamicPageRow(model.Schema):
    """ Marker interface and Dexterity Python Schema for DynamicPageRow
    """
    row_type = schema.Choice(title="Row type",
                               required=True,
                               vocabulary='cs_dynamicpages.RowType',
                               )

@implementer(IDynamicPageRow)
class DynamicPageRow(Container):
    """ Content-type class for IPortadakoLerroa
    """
    def render(self, request):
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
