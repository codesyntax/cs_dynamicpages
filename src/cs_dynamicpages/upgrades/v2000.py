from . import logger
from plone import api

import uuid


def update_registry_schema_and_add_types():
    """Update registry keys from featured to child/allows_children and add new types"""
    registry = api.portal.get_tool("portal_registry")
    record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
    row_type_fields = list(registry.get(record_name, []))

    # 1. Update existing records to new schema (rename key and add new keys)
    for field in row_type_fields:
        if "row_type_has_featured_add_button" in field:
            field["row_type_allows_children"] = field.pop(
                "row_type_has_featured_add_button"
            )
        if "allowed_child_row_types" not in field:
            field["allowed_child_row_types"] = []

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
            "allowed_child_row_types": [],
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
            "allowed_child_row_types": [],
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
        # Parent might also be a broken object if it's a nested DynamicPageRowFeatured
        parent_row_type = getattr(parent, "row_type", "")
        if not parent_row_type and hasattr(parent, "__dict__"):
            parent_row_type = parent.__dict__.get("row_type", "")
        new_row_type = "cs_dynamicpages-text-view"  # Default fallback

        if parent_row_type == "cs_dynamicpages-slider-view":
            new_row_type = "cs_dynamicpages-image-view"
        elif parent_row_type == "cs_dynamicpages-features-view":
            new_row_type = "cs_dynamicpages-card-view"
        elif parent_row_type == "cs_dynamicpages-accordion-view":
            new_row_type = "cs_dynamicpages-text-view"

        # Let's create the new object
        new_id = f"{brain.getId}-migrated-{str(uuid.uuid4())[:8]}"

        new_obj = api.content.create(
            type="DynamicPageRow",
            container=parent,
            id=new_id,
            title=brain.Title,
            description=brain.Description,
            row_type=new_row_type,
        )

        # Transfer data robustly.
        # We try to get the object state to handle "Broken Objects" where the class code is missing.
        state = {}
        if hasattr(old_obj, "__getstate__"):
            try:
                state = old_obj.__getstate__()
            except Exception:
                state = getattr(old_obj, "__dict__", {})
        elif hasattr(old_obj, "__dict__"):
            state = old_obj.__dict__

        # List of attributes to rescue (Standard + Common Behaviors)
        RESCUE_ATTRS = [
            "text",
            "related_image",
            "link_url",
            "link_text",
            "tabs_content",
            "grid_rows",
            "accordion_links",
            "links",
            "kicker_text",
            "youtube_link",
            "blockquote_title",
            "blockquote_description",
            "teacher_listing",
            "html_code",
            "card_render_type",
            "first_item_featured",
            "is_section_heading",
            "show_title",
            "show_ask_info_button",
        ]

        for attr in RESCUE_ATTRS:
            # We use state.get() because broken objects might crash on direct getattr()
            # for some internal reasons, and state inspection is safer.
            val = state.get(attr, None)
            if val is not None:
                try:
                    setattr(new_obj, attr, val)
                except Exception as e:
                    logger.warning(
                        f"Could not rescue attribute {attr} for {brain.getPath()}: {e}"
                    )

        # Handle position
        position = 0
        import contextlib

        old_id = brain.getId
        with contextlib.suppress(AttributeError, KeyError):
            position = parent.getObjectPositionInParent(old_id)

        parent.moveObjectToPosition(new_obj.getId(), position)

        # Delete old object
        api.content.delete(old_obj)

        # Rename new object to old id
        api.content.rename(obj=new_obj, new_id=old_id)


def upgrade(setup_tool=None):
    """Migrate DynamicPageRowFeatured to DynamicPageRow and update registry"""
    logger.info(
        "Running upgrade (Python): Migrate DynamicPageRowFeatured to DynamicPageRow"
    )

    update_registry_schema_and_add_types()
    migrate_featured_to_rows()

    logger.info("Migration completed.")
