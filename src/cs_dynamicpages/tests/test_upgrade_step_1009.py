from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UpgradeStep1009IntegrationTest(unittest.TestCase):
    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_upgrade_step_1009_registry_record(self):
        """Test that the registry record is added after upgrade."""

        # Manually run the upgrade step if needed, or just check if it's there
        # if the test layer already has it.
        # Usually, loadMigrationProfile is better in upgrade step handler.

        # Check if record exists
        registry = api.portal.get_tool("portal_registry")
        record_name = (
            "plone.bundles/cs_dynamicpages.dynamicpagerow_add_position.jscompilation"
        )

        # If it doesn't exist, we might need to run the upgrade handler
        # but since GS profiles in tests are usually loaded, it might be there.

        # Let's run the import profile manually to be sure we are testing the
        # configuration
        setup = api.portal.get_tool("portal_setup")
        setup.runImportStepFromProfile(
            "profile-cs_dynamicpages.upgrades:1009", "plone.app.registry"
        )

        self.assertIn(record_name, registry.records)
        self.assertEqual(
            registry.records[record_name].value,
            "++plone++cs_dynamicpages.edit/add-row-position.js",
        )
