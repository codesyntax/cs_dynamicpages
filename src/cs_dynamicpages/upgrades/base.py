from plone.app.upgrade.utils import loadMigrationProfile


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        "profile-cs_dynamicpages:default",
    )


def upgrade_registry(context, package, version):
    loadMigrationProfile(
        context,
        f"profile-{package}.upgrades:{version}",
    )
