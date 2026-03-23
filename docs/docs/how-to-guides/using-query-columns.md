---
myst:
  html_meta:
    "description": "How to use Query Columns to pull existing content into a dynamic page"
    "property=og:description": "How to use Query Columns"
    "property=og:title": "Using Query Columns"
    "keywords": "Plone, cs_dynamicpages, collections, query, dynamic content"
---

# Using Query Columns

While most row types in `cs_dynamicpages` require you to manually enter content (or add child {term}`Dynamic Page Row Featured` items), the **Query Columns View** is entirely automated. 

It behaves exactly like a Plone Collection. You define a search query, and the row automatically fetches matching content from across your site and displays it in a grid format. This is perfect for "Latest News", "Upcoming Events", or "Featured Products" sections.

## Step 1: Add a Query Columns Row

1. Inside your {term}`Dynamic Page Folder`, click **Add new...** -> **Dynamic Page Row**.
2. Change the **Row Type** to **Query columns view**.
   * *The form will instantly update to show the Collection query widget.*
3. Enter a **Title** (e.g., "Latest News").

## Step 2: Configure the Query

The core of this row type is the `plone.collection` behavior.

1. Scroll to the **Search terms** section.
2. Select your criteria. For example, to show only News Items:
   * Field: `Type`
   * Operator: `Any`
   * Value: `News Item`
3. Click **Add Criteria**.
4. Set the **Sort on** field to `Effective date` and **Sort order** to `Reverse` to show the newest items first.
5. Set **Limit** to `3` (so you only show the three most recent articles).

## Step 3: Configure the Grid

Because this is a column-based view, you need to tell it how many columns to use.

1. Locate the **Columns** field.
2. Enter the number of columns you want. For a limit of 3 items, entering `3` columns will create a perfect single row of news cards.

## Step 4: Save and View

Click **Save**. The row will now dynamically query the catalog and render the resulting News Items as cards within the grid layout. Whenever a new News Item is published elsewhere on the site, this row will automatically update without any manual intervention!
