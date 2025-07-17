/**
 * Handles the edit mode toggle functionality for dynamic pages.
 * Toggles between edit and preview modes and saves the preference in localStorage.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Only run if both required classes are present on the body
  if (
    !document.body.classList.contains("template-dynamic-view") ||
    !document.body.classList.contains("userrole-manager")
  ) {
    return;
  }

  const toggle = document.getElementById("editModeToggle");
  if (toggle) {
    // Initialize from localStorage if available
    const savedMode = localStorage.getItem("editMode");
    if (savedMode === "preview") {
      toggle.checked = false;
      document.body.classList.add("preview-mode");
    }

    toggle.addEventListener("change", function () {
      if (this.checked) {
        document.body.classList.remove("preview-mode");
        localStorage.setItem("editMode", "edit");
      } else {
        document.body.classList.add("preview-mode");
        localStorage.setItem("editMode", "preview");
      }
    });
  }
});
