# Refactoring Plan: Separate Dexterity Content Types for cs_dynamicpages

## Goal
Replace the current "God-object" pattern (`DynamicPageRow`) with separate, specific Dexterity content types to improve maintainability, eliminate complex field-toggling JavaScript, and leverage standard Plone features like workflows and schemas.

## Proposed New Structure

### 1. Row Types (Added to DynamicPageFolder)
- **TitleDescriptionRow**: Simple row with title and description.
- **FeaturedRow**: Row with image and link.
- **FeaturedOverlayRow**: Row with image as background and text overlay.
- **HorizontalRuleRow**: Simple horizontal line.
- **SpacerRow**: Adjustable vertical space.
- **SliderRow**: Container for Slider Items.
- **FeaturesRow**: Container for Feature Cards.
- **AccordionRow**: Container for Accordion Items.
- **QueryColumnsRow**: Row that pulls content via a Collection query.
- **TextRow**: Rich Text row.

### 2. Item Types (Added to specific Rows)
- **SliderItem**: Allowed only in `SliderRow`.
- **FeatureItem**: Allowed only in `FeaturesRow`.
- **AccordionItem**: Allowed only in `AccordionRow`.

## Step-by-Step Implementation

### Phase 1: Architectural Scaffolding
- [ ] Define base interfaces in `src/cs_dynamicpages/interfaces.py` (`IDynamicRow`, `IDynamicItem`).
- [ ] Refactor existing classes in `src/cs_dynamicpages/content/` to provide common base logic.

### Phase 2: Content Type Definitions
- [ ] Create FTI XML files for all new Row and Item types in `src/cs_dynamicpages/profiles/default/types/`.
- [ ] Register new types in `types.xml`.
- [ ] Configure `allowed_content_types` to enforce the strict hierarchy.

### Phase 3: Behaviors & Schema
- [ ] Map shared behaviors (`IRowWidth`, `IRowVerticalSpacing`, etc.) to the new types.
- [ ] Ensure specific fields for each type are defined in their respective schemas/interfaces.

### Phase 4: View & Template Mapping
- [ ] Register default `view` for each new type in `src/cs_dynamicpages/views/configure.zcml`.
- [ ] Reuse existing Page Templates.
- [ ] Clean up View classes from `row_type` logic.

### Phase 5: Cleanup
- [ ] Deprecate old `DynamicPageRow` types.
- [ ] Update or disable the JS field-toggling logic for new types.
- [ ] Update control panel documentation.

## Success Criteria
- [ ] All new types are addable in the correct locations.
- [ ] Schemas show only relevant fields without JS intervention.
- [ ] Existing views work correctly with new types.
- [ ] `make test` passes.
