from .utils import purge_item_from_cache
from Acquisition import aq_parent


def purge(context, event):
    """We are in a DynamicPageRow object, we need to go up in the content tree
    and find the container where we are being shown, and signal
    that it should be purged
    """
    # First of all, purge ourself
    purge_item_from_cache(context)

    # Now get our parent and check whether it is a DynamicPageFolder
    parent = aq_parent(context)
    if parent.portal_type == "DynamicPageFolder":
        # So purge the parent too
        purge_item_from_cache(parent)

        # Now check our grand parent
        grand_parent = aq_parent(parent)

        # How can we identify that it is using a DynamicView?
        # we can't, but if someone is modifying a content inside it
        # we could presume that it is, so let's purge it also
        purge_item_from_cache(grand_parent)
