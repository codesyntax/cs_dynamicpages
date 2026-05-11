/**
 * Handles setting the position when adding a new row
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", () => {
    const offcanvasAddRow = document.getElementById("addrow-offcanvasRight");
    if (!offcanvasAddRow) return;

    offcanvasAddRow.addEventListener("show.bs.offcanvas", (event) => {
      const button = event.relatedTarget;
      if (!button) {
        console.warn("Offcanvas opened without a relatedTarget (trigger button)");
        return;
      }
      
      const position = button.getAttribute("data-position");
      console.log("Setting add-row position to:", position);
      
      if (position !== null) {
        // Update all "add-row-content" links in the offcanvas
        const links = offcanvasAddRow.querySelectorAll('a[href*="add-row-content"]');
        links.forEach(link => {
          let href = link.getAttribute('href');
          
          // Remove existing position if any
          href = href.replace(/[&?]position=\d+/, '');
          
          // Add new position
          const separator = href.includes('?') ? '&' : '?';
          link.setAttribute('href', href + separator + 'position=' + position);
          
          console.debug("Updated link:", link.href);
        });

        // Also update template apply buttons
        const templateButtons = offcanvasAddRow.querySelectorAll('.apply-template');
        templateButtons.forEach(btn => {
          btn.setAttribute('data-position', position);
        });
      }
    });
  });
})();
