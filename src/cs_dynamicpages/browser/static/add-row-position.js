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
      // Get position and container from the button that triggered the offcanvas
      const button = event.relatedTarget;
      const position = button ? button.getAttribute("data-position") : lastClickedPosition;
      const container = button ? button.getAttribute("data-container") : null;
      
      if (position !== null || container !== null) {
        const links = offcanvasAddRow.querySelectorAll('a[href*="add-row-content"]');
        
        links.forEach(link => {
          let href = link.getAttribute('href');
          
          // Remove existing position and container if any to avoid duplication
          href = href.replace(/[&?]position=\d+/, '');
          href = href.replace(/[&?]container=[^&]+/, '');
          
          // Add new position
          if (position !== null) {
            const separator = href.includes('?') ? '&' : '?';
            href = href + separator + 'position=' + position;
          }
          
          // Add new container
          if (container !== null) {
            const separator = href.includes('?') ? '&' : '?';
            href = href + separator + 'container=' + container;
          }
          
          link.setAttribute('href', href);
        });

        // Also update template apply buttons
        const templateButtons = offcanvasAddRow.querySelectorAll('.apply-template');
        templateButtons.forEach(btn => {
          if (position !== null) btn.setAttribute('data-position', position);
          if (container !== null) btn.setAttribute('data-container', container);
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
