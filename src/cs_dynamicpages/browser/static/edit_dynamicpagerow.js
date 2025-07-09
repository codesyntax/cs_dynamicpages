/**
 * JavaScript for DynamicPageRow edit form
 * Loads configuration from control panel and applies it to the form
 */

(function() {
  "use strict";

  // Store row type configurations globally
  let rowTypeConfigs = {};
  let rowTypeSelect = null;

  function initialize() {
    // Only run on DynamicPageRow edit form
    if (!document.body.classList.contains('template-edit') || 
        !document.body.classList.contains('portaltype-dynamicpagerow')) {
      return;
    }

    // Get configuration from control panel
    const baseUrl = document.body.dataset.portalUrl || '';
    fetch(`${baseUrl}/@registry/cs_dynamicpages.dynamica_pages_control_panel.row_type_fields`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      credentials: 'same-origin'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data && data.length > 0) {
        processRowTypeFields(data);
      }
    })
    .catch(error => {
      console.error('Error loading row type fields:', error);
    });
  }

  function processRowTypeFields(rowTypeFields) {
    // Store all row type configurations
    rowTypeFields.forEach(rowTypeConfig => {
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
    rowTypeSelect.addEventListener('change', toggleFields);

    // Initial setup
    toggleFields();
  }

  function toggleFields() {
    const selectedRowType = rowTypeSelect.value;
    if (!selectedRowType) return;

    const config = rowTypeConfigs[selectedRowType];
    const allFields = document.querySelectorAll('.field');
    const rowTypeField = rowTypeSelect.closest('.field');

    // Show all fields first
    allFields.forEach(field => {
      field.style.display = '';
    });

    if (config && config.fields && config.fields.length > 0) {
      // Hide all fields except row type select
      allFields.forEach(field => {
        if (field !== rowTypeField) {
          field.style.display = 'none';
        }
      });

      // Show only the configured fields
      config.fields.forEach(fieldName => {
        const fieldElement = document.querySelector(
          `[data-fieldname$="form.widgets.${fieldName}"]`
        );
        if (fieldElement) {
          const fieldContainer = fieldElement.closest('.field');
          if (fieldContainer) {
            fieldContainer.style.display = '';
          }
        }
      });
    }
    // If no config, all fields remain visible
  }

  // Initialize when DOM is fully loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})();
