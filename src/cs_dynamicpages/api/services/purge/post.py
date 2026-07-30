from plone.restapi.services import Service
from z3c.caching.purge import Purge
from zope.event import notify


class PurgePost(Service):
    def reply(self):
        notify(Purge(self.context))
        return self.reply_no_content()
