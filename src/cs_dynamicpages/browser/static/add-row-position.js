/**
 * Handles setting the position when adding a new row
 */
(function () {
  "use strict";

  let lastClickedPosition = null;

  // Track which button was clicked last
  document.addEventListener("click", (event) => {
    const button = event.target.closest(".add-row-plus-btn");
    if (button) {
      lastClickedPosition = button.getAttribute("data-position");
    }
  });

  const initAddRowPosition = () => {
    const offcanvasAddRow = document.getElementById("addrow-offcanvasRight");
    if (!offcanvasAddRow) return;

    offcanvasAddRow.addEventListener("show.bs.offcanvas", (event) => {
      // event.relatedTarget sometimes fails in some Bootstrap versions or environments
      const button = event.relatedTarget || null;
      const position = (button ? button.getAttribute("data-position") : null) || lastClickedPosition;
      
      if (position !== null) {
        const links = offcanvasAddRow.querySelectorAll('a[href*="add-row-content"]');
        
        links.forEach(link => {
          let href = link.getAttribute('href');
          
          // Remove existing position if any to avoid duplication
          href = href.replace(/[&?]position=\d+/, '');
          
          // Add new position
          const separator = href.includes('?') ? '&' : '?';
          const newHref = href + separator + 'position=' + position;
          
          link.setAttribute('href', newHref);
        });

        // Also update template apply buttons
        const templateButtons = offcanvasAddRow.querySelectorAll('.apply-template');
        templateButtons.forEach(btn => {
          btn.setAttribute('data-position', position);
        });
      }
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAddRowPosition);
  } else {
    initAddRowPosition();
  }
})();
