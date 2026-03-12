from cs_dynamicpages.templates import Manager
from cs_dynamicpages.testing import CS_DYNAMICPAGES_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.publisher.browser import TestRequest

import json
import unittest


class TestApplyTemplatePostAPI(unittest.TestCase):
    layer = CS_DYNAMICPAGES_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # In order to allow copying a DynamicPageFolder into another,
        # we must ensure the FTI of the target allows it, or use a Folder
        # instead of a DynamicPageFolder for the target since Plone allows
        # anything inside a regular Folder by default.
        self.target_folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="target-folder",
            title="Target Folder",
        )

        self.source_folder = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="source-folder",
            title="Source Folder",
        )
        self.source_uid = self.source_folder.UID()

        # Register the template in the manager
        self.manager = Manager(self.target_folder)
        self.manager.append_template({
            "uid": self.source_uid,
            "name": "Source Template",
        })

    def _make_request(self, payload):
        """Helper to simulate a REST API POST request"""
        body = json.dumps(payload).encode("utf-8")
        request = TestRequest(
            environ={"CONTENT_TYPE": "application/json", "REQUEST_METHOD": "POST"},
            body=body,
        )
        # Mock request.get("BODY") which is what json_body() uses
        request.form["BODY"] = body
        return request

    def _get_service(self, request):
        from cs_dynamicpages.api.services.apply_template.post import ApplyTemplatePost
        from Products.Five.browser import BrowserView

        class TestApplyTemplatePost(ApplyTemplatePost, BrowserView):
            pass

        return TestApplyTemplatePost(self.target_folder, request)

    def test_apply_template_missing_uid(self):
        """Test POST /@apply-template without UID fails with 400"""
        request = self._make_request({})
        service = self._get_service(request)

        response = service.reply()

        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "UID is required")

    def test_apply_template_invalid_uid_format(self):
        """Test POST /@apply-template with template not in registry fails with 400"""
        request = self._make_request({"uid": "not-registered-uid"})
        service = self._get_service(request)

        response = service.reply()

        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "Template name is not valid")

    def test_apply_template_deleted_source(self):
        """Test POST /@apply-template when source was deleted but registry has it"""
        # Delete the source object so uuidToObject returns None
        api.content.delete(self.source_folder)

        request = self._make_request({"uid": self.source_uid})
        service = self._get_service(request)

        response = service.reply()

        self.assertEqual(request.response.getStatus(), 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"]["type"], "Bad Request")
        self.assertEqual(response["error"]["message"], "Content does not exist")

    def test_apply_template_success(self):
        """Test POST /@apply-template successfully applies the template"""
        request = self._make_request({"uid": self.source_uid})
        service = self._get_service(request)

        service.reply()

        self.assertEqual(request.response.getStatus(), 204)

        # The target folder should now have a copy of the source folder content inside
        self.assertTrue(len(self.target_folder.objectIds()) > 0)

    def test_apply_template_with_existing_rows(self):
        """Test POST /@apply-template overwrites existing 'rows' object"""
        # Note: applying a template deletes target_folder["rows"] if it exists
        # To test this we need target_folder to allow creating an object named 'rows'
        # Regular folders allow it.
        api.content.create(
            container=self.target_folder,
            type="DynamicPageFolder",
            id="rows",
            title="Old Rows",
        )
        old_rows_uid = self.target_folder["rows"].UID()

        request = self._make_request({"uid": self.source_uid})
        service = self._get_service(request)

        service.reply()

        self.assertEqual(request.response.getStatus(), 204)

        self.assertTrue(len(self.target_folder.objectIds()) > 0)
        if "rows" in self.target_folder.objectIds():
            self.assertNotEqual(self.target_folder["rows"].UID(), old_rows_uid)
