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
      console.log("cs_dynamicpages: Plus button clicked, position:", lastClickedPosition);
    }
  });

  const initAddRowPosition = () => {
    const offcanvasAddRow = document.getElementById("addrow-offcanvasRight");
    if (!offcanvasAddRow) return;

    console.log("cs_dynamicpages: Initializing add-row position handler");

    offcanvasAddRow.addEventListener("show.bs.offcanvas", (event) => {
      // event.relatedTarget sometimes fails in some Bootstrap versions or environments
      const button = event.relatedTarget || null;
      const position = (button ? button.getAttribute("data-position") : null) || lastClickedPosition;
      
      console.log("cs_dynamicpages: Offcanvas showing, target position:", position);
      
      if (position !== null) {
        const links = offcanvasAddRow.querySelectorAll('a[href*="add-row-content"]');
        console.log(`cs_dynamicpages: Found ${links.length} links to update`);
        
        links.forEach(link => {
          let href = link.getAttribute('href');
          
          // Remove existing position if any to avoid duplication
          href = href.replace(/[&?]position=\d+/, '');
          
          // Add new position
          const separator = href.includes('?') ? '&' : '?';
          const newHref = href + separator + 'position=' + position;
          
          link.setAttribute('href', newHref);
          console.debug("cs_dynamicpages: Updated link:", newHref);
        });

        // Also update template apply buttons
        const templateButtons = offcanvasAddRow.querySelectorAll('.apply-template');
        templateButtons.forEach(btn => {
          btn.setAttribute('data-position', position);
        });
      } else {
        console.warn("cs_dynamicpages: Position not found when opening offcanvas");
      }
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAddRowPosition);
  } else {
    initAddRowPosition();
  }
})();
