---
myst:
  html_meta:
    "description": "Tutorial: Building your first Dynamic Page"
    "property=og:description": "Tutorial: Building your first Dynamic Page"
    "property=og:title": "Your first Dynamic Page"
    "keywords": "Plone, cs_dynamicpages, tutorial, landing page"
---

# Your first Dynamic Page

In this tutorial, you will learn the fundamental workflow for building a dynamic landing page in Plone using the `cs_dynamicpages` add-on. We will create a new homepage from scratch consisting of a hero banner, a text section, and a sliding gallery.

By the end of this tutorial, you will understand how to:
* Create a **Dynamic Page** container.
* Add and configure different **Rows**.
* Add nested, **Featured** content inside complex rows (like sliders or grids).

---

## Step 1: Create the Dynamic Page Folder

The foundation of any dynamic page is the {term}`Dynamic Page Folder`. Think of this as the main "wrapper" or the "page" itself.

1. Navigate to the location in your Plone site where you want to build the page (e.g., the root of the site).
2. From the Plone toolbar, open the **Add new...** menu and select **Dynamic Page Folder**.
3. **Title:** Enter `Welcome to our new site`.
4. **Summary:** (Optional) Enter a brief description. This is used for SEO and when the page appears in search results.
5. Click **Save**.

You now have an empty canvas. Let's start adding content!

---

## Step 2: Add a "Hero" Banner Row

The first thing visitors should see is a large, striking header section. We will use a {term}`Dynamic Page Row` configured as a **Featured View**.

1. Make sure you are viewing the `Welcome to our new site` page you just created.
2. From the toolbar, open the **Add new...** menu and select **Dynamic Page Row**.
3. **Row Type:** The most important field! Change the dropdown from "Horizontal Rule View" to **Featured view**.
   * *Notice what happens! As soon as you change the Row Type, the available fields instantly update to match your choice.*
4. **Title:** Enter `Discover the future`.
5. **Description:** Enter `We are building amazing things with Plone.`.
6. **Related Image:** Upload a high-quality, wide background image.
7. **Image Position:** Choose whether the image should appear on the left, right, or top of the text.
8. **Link Text:** Enter `Learn More`.
9. **Link URL:** Enter `/about-us` (or a full `https://...` URL).
10. **Width:** Leave it at `Full width`.
11. Click **Save**.

You have just created the first slice of your page.

---

## Step 3: Add a Text Section

Next, let's add a standard paragraph of text below the hero banner.

1. Navigate back to the main `Welcome to our new site` folder (you can click the breadcrumb).
2. Open the **Add new...** menu and select **Dynamic Page Row**.
3. **Row Type:** Select **Text view**.
   * *The image upload fields disappear, and a Rich Text editor appears.*
4. **Title:** Enter `Our Mission`.
5. **Text:** Write a few paragraphs explaining your organization.
6. **Width:** Change this to **Centered** (or your equivalent narrowed class) so the text is easier to read.
7. Click **Save**.

Now you have two rows stacked vertically: a Featured hero and a Text block.

---

## Step 4: Create an Image Slider (Rows with Children)

Some rows, like sliders, grids, or accordions, require multiple distinct items inside them. We build these by adding a row, and then adding {term}`Dynamic Page Row Featured` items *inside* that row.

Let's build a slider with three images.

### 4.1. Create the Slider Row Wrapper

1. Navigate back to the main `Welcome to our new site` folder.
2. Open the **Add new...** menu and select **Dynamic Page Row**.
3. **Row Type:** Select **Slider view**.
4. **Title:** Enter `Our Gallery`.
5. **Padding top / Padding bottom:** Let's add some breathing room. Select `5` for both top and bottom padding.
6. Click **Save**.

You now have a Slider row, but it's empty! We need to add slides.

### 4.2. Add Slides to the Slider

1. Look at the view of the Slider row you just saved. Because this row type is configured to accept children, you will see a special **Add Featured** button (or you can use the standard Plone toolbar: **Add new... > Dynamic Page Row Featured**).
2. Click **Add Featured**.
3. **Title:** Enter `Slide 1: The Team`.
4. **Related Image:** Upload the first image.
5. Click **Save**.
6. Repeat steps 2-5 twice more, creating "Slide 2" and "Slide 3" with different images.

---

## Step 5: Admire Your Work

1. Navigate back to the main `Welcome to our new site` folder.
2. The default view of the folder automatically renders all of its children (the rows) in order.
3. You should see:
   * The **Featured view** hero block at the top.
   * The **Text view** block in the middle, nicely centered.
   * The **Slider view** at the bottom, automatically cycling through the three featured slides you added inside it.

If you need to reorder the rows, simply use Plone's standard **Contents** view (folder contents) on the {term}`DynamicPageFolder <Dynamic Page Folder>` and drag-and-drop the rows into your preferred sequence.

**Congratulations!** You have built your first dynamic page.
