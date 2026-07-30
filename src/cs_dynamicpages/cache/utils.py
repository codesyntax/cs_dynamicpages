from z3c.caching.purge import Purge
from zope.event import notify


def purge_item_from_cache(context):
    """
    Purging a content item is as simple as notifying the Purge event
    See https://pypi.org/project/plone.cachepurging/#user-content-initiating-a-purge-in-code
    """

    notify(Purge(context))
