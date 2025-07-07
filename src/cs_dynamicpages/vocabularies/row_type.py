# -*- coding: utf-8 -*-

from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer
from cs_dynamicpages import _
from zope.globalrequest import getRequest
from plone.dexterity.interfaces import IDexterityContent
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getSiteManager
from zope.schema.vocabulary import SimpleTerm
from zope.interface import providedBy
from zope.interface import Interface
class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value

VIEW_PREFIX = "cs_dynamicpages-"

@implementer(IVocabularyFactory)
class RowType(object):
    """
    """
    def __call__(self, context):
        items = []
        terms = []
        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]
        sm = getSiteManager()
        available_views = sm.adapters.lookupAll(
            required=(providedBy(context), providedBy(getRequest())),
            provided=Interface,
        )
        available_view_names = [view[0] for view in available_views if view[0].startswith(VIEW_PREFIX)]
        for view_name in available_view_names:
            items.append(VocabItem(view_name, view_name.replace(VIEW_PREFIX, "")))
        if not available_view_names:
            items.append(VocabItem("cs_dynamicpages-featured-view", "Featured View"))
        for item in items:
            terms.append(
                SimpleTerm(
                    value=item.token,
                    token=str(item.token),
                    title=item.value,
                )
            )
        return SimpleVocabulary(terms)


RowTypeFactory = RowType()