from cs_dynamicpages.templates import Manager
from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.publisher.browser import TestRequest

import json
import unittest


class TestTemplatesDeleteAPI(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create a folder to act as the context for our tests
        self.folder = api.content.create(
            container=self.portal, type="Folder", id="test-folder", title="Test Folder"
        )

        # Create some templates in the manager
        self.manager = Manager(self.folder)
        self.template_uid = "some-uuid-1234"
        self.manager.append_template({"uid": self.template_uid, "name": "Template 1"})

    def _make_request(self, payload):
        """Helper to simulate a REST API DELETE request"""
        body = json.dumps(payload).encode("utf-8")
        request = TestRequest(
            environ={"CONTENT_TYPE": "application/json", "REQUEST_METHOD": "DELETE"},
            body=body,
        )
        # Mock request.get("BODY") which is what json_body() uses
        request.form["BODY"] = body
        return request

    def _get_service(self, request):
        from cs_dynamicpages.api.services.templates.delete import TemplatesDelete
        from Products.Five.browser import BrowserView

        class TestTemplatesDelete(TemplatesDelete, BrowserView):
            pass

        return TestTemplatesDelete(self.folder, request)

    def test_delete_template_missing_uid(self):
        """Test DELETE /@templates without UID fails with 400"""
        request = self._make_request({"name": "Template 1"})
        service = self._get_service(request)

        response = service.reply()

        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "UID is required")

    def test_delete_template_not_found(self):
        """Test DELETE /@templates with non-existent template fails with 400"""
        request = self._make_request({"uid": "invalid-uuid"})
        service = self._get_service(request)

        response = service.reply()

        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "Content does not exist")

        # Verify the existing template was not deleted
        self.assertEqual(len(self.manager.get_templates()), 1)

    def test_delete_template_success(self):
        """Test DELETE /@templates successfully deletes a template"""
        request = self._make_request({"uid": self.template_uid})
        service = self._get_service(request)

        service.reply()

        # In Plone tests, we check that status is NO CONTENT (204)
        self.assertEqual(request.response.getStatus(), 204)

        # Verify the template was removed from the Manager
        self.assertEqual(len(self.manager.get_templates()), 0)
