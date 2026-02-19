# -*- coding: utf-8 -*-
from cs_dynamicpages.behaviors.templates import ITemplatesMarker
from cs_dynamicpages.testing import INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class TemplatesIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_templates(self):
        behavior = getUtility(IBehavior, 'cs_dynamicpages.templates')
        self.assertEqual(
            behavior.marker,
            ITemplatesMarker,
        )
