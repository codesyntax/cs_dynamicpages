from cs_dynamicpages.content.dynamic_page_row import IDynamicPageRow
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer


@indexer(IDexterityContent)
def dummy(obj):
    """Dummy to prevent indexing other objects thru acquisition"""
    raise AttributeError("This field should not indexed here!")


@indexer(IDynamicPageRow)  # ADJUST THIS!
def row_type_index(obj):
    """Calculate and return the value for the indexer"""
    return obj.row_type
