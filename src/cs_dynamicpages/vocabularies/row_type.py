from Acquisition import aq_parent
from cs_dynamicpages.content.dynamic_page_folder import IDynamicPageFolder
from cs_dynamicpages.content.dynamic_page_row import IDynamicPageRow
from cs_dynamicpages.utils import CORE_TYPES
from cs_dynamicpages.utils import get_available_views_for_row
from cs_dynamicpages.utils import VIEW_PREFIX
from zope.component import getSiteManager
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def is_registered(name):
    if not name.startswith(VIEW_PREFIX):
        return False

    sm = getSiteManager()
    try:
        # Check for browser view registration
        # required: (context, request)
        adapter = sm.adapters.lookup(
            (IDynamicPageRow, IBrowserRequest), Interface, name=name
        )
        return adapter is not None
    except Exception:
        return False


class DynamicVocabulary(SimpleVocabulary):
    def __init__(self, terms, *args, **kwargs):
        self._strict = kwargs.pop("strict", False)
        super().__init__(terms, *args, **kwargs)

    def __contains__(self, value):
        if super().__contains__(value):
            return True
        return not self._strict and isinstance(value, str) and is_registered(value)

    def getTerm(self, value):
        try:
            return super().getTerm(value)
        except LookupError:
            if not self._strict and isinstance(value, str) and is_registered(value):
                return SimpleTerm(
                    value=value,
                    token=str(value),
                    title=value.replace(VIEW_PREFIX, ""),
                )
            raise


@implementer(IVocabularyFactory)
class RowType:
    """Vocabulary for DynamicPageRow types."""

    def _get_content_context(self, context, request):
        container = None
        is_content = False

        if IDynamicPageFolder.providedBy(context):
            container = context
            is_content = True
        elif IDynamicPageRow.providedBy(context):
            is_content = True
            actual_url = (request and request.get("ACTUAL_URL")) or ""
            is_add_form = "++add++" in actual_url
            container = aq_parent(context) if not is_add_form else context

        return is_content, container

    def __call__(self, context):
        request = getRequest()
        is_content, container = self._get_content_context(context, request)

        if is_content:
            return self._content_vocabulary(context, container)

        return self._registry_vocabulary(context)

    def _content_vocabulary(self, context, container):
        terms = []
        available_views = get_available_views_for_row(container)
        for item in available_views:
            view_name = item["row_type"]
            terms.append(
                SimpleTerm(
                    value=view_name,
                    token=str(view_name),
                    title=view_name.replace(VIEW_PREFIX, ""),
                )
            )

        # Safeguard: If we're editing an existing row, ensure current value is present
        if IDynamicPageRow.providedBy(context):
            current_value = getattr(context, "row_type", None)
            if current_value and current_value not in [t.value for t in terms]:
                terms.append(
                    SimpleTerm(
                        value=current_value,
                        token=str(current_value),
                        title=current_value.replace(VIEW_PREFIX, ""),
                    )
                )

        return DynamicVocabulary(sorted(terms, key=lambda x: x.title), strict=True)

    def _get_names_from_record(self, context, view_names):
        from plone.registry.interfaces import IRecord

        if IRecord.providedBy(context):
            old_value = getattr(context, "value", [])
            if isinstance(old_value, (list, tuple)):
                for item in old_value:
                    if isinstance(item, dict) and "row_type" in item:
                        view_names.add(item["row_type"])
                    elif isinstance(item, str):
                        view_names.add(item)
            elif isinstance(old_value, str):
                view_names.add(old_value)

    def _registry_vocabulary(self, context):
        view_names = set()
        from plone import api

        # 1. Everything currently in the registry
        try:
            row_type_fields = api.portal.get_registry_record(
                "cs_dynamicpages.dynamic_pages_control_panel.row_type_fields",
                default=[],
            )
            for item in row_type_fields:
                view_names.add(item["row_type"])
        except Exception:  # noqa: S110
            pass

        # 2. Old values of the record being validated
        self._get_names_from_record(context, view_names)

        # 3. Everything currently in CORE_TYPES
        for name in CORE_TYPES:
            view_names.add(name)

        terms = [
            SimpleTerm(value=name, token=str(name), title=name.replace(VIEW_PREFIX, ""))
            for name in view_names
        ]

        return DynamicVocabulary(sorted(terms, key=lambda x: x.title), strict=False)


RowTypeFactory = RowType()
