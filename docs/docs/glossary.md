---
myst:
  html_meta:
    "description": "Terms and definitions used throughout the cs_dynamicpages documentation."
    "property=og:description": "Terms and definitions used throughout the cs_dynamicpages documentation."
    "property=og:title": "Glossary"
    "keywords": "Plone, documentation, glossary, term, definition, dynamicpages"
---

This glossary provides terms and definitions relevant to **cs_dynamicpages**.

(glossary-label)=

# Glossary

```{glossary}
:sorted: true

Dynamic Page Folder
    The top-level container content type (`DynamicPageFolder`) that represents an entire landing page. It acts as the wrapper holding all the individual rows that compose the page layout.

Dynamic Page Row
    A single horizontal block (`DynamicPageRow`) of a dynamic page. A row can display text, images, sliders, or collection grids depending on its configured {term}`Row Type`.

Dynamic Page Row Featured
    A child content type (`DynamicPageRowFeatured`) placed *inside* a {term}`Dynamic Page Row`. These are used when a row requires multiple distinct elements to function, such as the individual slides in a Slider view or the expandable panels in an Accordion view.

Row Type
    The specific view template assigned to a {term}`Dynamic Page Row` (e.g., `slider-view`, `text-view`, `features-view`). The Row Type dictates not only how the row looks on the frontend, but also which fields are exposed in the edit form.

Dynamic Pages Registry
    The Plone configuration registry specific to `cs_dynamicpages` (accessible via the Site Setup Control Panel). It is the central nervous system of the add-on, defining which fields belong to which {term}`Row Type`, and defining the global CSS utility classes for widths, margins, and paddings.

Plone
    [Plone](https://plone.org/) is an open-source content management system that is used to create, edit, and manage digital content.

```
