from .dynamic_page_row import purge as purge_dynamic_page_row
from .utils import purge_item_from_cache
from Acquisition import aq_parent


def purge(context, event):
    """We are in a DynamicPageRowFeatured object, we need to go up in the content tree
    and find the container where we are being shown, and signal
    that it should be purged
    """
    # First of all, purge ourself
    purge_item_from_cache(context)

    # Now get our parent and check whether it is a DynamicPageRow
    parent = aq_parent(context)

    if parent.portal_type == "DynamicPageRow":
        # We already know how to purge DynamicPageRow objects
        purge_dynamic_page_row(parent, event)
