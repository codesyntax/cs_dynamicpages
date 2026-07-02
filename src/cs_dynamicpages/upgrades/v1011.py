from . import logger
from plone import api

import uuid


def update_registry_schema_and_add_types():
    """Update registry keys from featured to child/allows_children and add new types"""
    registry = api.portal.get_tool("portal_registry")
    record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
    row_type_fields = list(registry.get(record_name, []))

    # 1. Update existing records to new schema (rename key)
    for field in row_type_fields:
        if "row_type_has_featured_add_button" in field:
            field["row_type_allows_children"] = field.pop(
                "row_type_has_featured_add_button"
            )

    existing_row_types = [field["row_type"] for field in row_type_fields]

    # 2. Define new primitives with new key
    new_primitives = [
        {
            "row_type": "cs_dynamicpages-image-view",
            "each_row_type_fields": [
                "IBasic.title",
                "IRowWidth.width",
                "IExtraClass.extra_class",
                "IRelatedImage.related_image",
                "IFetchPriorityImage.fetchpriority_image",
                "IRowVerticalSpacing.padding_top",
                "IRowVerticalSpacing.padding_bottom",
                "IRowVerticalSpacing.margin_top",
                "IRowVerticalSpacing.margin_bottom",
            ],
            "row_type_allows_children": False,
            "row_type_icon": "image",
        },
        {
            "row_type": "cs_dynamicpages-card-view",
            "each_row_type_fields": [
                "IBasic.title",
                "IBasic.description",
                "IRowWidth.width",
                "IExtraClass.extra_class",
                "IRelatedImage.related_image",
                "IFetchPriorityImage.fetchpriority_image",
                "IRichTextBehavior-text",
                "ILinkInfo.link_text",
                "ILinkInfo.link_url",
                "IRowVerticalSpacing.padding_top",
                "IRowVerticalSpacing.padding_bottom",
                "IRowVerticalSpacing.margin_top",
                "IRowVerticalSpacing.margin_bottom",
            ],
            "row_type_allows_children": False,
            "row_type_icon": "card-heading",
        },
    ]

    for primitive in new_primitives:
        if primitive["row_type"] not in existing_row_types:
            row_type_fields.append(primitive)

    # Save back to registry
    registry[record_name] = row_type_fields
    logger.info("Updated registry schema and added new primitive row types.")


def migrate_featured_to_rows():
    """Migrate DynamicPageRowFeatured to DynamicPageRow"""
    portal = api.portal.get()
    brains = api.content.find(
        portal_type="DynamicPageRowFeatured",
        context=portal,
    )

    logger.info(f"Found {len(brains)} DynamicPageRowFeatured objects to migrate.")

    for brain in brains:
        old_obj = brain.getObject()
        parent = old_obj.aq_parent

        # Determine appropriate row_type based on parent
        parent_row_type = getattr(parent, "row_type", "")
        new_row_type = "cs_dynamicpages-text-view"  # Default fallback

        if parent_row_type == "cs_dynamicpages-slider-view":
            new_row_type = "cs_dynamicpages-image-view"
        elif parent_row_type == "cs_dynamicpages-features-view":
            new_row_type = "cs_dynamicpages-card-view"
        elif parent_row_type == "cs_dynamicpages-accordion-view":
            new_row_type = "cs_dynamicpages-text-view"

        # Let's create the new object
        new_id = f"{old_obj.getId()}-migrated-{str(uuid.uuid4())[:8]}"

        new_obj = api.content.create(
            type="DynamicPageRow",
            container=parent,
            id=new_id,
            title=old_obj.Title(),
            description=old_obj.Description(),
            row_type=new_row_type,
        )

        # Transfer data
        if hasattr(old_obj, "text"):
            new_obj.text = old_obj.text

        if hasattr(old_obj, "link_url"):
            new_obj.link_url = old_obj.link_url

        if hasattr(old_obj, "link_text"):
            new_obj.link_text = old_obj.link_text

        if hasattr(old_obj, "related_image"):
            new_obj.related_image = old_obj.related_image

        # Handle position
        position = 0
        import contextlib

        with contextlib.suppress(AttributeError, KeyError):
            position = parent.getObjectPositionInParent(old_obj.getId())

        parent.moveObjectToPosition(new_obj.getId(), position)

        # Delete old object
        api.content.delete(old_obj)

        # Rename new object to old id
        api.content.rename(obj=new_obj, new_id=old_obj.getId())


def upgrade(setup_tool=None):
    """Migrate DynamicPageRowFeatured to DynamicPageRow and update registry"""
    logger.info(
        "Running upgrade (Python): Migrate DynamicPageRowFeatured to DynamicPageRow"
    )

    update_registry_schema_and_add_types()
    migrate_featured_to_rows()

    logger.info("Migration completed.")
