from cs_dynamicpages import _
from cs_dynamicpages.templates import Manager
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.i18n import translate
from zope.interface import alsoProvides

import transaction


class ApplyTemplatePost(Service):
    def reply(self):
        body = json_body(self.request)
        uid = body.get("uid")
        if uid is None:
            self.request.response.setStatus(400)
            return {
                "error": {
                    "type": "Bad Request",
                    "message": translate(_("UID is required"), context=self.request),
                }
            }

        manager = Manager(self.context)
        template = manager.get_template(uid)
        if template is None:
            self.request.response.setStatus(400)
            return {
                "error": {
                    "type": "Bad Request",
                    "message": translate(
                        _("Template name is not valid"), context=self.request
                    ),
                }
            }

        rows_folder = uuidToObject(uid)
        if rows_folder:
            alsoProvides(self.request, IDisableCSRFProtection)

            transaction.savepoint(True)
            if "rows" in self.context:
                api.content.delete(self.context.rows, check_linkintegrity=False)

            api.content.copy(
                source=rows_folder,
                target=self.context,
            )

            return self.reply_no_content()

        self.request.response.setStatus(400)
        return {
            "error": {
                "type": "Bad Request",
                "message": translate(_("Content does not exist"), context=self.request),
            }
        }
