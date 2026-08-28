from cs_dynamicpages.testing import FUNCTIONAL_TESTING
from cs_dynamicpages.testing import INTEGRATION_TESTING
from cs_dynamicpages.views.row_type_control_panel_view import IRowTypeControlPanelView
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

    def test_row_type_control_panel_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='row-type-control-panel-view'
        )
        self.assertTrue(IRowTypeControlPanelView.providedBy(view))

    def test_row_type_control_panel_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='row-type-control-panel-view'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IRowTypeControlPanelView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
