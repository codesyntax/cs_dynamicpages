/**
 * Handles reordering of dynamic page rows
 */

(function () {
  "use strict";

  // Initialize when DOM is loaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRowReordering);
  } else {
    initRowReordering();
  }

  function initRowReordering() {
    // Only run on dynamic-view with edit permissions
    if (
      !document.body.classList.contains("template-dynamic-view") ||
      !document.body.classList.contains("userrole-manager")
    ) {
      console.log(
        "Not in dynamic-view edit mode, skipping row reordering initialization"
      );
      return;
    }

    console.log("Initializing row reordering...");
    // Find all move up/down buttons
    const moveUpButtons = document.querySelectorAll('a[data-action="move-up"]');
    const moveDownButtons = document.querySelectorAll(
      'a[data-action="move-down"]'
    );
    console.log(
      `Found ${moveUpButtons.length} move-up buttons and ${moveDownButtons.length} move-down buttons`
    );

    // Add event listeners to move up buttons
    moveUpButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("Move up button clicked");
        const row = this.closest(".dynamic-row");
        console.log(`Moving row with ID: ${row.dataset.rowid} up`);
        moveRow(row, -1);
      });
    });

    // Add event listeners to move down buttons
    moveDownButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("Move down button clicked");
        const row = this.closest(".dynamic-row");
        console.log(`Moving row with ID: ${row.dataset.rowid} down`);
        moveRow(row, 1);
      });
    });
  }

  function moveRow(row, delta) {
    const rowId = row.dataset.rowid;
    if (!rowId) {
      const errorMsg = "No data-row-id attribute found on row";
      console.error(errorMsg);
      alert(errorMsg);
      return;
    }

    console.log(`Preparing to move row ${rowId} with delta ${delta}`);

    const baseUrl = row.dataset.rowsurl || "";
    console.log(`Sending request to: ${baseUrl}`);

    const requestBody = {
      ordering: {
        obj_id: rowId,
        delta: delta,
      },
    };

    console.log("Request payload:", JSON.stringify(requestBody, null, 2));

    fetch(baseUrl, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(requestBody),
      credentials: "same-origin",
    }).then((response) => {
      console.log(`Received response with status: ${response.status}`);
      console.log("Response headers:", response.headers);
      console.log("Response ok:", response.ok);
      if (!response.ok) {
        const error = new Error(`HTTP error! status: ${response.status}`);
        console.error("Response not OK:", error);
        throw error;
      }
      // Refresh the page after successful update
      window.location.reload();
    });
  }
})();
