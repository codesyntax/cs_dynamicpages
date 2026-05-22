"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRowTypeMetadata(Interface):
    """Metadata for a row type view."""

    allowed_fields = schema.List(
        title="Allowed fields",
        value_type=schema.TextLine(),
        required=False,
        default=[],
    )

    has_featured = schema.Bool(
        title="Has featured",
        required=False,
        default=False,
    )

    icon = schema.TextLine(
        title="Icon",
        required=False,
        default="bricks",
    )
