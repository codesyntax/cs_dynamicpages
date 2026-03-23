---
myst:
  html_meta:
    "description": "cs_dynamicpages architecture and concepts"
    "property=og:description": "cs_dynamicpages architecture and concepts"
    "property=og:title": "cs_dynamicpages architecture"
    "keywords": "Plone, cs_dynamicpages, concepts, architecture"
---

# Architecture

Understanding the architecture of `cs_dynamicpages` is the key to mastering dynamic page creation in Plone. The add-on is designed to balance developer flexibility with an intuitive content editor experience.

## What is a Dynamic Page?

In `cs_dynamicpages`, a **Dynamic Page** is a composite page built by vertically stacking modular, self-contained blocks called {term}`Rows <Dynamic Page Row>`.

Instead of relying on rigid page templates or complex visual builders, site administrators and content editors can construct rich, complex landing pages (such as homepages, campaign hubs, or feature showcases) by sequentially adding rows that map to specific design patterns (e.g., text blocks, image sliders, feature grids, or accordions).

## The Core Content Types

The add-on achieves this modularity by introducing three specialized Dexterity content types:

1.  **{term}`DynamicPageFolder <Dynamic Page Folder>`**: This is the top-level container. It represents the page itself (for instance, the "Home" page) and acts as the structural envelope holding all the individual rows that compose the page.
2.  **{term}`DynamicPageRow <Dynamic Page Row>`**: Represents a single horizontal slice (or block) of the page. Depending on its configured {term}`Row Type` (which maps to a specific view template like `text-view`, `slider-view`, or `featured-view`), a row behaves differently and displays different information.
3.  **{term}`DynamicPageRowFeatured <Dynamic Page Row Featured>`**: A nested, child content type used *inside* a {term}`DynamicPageRow <Dynamic Page Row>`. Some row types, like an "Image Slider" or a "Features Grid", require multiple child items (the slides or the individual features). The {term}`DynamicPageRowFeatured <Dynamic Page Row Featured>` type serves as these individual sub-items, holding their own title, description, image, and link.

## The Magic of the Registry

The most powerful innovation of `cs_dynamicpages` is its dynamic field rendering, powered by the Plone Configuration Registry.

Normally, a Dexterity content type has a fixed set of fields. However, a "Text" row doesn't need an image upload field, and an "Image Slider" row has no use for a rich text body field. Creating dozens of separate content types for every possible block variation would clutter the "Add new..." menu and make the system difficult to maintain.

Instead, `cs_dynamicpages` takes a completely different approach:

1.  **A Single "Super" Content Type:** It uses just one {term}`DynamicPageRow <Dynamic Page Row>` type, which is packed with numerous optional Plone behaviors (`IRichText`, `IRelatedImage`, `IRowColumns`, `IExtraClass`, `IRowWidth`, etc.). In theory, a row has *all* possible fields.
2.  **Registry Mapping:** In the {term}`Dynamic Pages Registry` (Control Panel), each available {term}`Row Type` (view template) is registered alongside a specific subset of fields (`each_row_type_fields`). For example, the `text-view` only lists the `IRichTextBehavior.text` field, while hiding the image fields.
3.  **Dynamic Interception:** When an editor selects a {term}`Row Type` in the edit form (e.g., switching from "Text" to "Slider view"), the add-on dynamically intercepts the form and *only* displays the fields relevant to the selected view, hiding the rest.

This architecture keeps the authoring experience incredibly clean and intuitive—editors only see fields that actually matter for the layout they are building—while developers maintain a very simple, unified underlying content structure.
