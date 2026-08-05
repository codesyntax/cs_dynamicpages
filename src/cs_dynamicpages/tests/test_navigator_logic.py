from cs_dynamicpages.testing import CS_DYNAMICPAGES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestNavigatorLogic(unittest.TestCase):
    """Integration tests for Navigator view logic."""

    layer = CS_DYNAMICPAGES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.dpf = api.content.create(
            container=self.portal,
            type="DynamicPageFolder",
            id="rows",
            title="Rows",
        )

    def test_row_tree_empty(self):
        from cs_dynamicpages.views.navigator import NavigatorView

        view = NavigatorView(self.dpf, self.layer["request"])
        tree = view.row_tree()
        self.assertEqual(len(tree), 0)

    def test_row_tree_nested(self):
        # Create a hierarchy:
        # Row 1 (Accordion)
        #   Row 1.1 (Text)
        #   Row 1.2 (Text)
        # Row 2 (Slider)
        #   Row 2.1 (Image)

        row1 = api.content.create(
            container=self.dpf,
            type="DynamicPageRow",
            id="row1",
            title="Accordion",
            row_type="cs_dynamicpages-accordion-view",
        )
        api.content.create(
            container=row1,
            type="DynamicPageRow",
            id="row1-1",
            title="Panel 1",
            row_type="cs_dynamicpages-text-view",
        )
        api.content.create(
            container=row1,
            type="DynamicPageRow",
            id="row1-2",
            title="Panel 2",
            row_type="cs_dynamicpages-text-view",
        )
        row2 = api.content.create(
            container=self.dpf,
            type="DynamicPageRow",
            id="row2",
            title="Slider",
            row_type="cs_dynamicpages-slider-view",
        )
        api.content.create(
            container=row2,
            type="DynamicPageRow",
            id="row2-1",
            title="Slide 1",
            row_type="cs_dynamicpages-image-view",
        )

        from cs_dynamicpages.views.navigator import NavigatorView

        view = NavigatorView(self.portal, self.layer["request"])
        tree = view.row_tree()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0]["id"], "row1")
        self.assertEqual(len(tree[0]["children"]), 2)
        self.assertEqual(tree[0]["children"][0]["id"], "row1-1")
        self.assertEqual(tree[0]["children"][0]["depth"], 1)

        self.assertEqual(tree[1]["id"], "row2")
        self.assertEqual(len(tree[1]["children"]), 1)
        self.assertEqual(tree[1]["children"][0]["id"], "row2-1")
        self.assertEqual(tree[1]["children"][0]["depth"], 1)

    def test_recursive_deletion(self):
        """Test that deleting a parent row deletes all children."""
        row1 = api.content.create(
            container=self.dpf,
            type="DynamicPageRow",
            id="parent",
            title="Parent",
        )
        child = api.content.create(
            container=row1,
            type="DynamicPageRow",
            id="child",
            title="Child",
        )
        grandchild = api.content.create(
            container=child,
            type="DynamicPageRow",
            id="grandchild",
            title="Grandchild",
        )

        child_uid = child.UID()
        grandchild_uid = grandchild.UID()

        # Delete parent
        api.content.delete(obj=row1)

        # Verify all are gone
        self.assertNotIn("parent", self.dpf.objectIds())
        self.assertIsNone(api.content.get(UID=child_uid))
        self.assertIsNone(api.content.get(UID=grandchild_uid))
