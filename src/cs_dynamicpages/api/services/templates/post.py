from cs_dynamicpages import _
from cs_dynamicpages.templates import Manager
from plone.app.uuid.utils import uuidToObject
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.i18n import translate
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection


class TemplatesPost(Service):
    def reply(self):
        body = json_body(self.request)
        uid = body.get("uid")
        name = body.get("name") or uid
        if uid is None or not uid.strip():
            self.request.response.setStatus(400)
            return {
                "error": {
                    "type": "Bad Request",
                    "message": translate(_("UID is required"), context=self.request),
                }
            }

        rows_folder = uuidToObject(uid)
        if rows_folder:
            alsoProvides(self.request, IDisableCSRFProtection)
            manager = Manager(self.context)
            template = {"name": name, "uid": uid}
            manager.append_template(template)

            return self.reply_no_content()

        self.request.response.setStatus(400)
        return {
            "error": {
                "type": "Bad Request",
                "message": translate(_("Content does not exist"), context=self.request),
            }
        }
