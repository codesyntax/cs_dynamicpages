# -*- coding: utf-8 -*-
from cs_dynamicpages.testing import FUNCTIONAL_TESTING
from cs_dynamicpages.testing import INTEGRATION_TESTING
from cs_dynamicpages.views.dynamic_pages_template_management import IDynamicPagesTemplateManagement
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_dynamic_pages_template_management_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='dynamic-pages-template-management'
        )
        self.assertTrue(IDynamicPagesTemplateManagement.providedBy(view))

    def test_dynamic_pages_template_management_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='dynamic-pages-template-management'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IDynamicPagesTemplateManagement.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
