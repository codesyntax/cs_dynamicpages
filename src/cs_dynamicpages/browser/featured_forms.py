"""Custom Add and Edit forms for DynamicPageRowFeatured.

Dynamically filters visible form fields and fieldset groups based on the
parent DynamicPageRow configuration stored in the Plone Registry.
"""

from Acquisition import aq_parent
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from z3c.form.field import Fields

import logging


logger = logging.getLogger(__name__)


def _matches_allowed(field_key: str, allowed_fields: list[str]) -> bool:
    """Matches a field key against allowed names, supporting dotted prefixes."""
    field_short = field_key.split(".")[-1]
    for pattern in allowed_fields:
        pattern_short = pattern.split(".")[-1]
        if field_key == pattern or field_short == pattern_short:
            return True
    return False


def get_allowed_featured_fields_for_row(row_type: str | None) -> list[str] | None:
    """Fetches allowed featured fields for a given row type from the registry."""
    if not row_type:
        return None
    try:
        records = api.portal.get_registry_record(
            "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields",
            default=[],
        )
        for record in records:
            if record.get("row_type") == row_type:
                fields = record.get("each_featured_type_fields")
                return fields if fields else None
    except Exception as exc:
        logger.debug("Failed to retrieve row_type_fields from registry: %s", exc)
    return None


def filter_form_fields_for_row(form, row_type: str | None) -> None:
    """Filters top-level fields and prunes empty fieldset groups from the form."""
    allowed = get_allowed_featured_fields_for_row(row_type)
    if not allowed:
        return

    # Filter base fields
    if hasattr(form, "fields") and form.fields:
        filtered_fields = [
            f for k, f in form.fields.items() if _matches_allowed(k, allowed)
        ]
        form.fields = Fields(*filtered_fields)

    # Filter fields in fieldset groups and remove empty groups
    if hasattr(form, "groups") and form.groups:
        new_groups = []
        for group in form.groups:
            if hasattr(group, "fields") and group.fields:
                filtered_group_fields = [
                    f for k, f in group.fields.items() if _matches_allowed(k, allowed)
                ]
                if filtered_group_fields:
                    group.fields = Fields(*filtered_group_fields)
                    new_groups.append(group)
        form.groups = new_groups


class DynamicPageRowFeaturedAddForm(DefaultAddForm):
    """Add form that restricts fields according to the parent row configuration."""

    portal_type = "DynamicPageRowFeatured"

    def updateFields(self):
        super().updateFields()
        row_type = getattr(self.context, "row_type", None)
        filter_form_fields_for_row(self, row_type)


class DynamicPageRowFeaturedAddView(DefaultAddView):
    """Add view wrapper for DynamicPageRowFeatured."""

    form = DynamicPageRowFeaturedAddForm


class DynamicPageRowFeaturedEditForm(DefaultEditForm):
    """Edit form that restricts fields according to the parent row configuration."""

    def updateFields(self):
        super().updateFields()
        parent_row = aq_parent(self.context)
        row_type = getattr(parent_row, "row_type", None)
        filter_form_fields_for_row(self, row_type)
