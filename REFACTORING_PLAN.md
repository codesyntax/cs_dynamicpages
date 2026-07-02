# Refactoring Plan: Infinite Nesting via DynamicPageRow

## Goal
Eliminate the redundant `DynamicPageRowFeatured` content type by making `DynamicPageRow` folderish and self-nesting. This enables infinite nesting (e.g., tabs inside accordions) while maintaining the current inline editing UX.

## Strategy: Parallel Evolution
We will keep the current UX (inline buttons, drag-and-drop handles) throughout the transition. The enhanced JS navigator is deferred to a separate, future project.

---

## Phase 1: Backend & Schema
1. **Enable Nesting**: Update `DynamicPageRow` FTI to allow `DynamicPageRow` as a child. (✅ Done)
2. **Behavior Parity**: Ensure `DynamicPageRow` has all behaviors present in `DynamicPageRowFeatured`. (✅ Done)
3. **Control Panel**: Update "Has Featured Add Button" logic to generically mean "Has Children". (✅ Done)

## Phase 2: Recursive Rendering
1. **Update Sub-views**: Modify `slider_view.pt`, `accordion_view.pt`, and `features_view.pt` to render children recursively. (✅ Done)
2. **Dynamic View**: Ensure `dynamic_view.pt` correctly iterates and displays the nested structure. (✅ Done)
3. **Recursion Safety**: Implement `render_stack` in `DynamicPageRow.render()` to prevent infinite loops and server crashes. (✅ Done)

## Phase 3: Legacy UX Support
1. **Nesting via "+" Button**: Use direct Plone add links (`++add++DynamicPageRow`) for nested additions to avoid JS complexity. (✅ Done)
2. **JS Verification**: Revert `reorder-rows.js` and `add-row-position.js` to original states to ensure top-level stability. (✅ Done)
3. **Management Icons**: Add direct links for "Edit" and "Delete" next to nested rows for easy access. (✅ Done)

## Phase 4: Migration & Cleanup
1. **Upgrade Step**: Implement migration script `1011` to convert `DynamicPageRowFeatured` to `DynamicPageRow`, intelligently assigning primitive row types based on parent context and registering new row types in the Plone registry. (✅ Done)
2. **Type Deletion**: Remove all `DynamicPageRowFeatured` code, XML, and tests. (✅ Done)
3. **API Alignment**: Update `DynamicPageRow.nested_rows()` (formerly `featured_list()`) to query the correct content type. (✅ Done)
4. **Terminology Unification**: Rename "featured" fields/methods to "child" or "nested" where possible. (✅ Done)
5. **Clean Legacy Files**: Delete obsolete robot tests. (✅ Done)

## Phase 5: Documentation & Standards
1. **Documentation Overhaul**: Update `README.md` and `docs/` to reflect the new single-type architecture. (⏳ Pending)
2. **Internationalization**: Run `make i18n` to sync translation strings. (⏳ Pending)
3. **Final Verification**: Run `make check`, `make test`, and manually verify nesting UI. (⏳ Pending)

---

## Phase 6: Enhanced Navigator (Separate Project)
*Deferred: To be implemented only after the legacy-UX nesting is stable.*
