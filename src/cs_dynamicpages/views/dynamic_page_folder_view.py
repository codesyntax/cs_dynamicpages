# from cs_dynamicpages import _
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from contextlib import suppress
from cs_dynamicpages import _
from cs_dynamicpages.utils import get_available_views_for_row
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from uuid import uuid4
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface


class IDynamicPageFolderView(Interface):
    """Marker Interface for IDynamicPageFolderView"""


@implementer(IDynamicPageFolderView)
class DynamicPageFolderView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('dynamic_page_folder_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()


@implementer(IDynamicPageFolderView)
class DynamicPageAddRowContentView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('dynamic_page_folder_view.pt')

    def __call__(self):
        # Implement your own actions:
        row_type = self.request.get("row_type") or self.request.form.get("row_type")
        position = self.request.get("position") or self.request.form.get("position")
        container_uid = self.request.get("container") or self.request.form.get(
            "container"
        )

        container = self.context
        if container_uid:
            container = uuidToObject(container_uid) or self.context

        if row_type:
            random_id = str(uuid4())

            alsoProvides(self.request, IDisableCSRFProtection)
            obj = api.content.create(
                type="DynamicPageRow",
                container=container,
                row_type=row_type,
                title=row_type,
                description="Here goes the description",
                id=random_id,
                link_text="Link Text",
                link_url="/",
            )
            if position is not None:
                with suppress(ValueError, TypeError):
                    container.moveObjectToPosition(obj.getId(), int(position))

            available_views = get_available_views_for_row()
            for view in available_views:
                if view["row_type"] == row_type:
                    has_children = view["row_type_allows_children"]
                    if has_children:
                        api.content.create(
                            type="DynamicPageRow",
                            container=obj,
                            title="New Nested Row",
                            description="Here goes the description",
                            id=str(uuid4()),
                            row_type="cs_dynamicpages-text-view",
                            link_text="Link Text",
                            link_url="/",
                        )

                        api.content.create(
                            type="DynamicPageRow",
                            container=obj,
                            title="New Nested Row 2",
                            description="Here goes the description",
                            id=str(uuid4()),
                            row_type="cs_dynamicpages-text-view",
                            link_text="Link Text",
                            link_url="/",
                        )
            statusmessage = _("Row added successfully")
            api.portal.show_message(statusmessage, type="info")

            # Redirect to the dynamic view, which is likely on a parent of
            # DynamicPageFolder
            # Search for the DynamicView registered for IFolder or INavigationRoot
            redirect_url = container.absolute_url()
            with suppress(Exception):
                # Try to find the parent that has the dynamic-view assigned
                curr = container
                while curr:
                    if api.content.get_view(
                        name="dynamic-view", context=curr, request=self.request
                    ):
                        redirect_url = f"{curr.absolute_url()}#{random_id}"
                        break
                    curr = curr.aq_parent

            return self.request.response.redirect(redirect_url)
