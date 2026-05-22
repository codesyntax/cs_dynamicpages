from cs_dynamicpages import logger
from plone import api
from plone.app.uuid.utils import uuidToObject
from urllib.parse import urlparse
from zope.component import getSiteManager
from zope.globalrequest import getRequest
from zope.interface import Interface
from zope.interface import providedBy


VIEW_PREFIX = "cs_dynamicpages-"

# links starting with these URL scheme should not be redirected to
NON_REDIRECTABLE_URL_SCHEMES = [
    "mailto:",
    "tel:",
    "callto:",  # nonstandard according to RFC 3966. used for skype.
    "webdav:",
    "caldav:",
]

# links starting with these URL scheme should not be resolved to paths
NON_RESOLVABLE_URL_SCHEMES = [*NON_REDIRECTABLE_URL_SCHEMES, "file:", "ftp:"]


def add_custom_view(
    view_name: str,
    shown_fields: list[str],
    has_button: bool = False,
    icon: str = "bricks",
):
    """utility function to add a given view to the list of available row types"""
    record_name = "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields"
    values = api.portal.get_registry_record(record_name)
    existing_views = [item.get("row_type") for item in values]
    if view_name in existing_views:
        return False

    new_item = {
        "row_type": view_name,
        "each_row_type_fields": shown_fields,
        "row_type_has_featured_add_button": has_button,
        "row_type_icon": icon,
    }
    values.append(new_item)
    api.portal.set_registry_record(record_name, values)
    logger.info("Added new row type: %s", view_name)

    return True


def enable_behavior(behavior_dotted_name=str):
    """
    utility function to enable the given behavior in the DynamicPageRow content type
    """
    # Get the portal_types tool, which manages all content type definitions (FTIs)
    portal_types = api.portal.get_tool("portal_types")

    # Get the Factory Type Information (FTI) for our specific content type
    fti = getattr(portal_types, "DynamicPageRow", None)

    if not fti:
        # Failsafe in case the content type doesn't exist
        print("Content type 'DynamicPageRow' not found.")
        return

    # Get the current list of behaviors
    behaviors = list(fti.behaviors)

    # --- The Core Logic ---
    # Check if the behavior is already enabled to avoid duplicates
    if behavior_dotted_name not in behaviors:
        print(f"Enabling behavior '{behavior_dotted_name}' on 'DynamicPageRow'.")
        # Add the new behavior to the list
        behaviors.append(behavior_dotted_name)
        # Assign the updated list back to the FTI's behaviors attribute
        fti.behaviors = tuple(behaviors)
    else:
        print(
            f"Behavior '{behavior_dotted_name}' is already enabled on 'DynamicPageRow'."
        )


def get_available_views_for_row():
    from cs_dynamicpages.content.dynamic_page_row import IDynamicPageRow
    from cs_dynamicpages.interfaces import IRowTypeMetadata

    sm = getSiteManager()
    available_views = sm.adapters.lookupAll(
        required=(IDynamicPageRow, providedBy(getRequest())),
        provided=Interface,
    )

    registry_values = api.portal.get_registry_record(
        "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields", default=[]
    )
    registry_map = {item["row_type"]: item for item in registry_values}

    items = []
    for name, factory in available_views:
        if not name.startswith(VIEW_PREFIX):
            continue

        # Start with Code Defaults
        item_dict = {
            "row_type": name,
            "each_row_type_fields": [],
            "row_type_has_featured_add_button": False,
            "row_type_icon": "bricks",
        }

        # Try to get metadata from factory
        if IRowTypeMetadata.implementedBy(factory):
            item_dict["each_row_type_fields"] = list(
                getattr(factory, "allowed_fields", [])
            )
            item_dict["row_type_has_featured_add_button"] = getattr(
                factory, "has_featured", False
            )
            item_dict["row_type_icon"] = getattr(factory, "icon", "bricks")

        # Merge Registry Overrides
        if name in registry_map:
            override = registry_map[name]
            # If the registry has specific fields defined, use them
            if override.get("each_row_type_fields"):
                item_dict["each_row_type_fields"] = list(
                    override["each_row_type_fields"]
                )

            # Icons and buttons can also be overridden
            if override.get("row_type_icon"):
                item_dict["row_type_icon"] = override["row_type_icon"]

            if override.get("row_type_has_featured_add_button") is not None:
                item_dict["row_type_has_featured_add_button"] = override[
                    "row_type_has_featured_add_button"
                ]

        items.append(item_dict)
    return items


def get_row_config(view_name):
    configs = get_available_views_for_row()
    for config in configs:
        if config["row_type"] == view_name:
            return config
    return None


def normalize_uid_from_path(url=None):
    """
    Args:
        url (string): a path or orl

    Returns:
        tuple: tuple of (uid, fragment) a fragment is an anchor id e.g. #head1
    """
    uid = None
    fragment = None

    if not url:
        return uid, fragment

    # resolve uid
    paths = url.split("/")
    paths_lower = [_item.lower() for _item in paths]

    if "resolveuid" in paths_lower:
        ri = paths_lower.index("resolveuid")
        if ri + 1 != len(paths):
            uid = paths[ri + 1]
            if uid == "":
                uid = None

    if not uid:
        return uid, fragment

    # resolve fragment
    parts = urlparse(uid)

    uid = parts.path

    fragment = f"#{parts.fragment}" if parts.fragment else None

    return uid, fragment


def _url_uses_scheme(schemes, url):
    return any(url.startswith(scheme) for scheme in schemes)


def absolute_target_url(url):
    """Compute the absolute target URL."""

    if _url_uses_scheme(NON_RESOLVABLE_URL_SCHEMES, url):
        # For non http/https url schemes, there is no path to resolve.
        return url

    else:
        if "resolveuid" in url:
            uid, fragment = normalize_uid_from_path(url)
            obj = uuidToObject(uid)
            if obj is None:
                # uid can't resolve, return the url
                return url

            url = obj.absolute_url()
            if fragment is not None:
                url = f"{url}{fragment}"
    return url
