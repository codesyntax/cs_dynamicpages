from cs_dynamicpages.upgrades.base import upgrade_registry


def upgrade(context):
    upgrade_registry(context, "cs_dynamicpages", "1009")
