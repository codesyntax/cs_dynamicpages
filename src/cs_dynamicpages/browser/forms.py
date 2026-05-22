from cs_dynamicpages.utils import get_available_views_for_row
from cs_dynamicpages.utils import get_row_config
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.field import Fields

import json


class RowFormMixin:
    def _get_current_row_type(self):
        if hasattr(self.context, "row_type"):
            return self.context.row_type
        return self.request.get("row_type") or self.request.form.get(
            "form.widgets.IDynamicPageRow.row_type"
        )

    def _collect_all_fields(self):
        all_fields_dict = {}
        for name, field in self.fields.items():
            all_fields_dict[name] = field
        for group in self.groups:
            if hasattr(group, "fields"):
                for name, field in group.fields.items():
                    all_fields_dict[name] = field
        return all_fields_dict

    def _get_ordered_fields(self, all_fields_dict, allowed_fields):
        new_fields_list = []

        # Always keep row_type
        for n in ["IDynamicPageRow.row_type", "row_type"]:
            if n in all_fields_dict:
                new_fields_list.append(all_fields_dict[n])
                del all_fields_dict[n]
                break

        # Add allowed fields in order
        for field_name in allowed_fields:
            matched_name = self._find_matched_field(all_fields_dict, field_name)
            if matched_name:
                new_fields_list.append(all_fields_dict[matched_name])
                del all_fields_dict[matched_name]

        # Always include Title
        for n in ["IBasic.title", "title"]:
            if n in all_fields_dict:
                new_fields_list.append(all_fields_dict[n])
                del all_fields_dict[n]

        return new_fields_list

    def _find_matched_field(self, all_fields_dict, field_name):
        if field_name in all_fields_dict:
            return field_name
        for sep_from, sep_to in [(".", "-"), ("-", ".")]:
            norm_name = field_name.replace(sep_from, sep_to)
            if norm_name in all_fields_dict:
                return norm_name
        return None

    def _flatten_and_order_fields(self):
        row_type = self._get_current_row_type()
        if not row_type:
            return

        config = get_row_config(row_type)
        if not config:
            return

        allowed_fields = config.get("each_row_type_fields", [])
        all_fields_dict = self._collect_all_fields()
        new_fields_list = self._get_ordered_fields(all_fields_dict, allowed_fields)

        self.fields = Fields(*new_fields_list)
        self.groups = []


class RowEditForm(RowFormMixin, DefaultEditForm):
    template = ViewPageTemplateFile("row_form.pt")

    def updateFields(self):
        super().updateFields()
        self._flatten_and_order_fields()

    def row_type_configs(self):
        return json.dumps(get_available_views_for_row())


class RowAddForm(RowFormMixin, DefaultAddForm):
    template = ViewPageTemplateFile("row_form.pt")

    def updateFields(self):
        super().updateFields()
        self._flatten_and_order_fields()

    def row_type_configs(self):
        return json.dumps(get_available_views_for_row())


class RowAddView(DefaultAddView):
    form = RowAddForm
