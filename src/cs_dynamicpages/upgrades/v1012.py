from . import logger
from plone import api
from zope.globalrequest import getRequest


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade (Python): Add new index to catalog")
    catalog = api.portal.get_tool("portal_catalog")
    catalog.reindexIndex(["row_type"], REQUEST=getRequest())
    logger.info("New index `row_type` reindexed")
