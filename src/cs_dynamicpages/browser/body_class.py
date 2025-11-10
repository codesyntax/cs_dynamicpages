from plone import api
from plone.app.contenttypes.interfaces import IFolder
from plone.app.layout.globals.layout import IBodyClassAdapter
from plone.base.interfaces import INavigationRoot
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(IFolder, Interface)
@implementer(IBodyClassAdapter)
class DynamicViewFolderClasses:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_classes(self, template, view):
        """Default body classes adapter."""
        if template.id == "dynamic_view.pt":
            can_edit = api.user.has_permission(
                "Modify portal content", obj=self.context
            )
            if can_edit:
                return ["can_edit"]
            return []
        return []


@adapter(INavigationRoot, Interface)
@implementer(IBodyClassAdapter)
class DynamicViewNavigationRootClasses:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_classes(self, template, view):
        """Default body classes adapter."""
        if template.id == "dynamic_view.pt":
            can_edit = api.user.has_permission(
                "Modify portal content", obj=self.context
            )
            if can_edit:
                return ["can_edit"]
            return []
        return []
