/**
 * JavaScript for DynamicPageRow edit form
 * Loads configuration from control panel and applies it to the form
 */

(function ($) {
  "use strict";

  function initialize() {
    // Only run on DynamicPageRow edit form
    if (
      !$("body.template-edit").length ||
      !$("body.portaltype-dynamicpagerow").length
    ) {
      return;
    }

    // Get configuration from control panel
    let base_url = $("body").data("portal-url");
    $.ajax({
      url: `${base_url}/@registry/cs_dynamicpages.dynamica_pages_control_panel.row_type_fields`,
      type: "GET",
      dataType: "json",
      headers: {
        Accept: "application/json",
      },
    })
      .done(function (data) {
        if (data.length > 0) {
          processRowTypeFields(data);
        }
      })
      .fail(function (error) {
        console.error("Error loading row type fields:", error);
      });
  }

  // Store row type configurations globally
  let rowTypeConfigs = {};

  function processRowTypeFields(rowTypeFields) {
    // Store all row type configurations
    rowTypeFields.forEach(function (rowTypeConfig) {
      rowTypeConfigs[rowTypeConfig.row_type] = {
        fields: rowTypeConfig.each_row_type_fields || [],
      };
    });

    // Initial setup
    updateFieldVisibility();
  }

  function updateFieldVisibility() {
    const rowTypeSelect = $('select[name$=".row_type:list"]');
    if (!rowTypeSelect.length) return;

    function toggleFields() {
      const selectedRowType = rowTypeSelect.val();
      if (!selectedRowType) return;

      const config = rowTypeConfigs[selectedRowType];

      // Always show the row type select
      rowTypeSelect.closest(".field").show();

      if (!config || !config.fields || config.fields.length === 0) {
        // If no configuration for this row type, show all fields
        $(".field").show();
      } else {
        // Otherwise, show only the configured fields
        // First hide all fields except the row type select
        $(".field").not(rowTypeSelect.closest(".field")).hide();

        // Show the fields for the selected row type
        config.fields.forEach(function (fieldName) {
          $(`[data-fieldname$="form.widgets.${fieldName}"]`)
            .closest(".field")
            .show();
        });
      }
    }

    // Initial setup
    toggleFields();

    // Update on change
    rowTypeSelect
      .off("change.rowTypeChange")
      .on("change.rowTypeChange", toggleFields);
  }

  $(document).ready(initialize);
})(jQuery);
