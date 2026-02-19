# -*- coding: utf-8 -*-

from cs_dynamicpages import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
import json


class ITemplatesMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ITemplates(model.Schema):
    """ """

    templates = schema.JSONField(
        title=_(
            "",
        ),
        description=_(
            "",
        ),
        schema=json.dumps({}),
        default={"templates": []},
        required=False,
        readonly=False,
    )


@implementer(ITemplates)
@adapter(ITemplatesMarker)
class Templates:
    def __init__(self, context):
        self.context = context

    @property
    def templates(self):
        if safe_hasattr(self.context, "templates"):
            return self.context.templates
        return None

    @templates.setter
    def templates(self, value):
        self.context.templates = value
