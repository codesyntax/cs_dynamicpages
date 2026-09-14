# Plan: Enhanced Nested Row Management UX

## Goal
Improve the editor experience for nested rows by making structural controls (Add, Edit, Delete) available recursively. This will allow adding rows directly into nested containers (like sliders or accordions) using a unified, robust Offcanvas approach without introducing complex JavaScript.

## Branch
`feature/nested-row-management-ux`

## Technical Approach

### 1. Backend: Contextual Creation
*   **Target**: `src/cs_dynamicpages/views/dynamic_page_folder_view.py`
*   **Changes**: Restore `container` parameter support in `DynamicPageAddRowContentView`.
*   **Logic**: Use `uuidToObject(container_uid)` to determine the parent for the new `DynamicPageRow`. Redirect to the nearest parent with a `dynamic-view` display.

### 2. Macros: Unified UI Components
*   **Target**: `src/cs_dynamicpages/views/macros.pt`
*   **Components**:
    *   `add_row_button`: Standardized button with `data-bs-toggle="offcanvas"` and `data-bs-target="#addrow-offcanvasRight"`. Parameters: `container_uid`, `position`, `is_nested`.
    *   `row_management_icons`: Standardized Pen (Edit) and Trash (Delete confirmation) links.

### 3. Templates: Enabling Recursive Addition
*   **Top Level**: Update `dynamic_view.pt` to use the `add_row_button` macro.
*   **Sub-views**: Update `accordion_view.pt`, `slider_view.pt`, and `features_view.pt` to:
    *   Iterate through their children.
    *   Render an `add_row_button` macro after each child item, passing the current row's UID as the container.
    *   This allows inserting rows *between* existing nested items.

### 4. JavaScript: Robust State Sync
*   **Target**: `src/cs_dynamicpages/browser/static/add-row-position.js`
*   **Logic**:
    1.  Listen for `show.bs.offcanvas` on `#addrow-offcanvasRight`.
    2.  Extract `container` and `position` from `event.relatedTarget` (the clicked button).
    3.  Update all "Add" links inside the offcanvas with these parameters.
*   **Why**: Official Bootstrap 5 lifecycle usage prevents the `backdrop` undefined errors seen in nested DOMs.

### 5. CSS: Visual Depth
*   **Target**: `src/cs_dynamicpages/browser/static/dynamicpageview.css`
*   **Changes**:
    *   Discreet styling for nested `+` buttons (smaller scale).
    *   Visual cues (indents or subtle borders) for nested management areas.

---

## Verification Plan
1.  Run `make check` and `make test`.
2.  Manual test: Create an Accordion, then add a Slider inside one of its panels using the inline UI.
3.  Manual test: Verify that reordering works for top-level rows and that nested rows can be edited/deleted individually.
