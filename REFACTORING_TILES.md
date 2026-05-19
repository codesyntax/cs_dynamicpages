# Refactoring Plan: Transition to `plone.tiles`

**Goal**: Replace the custom "Row Type" logic with a standardized Tile-based approach while maintaining independent workflows and publication dates for each row.

## 1. Architecture Summary
- **Data Model**: Keep **Dexterity Objects** as "Row" containers to preserve workflows and permissions.
- **Persistence**: Layout settings (width, spacing, etc.) and content (text, links) move into **Persistent Tile Data** (Annotations).
- **Types**: Move from one generic `DynamicPageRow` to **specific content types** (e.g., `TextRow`, `SliderRow`, `FeaturedRow`).
- **Rendering**: Each row type will have its corresponding **Tile** registered as its **Default View**.
- **UI**: Custom "Plus" button menu updated to create these specific types and use standard `@@edit-tile` forms.

## 2. Technical Components

### A. Tiles & Schemas
- **Base Layout Schema**: Defines common settings (Row width, Vertical spacing, Extra CSS classes).
- **Specific Schemas**: Each functionality (Text, Slider, Gallery) gets its own schema with specific fields.
- **Persistent Tiles**: Python classes that handle fetching data from annotations and rendering the template.
- **Bootstrap Wrappers**: Tiles are "self-contained," templates render the `<div class="col-md-X">` wrappers based on their own configuration.

### B. Dexterity Types
- New FTIs (Factory Type Information) for each row variant.
- Set the `default_view` of these FTIs to the corresponding Tile name.

### C. Main Page View
- `DynamicView` simplified to render the row objects, allowing Plone's `default_view` mechanism to invoke the Tiles.

### D. Editing & Add Logic
- Update custom JS offcanvas menu to create the correct row type in the background.
- Redirect "Edit" button to `context/@@edit-tile/tile.name/default`.

## 3. Implementation Steps
1. **Tile Setup**: Create the `tiles` package and define the base `ITileLayoutSchema`.
2. **Schema Migration**: Port current behavior fields into Tile schemas.
3. **Tile Implementation**: Create the `.py` classes and `.pt` templates.
4. **Registration**: Register tiles in ZCML and define new Dexterity types.
5. **UI Updates**: Modify Bootstrap offcanvas and JS for new workflow.
6. **Migration Script**: Upgrade step to convert existing `DynamicPageRow` objects and migrate data.

## 4. Verification
- **Unit Tests**: Verify Tile data persistence.
- **Functional Tests**: Verify `@@edit-tile` form updates rendering.
- **Integration**: Confirm "Add Row" menu creates new types.
