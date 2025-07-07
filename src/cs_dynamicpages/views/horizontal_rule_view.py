# -*- coding: utf-8 -*-

# from cs_dynamicpages import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IHorizontalRuleView(Interface):
    """ Marker Interface for IHorizontalRuleView"""


@implementer(IHorizontalRuleView)
class HorizontalRuleView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('horizontal_rule_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
