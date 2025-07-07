# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer


# from cs_dynamicpages import _


class IDynamicPageRow(model.Schema):
    """ Marker interface and Dexterity Python Schema for DynamicPageRow
    """
    row_type = schema.Choice(title="Row type",
                               required=True,
                               vocabulary='cs_dynamicpages.RowType',
                               )


@implementer(IDynamicPageRow)
class DynamicPageRow(Item):
    """ Content-type class for IDynamicPageRow
    """