/**
 * Handles the edit mode toggle functionality for dynamic pages.
 * Toggles between edit and preview modes and saves the preference in localStorage.
 */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    // Only run if both required classes are present on the body
    if (
      !document.body.classList.contains("template-dynamic-view") ||
      !document.body.classList.contains("can_edit")
    ) {
      return;
    }

    // Add preview-mode class by default on page load
    // document.body.classList.add("preview-mode");

    const toggle = document.getElementById("editModeToggle");
    if (toggle) {
      toggle.addEventListener("change", function () {
        if (this.checked) {
          document.body.classList.remove("preview-mode");
        } else {
          document.body.classList.add("preview-mode");
        }
      });
    }

    const adminBarToggle = document.getElementById("adminBarToggle");
    const adminBar = document.querySelector(".rows-mangement");
    const adminBarContainer = document.querySelector(".admin-bar-container");

    if (adminBarToggle && adminBar && adminBarContainer) {
      adminBarToggle.addEventListener("click", function () {
        const isExpanded = adminBarContainer.classList.contains("expanded");
        adminBar.classList.toggle("d-none");
        adminBarContainer.classList.toggle("expanded");

        if (!isExpanded) {
          // Change to Close icon (X)
          adminBarToggle.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
              <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
            </svg>`;
        } else {
          // Change back to Chevron Up
          adminBarToggle.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z"/>
            </svg>`;
        }
      });
    }
  });
})();
