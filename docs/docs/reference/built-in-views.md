---
myst:
  html_meta:
    "description": "cs_dynamicpages Built-in Views"
    "property=og:description": "cs_dynamicpages Built-in Views"
    "property=og:title": "Built-in Views"
    "keywords": "Plone, cs_dynamicpages, reference, views, row types"
---

# Built-in Views

`cs_dynamicpages` comes pre-packaged with several **{term}`Row Types <Row Type>`** (views) that handle common landing page patterns. 

Each row type is configured by default in the **{term}`Dynamic Pages Registry`** to expose a specific subset of fields in the edit form, and to display a specific icon. Some rows also support adding child rows if they require multiple elements (like sliders or grids).

Below is the reference of all default built-in views, the fields they expose, and whether they accept nested rows.

---

## Typography & Text

### Text View
* **ID:** `cs_dynamicpages-text-view`
* **Icon:** `body-text`
* **Description:** A standard rich text block.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Width, Extra Class, Rich Text (Body), Vertical Spacing (Margins/Paddings).

### Title & Description View
* **ID:** `cs_dynamicpages-title-description-view`
* **Icon:** `fonts`
* **Description:** A simple header block displaying just the title and a short description, useful for section headers.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Description, Width, Extra Class, Vertical Spacing (Margins/Paddings).

---

## Layout & Separators

### Spacer View
* **ID:** `cs_dynamicpages-spacer-view`
* **Icon:** `arrows-vertical`
* **Description:** An invisible row used purely to add vertical whitespace between other rows.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Extra Class, Vertical Spacing (Margins/Paddings).

### Horizontal Rule View
* **ID:** `cs_dynamicpages-horizontal-rule-view`
* **Icon:** `hr`
* **Description:** A simple `<hr>` separator to visually divide sections.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Width, Extra Class, Vertical Spacing (Margins/Paddings).

---

## Media & Features

### Featured View
* **ID:** `cs_dynamicpages-featured-view`
* **Icon:** `card-image`
* **Description:** A standard "hero" or "call to action" block featuring a title, description, an image, and a button.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Description, Width, Extra Class, Related Image, Fetch Priority Image, Image Position, Link Text, Link URL, Vertical Spacing (Margins/Paddings).

### Featured Overlay View
* **ID:** `cs_dynamicpages-featured-overlay-view`
* **Icon:** `image-fill`
* **Description:** Similar to the Featured View, but the text is overlaid on top of a background image.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Description, Width, Extra Class, Related Image, Fetch Priority Image, Link Text, Link URL, Vertical Spacing (Margins/Paddings).

---

## Collections & Grids

### Slider View
* **ID:** `cs_dynamicpages-slider-view`
* **Icon:** `images`
* **Description:** A carousel that rotates through child rows.
* **Allows Nested Rows:** **Yes** (You add child {term}`DynamicPageRow <Dynamic Page Row>` items to create the slides).
* **Exposed Fields:** Title, Width, Extra Class, Fetch Priority Image, Vertical Spacing (Margins/Paddings).

### Features View
* **ID:** `cs_dynamicpages-features-view`
* **Icon:** `grid`
* **Description:** Displays child rows in a multi-column grid layout (e.g., 3 columns of features/services).
* **Allows Nested Rows:** **Yes** (You add child {term}`DynamicPageRow <Dynamic Page Row>` items to create the grid blocks).
* **Exposed Fields:** Title, Width, Columns, Extra Class, Fetch Priority Image, Vertical Spacing (Margins/Paddings).

### Accordion View
* **ID:** `cs_dynamicpages-accordion-view`
* **Icon:** `chevron-double-down`
* **Description:** Displays child rows in a collapsible accordion (often used for FAQs).
* **Allows Nested Rows:** **Yes** (You add child {term}`DynamicPageRow <Dynamic Page Row>` items to create the accordion panels).
* **Exposed Fields:** Title, Width, Extra Class, Vertical Spacing (Margins/Paddings).

### Query Columns View
* **ID:** `cs_dynamicpages-query-columns-view`
* **Icon:** `funnel`
* **Description:** Acts like a Collection. It queries existing content in the site and displays the results in a grid.
* **Allows Nested Rows:** No
* **Exposed Fields:** Title, Width, Extra Class, Query parameters (query, sort_on, sort_order, limit), Columns, Fetch Priority Image, Vertical Spacing (Margins/Paddings).
