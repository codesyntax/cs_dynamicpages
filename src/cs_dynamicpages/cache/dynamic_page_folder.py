from .utils import purge_item_from_cache
from Acquisition import aq_parent


def purge(context, event):
    """We are in a DynamicPageFolder object, we need to go up in the content tree
    and find the container where we are being shown, and signal
    that it should be purged
    """
    # First of all, purge ourself
    purge_item_from_cache(context)

    # Now get our parent and purge it
    # we could presume that it is using a dynamic-view
    parent = aq_parent(context)
    purge_item_from_cache(parent)
