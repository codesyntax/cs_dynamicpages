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
      const containerType = button ? button.getAttribute("data-container-type") : 'top_level';
      
      // Filter available views based on constraints
      const constraintsElem = document.getElementById("row-constraints-json");
      if (constraintsElem && containerType) {
        try {
          const constraints = JSON.parse(constraintsElem.textContent);
          const allowedTypes = constraints[containerType] || [];
          const viewItems = offcanvasAddRow.querySelectorAll(".available-view-item");
          
          viewItems.forEach(item => {
            const rowType = item.getAttribute("data-row-type");
            if (allowedTypes.length === 0 || allowedTypes.includes(rowType)) {
              item.classList.remove("d-none");
            } else {
              item.classList.add("d-none");
            }
          });
        } catch (e) {
          console.error("Error parsing constraints:", e);
        }
      }

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
