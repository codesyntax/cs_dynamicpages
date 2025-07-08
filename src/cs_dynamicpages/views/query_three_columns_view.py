# -*- coding: utf-8 -*-

# from cs_dynamicpages import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IQueryThreeColumnsView(Interface):
    """ Marker Interface for IQueryThreeColumnsView"""


@implementer(IQueryThreeColumnsView)
class QueryThreeColumnsView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('query_three_columns_view.pt')

    def elements(self):
        import pdb; pdb.set_trace(); a=1

