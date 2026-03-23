---
myst:
  html_meta:
    "description": "How to create a custom row view"
    "property=og:description": "How to create a custom row view"
    "property=og:title": "Create a Custom Row View"
    "keywords": "Plone, cs_dynamicpages, developer, custom view, row type"
---

# Create a Custom Row View

The true power of `cs_dynamicpages` is its extensibility. As a developer, if the built-in row types (Text, Slider, Features, etc.) do not meet your design requirements, you can easily create and register your own custom view.

This guide will walk you through creating a "Video Embed" row type.

## 1. Create the Page Template

First, we need a standard Plone browser view template to render the row.

In your add-on (e.g., `my.addon`), create a new template `video_embed_view.pt` inside your `browser` or `views` directory.

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="cs_dynamicpages"
      metal:use-macro="context/main_template/macros/master">

<body>
  <metal:content-core fill-slot="content-core">
    <div tal:attributes="class python:' '.join(filter(None, [
           'row-video-embed',
           context.width,
           context.extra_class,
           context.padding_top,
           context.padding_bottom,
           context.margin_top,
           context.margin_bottom
         ]))">
      
      <h2 tal:condition="context.title" tal:content="context.title">Video Title</h2>
      <p tal:condition="context.description" tal:content="context.description">Description</p>

      <!-- Here we assume the user enters an iframe or URL into the text field -->
      <div class="video-container" 
           tal:condition="context.text" 
           tal:content="structure context.text.output">
        [Video iframe goes here]
      </div>

    </div>
  </metal:content-core>
</body>
</html>
```

## 2. Register the View in ZCML

Next, register the view in your `configure.zcml` so Plone knows it exists. It is important to bind it specifically to the `IDynamicPageRow` interface.

```xml
<browser:page
    name="myaddon-video-embed-view"
    for="cs_dynamicpages.content.dynamic_page_row.IDynamicPageRow"
    template="video_embed_view.pt"
    permission="zope2.View"
    layer="my.addon.interfaces.IMyAddonLayer"
    />
```

## 3. Register the View in the Control Panel

Currently, Plone knows the view exists, but `cs_dynamicpages` doesn't know it should be available as a "Row Type" in the edit form dropdown, nor does it know which fields it requires.

You must register it in the {term}`Dynamic Pages Registry` (`IDynamicPagesControlPanel`). The best way to do this is via a `registry.xml` file in your GenericSetup profile (e.g., `profiles/default/registry.xml`).

```xml
<?xml version="1.0"?>
<registry xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          i18n:domain="cs_dynamicpages">

  <!-- Append our new view to the existing row_type_fields record -->
  <record name="cs_dynamicpages.dynamic_pages_control_panel.row_type_fields">
    <value purge="False">
      <element>
        <!-- The ZCML name of your view -->
        <key name="row_type">myaddon-video-embed-view</key>
        
        <!-- The icon to display in the dropdown (Bootstrap/Plone icon name) -->
        <key name="row_type_icon">play-btn</key>
        
        <!-- Does it need the 'Add Featured' button for child items? -->
        <key name="row_type_has_featured_add_button">False</key>
        
        <!-- The exact list of fields to expose when this view is selected -->
        <key name="each_row_type_fields">
          <element>IBasic.title</element>
          <element>IBasic.description</element>
          <element>IRichTextBehavior-text</element>
          <element>IRowWidth.width</element>
          <element>IExtraClass.extra_class</element>
          <element>IRowVerticalSpacing.padding_top</element>
          <element>IRowVerticalSpacing.padding_bottom</element>
          <element>IRowVerticalSpacing.margin_top</element>
          <element>IRowVerticalSpacing.margin_bottom</element>
        </key>
      </element>
    </value>
  </record>

</registry>
```

### Understanding the Registration

* `purge="False"`: This is critical. It ensures your new row type is *added* to the list, rather than overwriting all the default `cs_dynamicpages` row types.
* `each_row_type_fields`: This array dictates exactly which fields are visible. Notice how we use `IRichTextBehavior-text` to capture the video iframe embed code, but we omitted `IRelatedImage.related_image` because a video row doesn't need an image upload.

## 4. Apply the Profile

Restart your Plone instance and re-install your add-on (or import the Registry step via the ZMI/portal_setup). 

When you add or edit a {term}`DynamicPageRow <Dynamic Page Row>`, you will now see **myaddon-video-embed-view** in the "Row type" dropdown, and selecting it will instantly filter the form to show only the Title, Description, Text, and Spacing fields!
