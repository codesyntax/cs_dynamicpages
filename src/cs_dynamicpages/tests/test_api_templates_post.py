import json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from cs_dynamicpages.templates import Manager
from zope.publisher.browser import TestRequest

import unittest


class TestTemplatesPostAPI(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        # Create a folder to act as the context for our tests
        self.folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder",
            title="Test Folder"
        )
        
        # Create a source content to act as the template
        self.source_content = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="source-content",
            title="Source Content"
        )
        self.source_uid = self.source_content.UID()
        
    def _make_request(self, payload):
        """Helper to simulate a REST API POST request"""
        body = json.dumps(payload).encode("utf-8")
        request = TestRequest(
            environ={"CONTENT_TYPE": "application/json", "REQUEST_METHOD": "POST"},
            body=body
        )
        # Mock request.get("BODY") which is what json_body() uses
        request.form["BODY"] = body
        return request

    def _get_service(self, request):
        from cs_dynamicpages.api.services.templates.post import TemplatesPost
        from Products.Five.browser import BrowserView
        class TestTemplatesPost(TemplatesPost, BrowserView):
            pass
        return TestTemplatesPost(self.folder, request)

    def test_post_template_missing_uid(self):
        """Test POST /@templates without UID fails with 400"""
        request = self._make_request({"name": "My Template"})
        service = self._get_service(request)
        
        response = service.reply()
        
        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "UID is required")

    def test_post_template_invalid_uid(self):
        """Test POST /@templates with non-existent UID fails with 400"""
        request = self._make_request({"uid": "invalid-uuid", "name": "My Template"})
        service = self._get_service(request)
        
        response = service.reply()
        
        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "Content does not exist")

    def test_post_template_success(self):
        """Test POST /@templates successfully creates a template"""
        request = self._make_request({"uid": self.source_uid, "name": "My Template"})
        service = self._get_service(request)
        
        service.reply()
        self.assertEqual(request.response.getStatus(), 204)
        
        # Verify the template was added to the Manager
        manager = Manager(self.folder)
        templates = manager.get_templates()
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0]["uid"], self.source_uid)
        self.assertEqual(templates[0]["name"], "My Template")

    def test_post_template_without_name(self):
        """Test POST /@templates uses UID as name if name is missing"""
        request = self._make_request({"uid": self.source_uid})
        service = self._get_service(request)
        
        service.reply()
        self.assertEqual(request.response.getStatus(), 204)
        
        # Verify the template was added with UID as name
        manager = Manager(self.folder)
        templates = manager.get_templates()
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0]["name"], self.source_uid)

