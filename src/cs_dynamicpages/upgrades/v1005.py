from . import logger
from .base import reload_gs_profile
from plone import api


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade (Python): Remove unneeded behaviors")

    registry_values = api.portal.get_registry_record(
        "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
    )
    new_registry_values = []
    for registry_value in registry_values:
        if not registry_value.get("row_type_icon"):
            registry_value["row_type_icon"] = "bricks"
        new_registry_values.append(registry_value)
    api.portal.set_registry_record(
        "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields",
        new_registry_values,
    )
