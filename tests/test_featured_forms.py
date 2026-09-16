from cs_dynamicpages.browser.featured_forms import get_allowed_featured_fields_for_row
from cs_dynamicpages.interfaces import IBrowserLayer
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import pytest


@pytest.mark.usefixtures("integration")
class TestFeaturedForms:
    @pytest.fixture(autouse=True)
    def setup(self, portal):
        self.portal = portal
        setRoles(portal, TEST_USER_ID, ["Manager"])
        alsoProvides(self.portal.REQUEST, IBrowserLayer)

    def _get_all_field_keys(self, form):
        keys = (
            list(form.fields.keys()) if hasattr(form, "fields") and form.fields else []
        )
        if hasattr(form, "groups") and form.groups:
            for group in form.groups:
                if hasattr(group, "fields") and group.fields:
                    keys.extend(group.fields.keys())
        return keys

    def _set_row_type_featured_fields(self, row_type, featured_fields):
        records = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
        )
        for record in records:
            if record.get("row_type") == row_type:
                record["each_featured_type_fields"] = featured_fields
                break
        api.portal.set_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields", records
        )

    def test_get_allowed_featured_fields_from_registry(self):
        """Test get_allowed_featured_fields_for_row reads registry configuration."""
        self._set_row_type_featured_fields(
            "cs_dynamicpages-slider-view", ["title", "related_image"]
        )
        allowed = get_allowed_featured_fields_for_row("cs_dynamicpages-slider-view")
        assert allowed == ["title", "related_image"]

    def test_featured_edit_form_filtering_from_registry(self):
        """Test edit form filters fields based on registry configuration."""
        self._set_row_type_featured_fields(
            "cs_dynamicpages-slider-view", ["title", "related_image"]
        )

        rows_folder = api.content.create(
            type="DynamicPageFolder",
            title="Rows",
            id="rows-test",
            container=self.portal,
        )
        row = api.content.create(
            type="DynamicPageRow",
            title="Slider Row",
            id="slider-row",
            container=rows_folder,
            row_type="cs_dynamicpages-slider-view",
        )
        featured = api.content.create(
            type="DynamicPageRowFeatured",
            title="Slider Item",
            id="slider-item",
            container=row,
        )

        edit_view = getMultiAdapter((featured, self.portal.REQUEST), name="edit")
        edit_view.update()
        form = getattr(edit_view, "form_instance", edit_view)

        field_keys = self._get_all_field_keys(form)

        # Configured fields should be present
        assert any(k == "title" or k.endswith(".title") for k in field_keys)
        assert any("related_image" in k for k in field_keys)

        # Non-configured fields (e.g., link_url, link_text, text) should NOT be present
        assert not any("link_url" in k for k in field_keys)
        assert not any("link_text" in k for k in field_keys)

    def test_featured_add_form_filtering_from_registry(self):
        """Test add form filters fields based on registry configuration."""
        self._set_row_type_featured_fields(
            "cs_dynamicpages-features-view", ["title", "link_url"]
        )

        rows_folder = api.content.create(
            type="DynamicPageFolder",
            title="Rows",
            id="rows-test-2",
            container=self.portal,
        )
        row = api.content.create(
            type="DynamicPageRow",
            title="Features Row",
            id="features-row",
            container=rows_folder,
            row_type="cs_dynamicpages-features-view",
        )

        add_view = row.restrictedTraverse("++add++DynamicPageRowFeatured")
        add_view.update()
        form = getattr(add_view, "form_instance", add_view)

        field_keys = self._get_all_field_keys(form)

        assert any(k == "title" or k.endswith(".title") for k in field_keys)
        assert any("link_url" in k for k in field_keys)
        assert not any("related_image" in k for k in field_keys)

    def test_unconfigured_row_preserves_all_fields(self):
        """Test row types without configured featured fields keep all fields."""
        rows_folder = api.content.create(
            type="DynamicPageFolder",
            title="Rows",
            id="rows-test-3",
            container=self.portal,
        )
        row = api.content.create(
            type="DynamicPageRow",
            title="Accordion Row",
            id="accordion-row",
            container=rows_folder,
            row_type="cs_dynamicpages-accordion-view",
        )
        featured = api.content.create(
            type="DynamicPageRowFeatured",
            title="Accordion Item",
            id="accordion-item",
            container=row,
        )

        edit_view = getMultiAdapter((featured, self.portal.REQUEST), name="edit")
        edit_view.update()
        form = getattr(edit_view, "form_instance", edit_view)

        field_keys = self._get_all_field_keys(form)

        # Unconfigured rows preserve all standard fields
        assert any(k == "title" or k.endswith(".title") for k in field_keys)
        assert any("link_url" in k for k in field_keys)
