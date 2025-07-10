/**
 * Handles deletion of dynamic page rows
 */

(function () {
  "use strict";

  // Initialize when DOM is loaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRowDeletion);
  } else {
    initRowDeletion();
  }

  function initRowDeletion() {
    // Only run on dynamic-view with edit permissions
    if (
      !document.body.classList.contains("template-dynamic-view") ||
      !document.body.classList.contains("userrole-manager")
    ) {
      console.log(
        "Not in dynamic-view edit mode, skipping row deletion initialization"
      );
      return;
    }

    console.log("Initializing row deletion...");

    const deleteModal = document.getElementById("deleteRowModal");
    if (!deleteModal) {
      console.error("Delete row modal not found");
      return;
    }

    let rowToDelete = null;

    deleteModal.addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;
      rowToDelete = button.closest("section.dynamic-row");
      console.log("Preparing to delete row:", rowToDelete?.dataset.rowid);
    });

    const confirmButton = document.getElementById("confirmDeleteRow");
    if (confirmButton) {
      confirmButton.addEventListener("click", handleDeleteRow);
    } else {
      console.error("Confirm delete button not found");
    }

    function handleDeleteRow() {
      if (!rowToDelete) {
        console.error("No row selected for deletion");
        return;
      }

      const rowId = rowToDelete.dataset.rowid;
      const rowUrl = rowToDelete.dataset.rowurl;

      console.log(`Deleting row ${rowId} via ${rowUrl}`);

      fetch(rowUrl, {
        method: "DELETE",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRF-TOKEN":
            document.querySelector('input[name="_authenticator"]')?.value || "",
        },
        credentials: "same-origin",
      })
        .then((response) => {
          console.log(`Received response with status: ${response.status}`);
          console.log("Response headers:", response.headers);
          console.log("Response ok:", response.ok);
          if (!response.ok) {
            const error = new Error(`HTTP error! status: ${response.status}`);
            console.error("Response not OK:", error);
            throw error;
          }
        })
        .finally(() => {
          const modal = bootstrap.Modal.getInstance(deleteModal);
          if (modal) {
            modal.hide();
          }
          // Refresh the page after successful update
          window.location.reload();
        });
    }
  }
})();
