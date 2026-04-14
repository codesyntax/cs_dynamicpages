---
myst:
  html_meta:
    "description": "cs_dynamicpages Custom Behaviors"
    "property=og:description": "cs_dynamicpages Custom Behaviors"
    "property=og:title": "Custom Behaviors"
    "keywords": "Plone, cs_dynamicpages, reference, behaviors, dexterity"
---

# Custom Behaviors

Rather than using monolithic schemas, `cs_dynamicpages` defines several specialized Dexterity behaviors. These behaviors are applied to the {term}`Dynamic Page Row` and {term}`Dynamic Page Row Featured` content types to provide modular fields.

By decoupling fields into behaviors, the add-on allows maximum flexibility and reuse.

Below is a reference of the custom behaviors provided by the package.

## Structural Behaviors

### Row Width (`cs_dynamicpages.row_width`)
Provides the `width` field, allowing the editor to define the maximum width of the row content (e.g., "Full width", "Centered", "Narrow"). The available options are managed dynamically via the {term}`Dynamic Pages Registry`.

### Row Columns (`cs_dynamicpages.row_columns`)
Provides the `columns` field, used in grid views (like the *Features View* or *Query Columns View*) to determine how many columns the grid should split into (e.g., 2, 3, or 4 columns).

### Row Vertical Spacing (`cs_dynamicpages.row_vertical_spacing`)
Provides a set of fields to control the CSS margin and padding (top and bottom) of a row.
* `margin_top`
* `margin_bottom`
* `padding_top`
* `padding_bottom`
The available spacing classes (e.g., `mt-1`, `pb-5`) are managed dynamically via the {term}`Dynamic Pages Registry`.

### Extra Class (`cs_dynamicpages.extra_class`)
Provides the `extra_class` field. This allows advanced editors to inject custom CSS classes directly into the row's wrapper `<div>`, enabling custom styling hooks without modifying templates.

## Media & Links

### Related Image (`cs_dynamicpages.related_image`)
Provides an image upload field (`related_image`) and an image alignment field (`image_position`). Useful for Hero blocks or Featured rows where a distinct image is required alongside text.

### Fetch Priority Image (`cs_dynamicpages.fetchpriority_image`)
Provides a boolean field (`fetchpriority_image`). When checked, it adds the `fetchpriority="high"` attribute to the primary image in the row. This is a crucial SEO and performance feature for optimizing the Largest Contentful Paint (LCP), typically used on the first row (Hero image) of a landing page.

### Link Info (`cs_dynamicpages.link_info`)
Provides fields for creating a Call-To-Action (CTA) button.
* `link_url`: The destination URL (supports internal path references or absolute URLs).
* `link_text`: The text displayed on the button.

## Templates

### Templates (`cs_dynamicpages.templates`)
Provides the internal mechanics to save a full {term}`DynamicPageFolder <Dynamic Page Folder>` configuration as a reusable template. This allows editors to construct complex landing pages and save them to be stamped out again in the future.
