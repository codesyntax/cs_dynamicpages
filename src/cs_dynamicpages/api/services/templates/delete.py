from cs_dynamicpages import _
from cs_dynamicpages.templates import Manager
from plone.app.uuid.utils import uuidToObject
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.i18n import translate
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection


class TemplatesDelete(Service):
    def reply(self):
        body = json_body(self.request)
        uid = body.get("uid")
        if uid is None or not uid.strip():
            self.request.response.setStatus(400)
            return {
                "error": {
                    "type": "Bad Request",
                    "message": translate(_("UID is required"), context=self.request),
                }
            }

        alsoProvides(self.request, IDisableCSRFProtection)
        manager = Manager(self.context)
        result = manager.delete_template(uid)
        if result:
            return self.reply_no_content()

        self.request.response.setStatus(400)
        return {
            "error": {
                "type": "Bad Request",
                "message": translate(_("Content does not exist"), context=self.request),
            }
        }
