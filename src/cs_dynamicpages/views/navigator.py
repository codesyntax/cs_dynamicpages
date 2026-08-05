from plone import api
from Products.Five.browser import BrowserView


class NavigatorView(BrowserView):
    """View to provide data for the recursive row navigator."""

    def row_tree(self):
        """Build a recursive tree of rows."""
        # Find the DynamicPageFolder first
        page_folders = api.content.find(
            portal_type="DynamicPageFolder",
            context=self.context,
            depth=1,
            sort_on="getObjPositionInParent",
        )
        if not page_folders:
            return []

        folder = page_folders[0].getObject()
        return self._get_children(folder, depth=0)

    def _get_children(self, container, depth=0):
        """Recursively fetch DynamicPageRow children."""
        results = []
        brains = api.content.find(
            context=container,
            portal_type="DynamicPageRow",
            sort_on="getObjPositionInParent",
            depth=1,
        )

        total = len(brains)
        for index, brain in enumerate(brains):
            obj = brain.getObject()
            item = {
                "id": obj.getId(),
                "uid": obj.UID(),
                "title": obj.Title(),
                "row_type": getattr(obj, "row_type", ""),
                "allows_children": obj.show_add_child_button(),
                "depth": depth,
                "is_first": index == 0,
                "is_last": index == total - 1,
                "url": obj.absolute_url(),
                "parent_url": container.absolute_url(),
                "can_edit": api.user.has_permission("Modify portal content", obj=obj),
                "children": self._get_children(obj, depth + 1),
            }
            results.append(item)
        return results

    def normalize_title(self, title):
        """Reuse normalization logic from dynamic_view."""
        return (
            title.replace("cs_dynamicpages-", " ")
            .replace("-", " ")
            .replace("_", " ")
            .replace("view", "")
            .lower()
        )
