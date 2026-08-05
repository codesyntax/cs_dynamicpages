---
myst:
  html_meta:
    "description": "How to configure the Dynamic Pages registry"
    "property=og:description": "How to configure the Dynamic Pages registry"
    "property=og:title": "Configure the Registry (Widths & Spacers)"
    "keywords": "Plone, cs_dynamicpages, admin, registry, css, spacing"
---

# Configure the Registry (Widths & Spacers)

`cs_dynamicpages` avoids hardcoding CSS classes for layouts. Instead, it relies on a central configuration {term}`registry <Dynamic Pages Registry>` where site administrators can define exactly which spacing utilities and width constraints are available to content editors.

By default, the add-on ships with standard Bootstrap 5 utility classes (e.g., `mt-3`, `pb-5`, `col-md-8 offset-md-2`). If your theme uses a different CSS framework (like Tailwind, Bulma, or a custom grid), you can easily update these values.

## Accessing the Control Panel

1. Log into Plone as a Site Administrator or Manager.
2. Navigate to **Site Setup** -> **Dynamic Pages Control Panel**.

Here, you will find several tabs:
* **Row type fields:** Mappings of views to their visible fields and child constraints (see {doc}`custom-row-view`).
* **Top-level row types:** Constraints on which rows can be added directly to a page.
* **Row widths:** Definitions for the `Width` dropdown on rows.
* **Spacers:** Definitions for top/bottom margins and paddings.

## Structural Governance

`cs_dynamicpages` allows you to control the hierarchy of your pages to ensure design consistency.

### Top-level Row Types
In the **Top-level row types** tab, you can select which row types are allowed to be added directly to a {term}`Dynamic Page Folder`. If you leave this list empty, all registered row types are allowed.

### Allowed Child Row Types
Within the **Row type fields** tab, each row definition includes an **Allowed child row types** field. This allows you to restrict what can be added inside a folderish row. For example, you might want to allow only "Image" rows inside a "Slider" row.

## Modifying Row Widths

When a content editor creates a row, they can choose its width. The default options are usually "Full width", "Centered", and "Narrow".

To change these or add new ones to match your theme:

1. Go to the **Row widths** tab.
2. You will see a DataGrid (a table of rows).
3. To add a new width, click **Add**.
   * **Row Width Label:** This is what the editor sees in the dropdown (e.g., "Extra Narrow").
   * **Row Width CSS class:** This is the exact CSS class injected into the row's wrapper `<div>` (e.g., `col-md-4 offset-md-4` or `max-w-prose mx-auto`).
4. Click **Save** at the bottom of the control panel.

## Modifying Spacers (Margins and Paddings)

Spacers allow editors to control the vertical rhythm of the page without writing custom CSS. The add-on provides four separate dropdowns on rows: Top Margin, Bottom Margin, Top Padding, and Bottom Padding.

The classes for these are managed in the respective tabs:
* **Spacer padding top**
* **Spacer padding bottom**
* **Spacer margin top**
* **Spacer margin bottom**

If you are using Tailwind CSS instead of Bootstrap, you would change these values:

1. Go to the **Spacer padding top** tab.
2. Edit the existing rows or add new ones.
   * **Spacer Label:** The human-readable label (e.g., "Large").
   * **Spacer CSS class:** The utility class (e.g., `pt-12` instead of Bootstrap's `pt-5`).
3. Click **Save**.

The changes will immediately be reflected in the edit form dropdowns for all {term}`Dynamic Page Row` instances across the site.
