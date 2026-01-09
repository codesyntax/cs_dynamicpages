/**
 * JavaScript for DynamicPageRow edit form
 * Loads configuration from control panel and applies it to the form
 */

(function () {
  "use strict";

  // Store row type configurations globally
  let rowTypeConfigs = {};
  let rowTypeSelect = null;

  function initialize(context = document) {
    // Check if we're in an edit form or an add form
    const isEditForm =
      context === document &&
      document.body.classList.contains("template-edit") &&
      document.body.classList.contains("portaltype-dynamicpagerow");

    // Check if we're in an add form or a dynamically added form
    const isAddForm = (context === document ? document : context).querySelector(
      "form.view-name-add-DynamicPageRow"
    );

    if (!isEditForm && !isAddForm) {
      return;
    }

    // Get configuration from control panel
    const baseUrl = document.body.dataset.portalUrl || "";
    fetch(
      `${baseUrl}/@registry/cs_dynamicpages.dynamic_pages_control_panel.row_type_fields`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
        credentials: "same-origin",
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data && data.length > 0) {
          processRowTypeFields(data);
        }
      })
      .catch((error) => {
        console.error("Error loading row type fields:", error);
      });
  }

  function processRowTypeFields(rowTypeFields) {
    // Store all row type configurations
    rowTypeFields.forEach((rowTypeConfig) => {
      rowTypeConfigs[rowTypeConfig.row_type] = {
        fields: rowTypeConfig.each_row_type_fields || [],
      };
    });

    // Initial setup
    updateFieldVisibility();
  }

  function updateFieldVisibility() {
    rowTypeSelect = document.querySelector('select[name$=".row_type:list"]');
    if (!rowTypeSelect) return;

    // Remove previous event listener if it exists
    const newSelect = rowTypeSelect.cloneNode(true);
    rowTypeSelect.parentNode.replaceChild(newSelect, rowTypeSelect);
    rowTypeSelect = newSelect;

    // Add new event listener
    rowTypeSelect.addEventListener("change", toggleFields);

    // Initial setup - force update for the default value
    toggleFields();
  }

  function toggleFields() {
    const selectedRowType = rowTypeSelect.value;
    if (!selectedRowType) return;

    const config = rowTypeConfigs[selectedRowType];
    const allFields = document.querySelectorAll(".field");
    const rowTypeField = rowTypeSelect.closest(".field");

    // Define default Plone fields that should always be visible
    const alwaysVisibleFieldIds = [
      "formfield-form-widgets-IExcludeFromNavigation-exclude_from_nav",
      "formfield-form-widgets-IShortName-id",
      "formfield-form-widgets-IOwnership-creators",
      "formfield-form-widgets-IOwnership-contributors",
      "formfield-form-widgets-IOwnership-rights",
      "formfield-form-widgets-IPublication-effective",
      "formfield-form-widgets-IPublication-expires",
      "formfield-form-widgets-ICategorization-subjects",
      "formfield-form-widgets-ICategorization-language",
    ];

    // Hide all fields except the row type selector and the always-visible ones
    allFields.forEach((field) => {
      // Check if the field is the row type selector or if its ID is in the always-visible list
      const isAlwaysVisible = alwaysVisibleFieldIds.includes(field.id);

      if (field !== rowTypeField && !isAlwaysVisible) {
        field.style.display = "none";
      } else {
        // Ensure the always-visible fields and the selector are displayed
        field.style.display = "";
      }
    });

    // If we have a config for this row type, show its fields
    if (config && config.fields && config.fields.length > 0) {
      config.fields.forEach((fieldName) => {
        // Try different field name patterns to match the actual field in the form
        const fieldSelectors = [
          `[data-fieldname$="form.widgets.${fieldName}"]`,
          `[data-fieldname$="form.widgets.I${fieldName}"]`,
          `[data-fieldname*="${fieldName}"]`,
          `#formfield-form-widgets-${fieldName}`,
          `#formfield-form-widgets-I${fieldName}`,
        ];

        for (const selector of fieldSelectors) {
          const fieldElement = document.querySelector(selector);
          if (fieldElement) {
            const fieldContainer = fieldElement.closest(".field");
            if (fieldContainer) {
              fieldContainer.style.display = "";
              break; // Found and showed the field, no need to check other selectors
            }
          }
        }
      });
    } else if (selectedRowType === "horizontal-row-type") {
      // If no config but we're on the default type, show all fields
      allFields.forEach((field) => {
        field.style.display = "";
      });
    }

    // After toggling fields, check for empty fieldsets and hide them
    updateFieldsetAndTabVisibility();
  }

  function updateFieldsetAndTabVisibility() {
    const allFieldsets = document.querySelectorAll("fieldset");
    const allTabLinks = document.querySelectorAll("a.autotoc-level-1");

    allFieldsets.forEach((fieldset, index) => {
      // Find all direct .field children that are currently visible
      const visibleFields = fieldset.querySelectorAll(
        ".field:not([style*='display: none'])"
      );

      const hasVisibleFields = Array.from(visibleFields).some(
        (field) => field.style.display !== "none"
      );

      // Hide or show the fieldset based on whether it has visible fields
      fieldset.style.display = hasVisibleFields ? "" : "none";

      // Also hide/show the corresponding autotoc tab/link based on its order
      const tabLink = allTabLinks[index];
      if (tabLink) {
        tabLink.style.display = hasVisibleFields ? "" : "none";
      }
    });
  }

  // Initialize when DOM is fully loaded
  function start() {
    initialize();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
