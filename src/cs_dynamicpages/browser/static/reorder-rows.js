/**
 * Handles reordering of dynamic page rows
 */
(function () {
  "use strict";

  // Store references to avoid re-querying the DOM
  let sortableInstance = null;
  const upClickHandlers = new Map();
  const downClickHandlers = new Map();
  let isInitialized = false;

  // Initialize when DOM is loaded
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRowReordering);
  } else {
    initRowReordering();
  }

  function initRowReordering() {
    if (
      !document.body.classList.contains("template-dynamic-view") ||
      !document.body.classList.contains("can_edit")
    ) {
      return;
    }

    // Initialize drag-and-drop reordering
    initDragAndDropReordering();

    // Find all move up/down buttons
    const moveUpButtons = document.querySelectorAll('a[data-action="move-up"]');
    const moveDownButtons = document.querySelectorAll(
      'a[data-action="move-down"]'
    );

    moveUpButtons.forEach((button) => {
      button.addEventListener("click", (e) => handleButtonClick(e, -1));
    });

    moveDownButtons.forEach((button) => {
      button.addEventListener("click", (e) => handleButtonClick(e, 1));
    });
  }

  function handleButtonClick(e, delta) {
    e.preventDefault();
    e.stopPropagation();

    const button = e.currentTarget;
    if (button.disabled) return;
    button.disabled = true;

    const element = button.closest('[data-move-target="true"]');
    if (element) {
      moveElementInDOM(element, delta);
      sendReorderRequest(element, delta);
    }

    setTimeout(() => (button.disabled = false), 500);
  }

  function initDragAndDropReordering() {
    if (typeof Sortable === "undefined") {
      console.log("SortableJS not loaded. Drag-and-drop reordering disabled.");
      return;
    }

    // Find the container of the rows. We assume all draggable items share the same parent.
    const firstDraggableElement = document.querySelector(
      '[data-move-target="true"]'
    );
    if (!firstDraggableElement?.parentElement) {
      return;
    }
    const container = firstDraggableElement.parentElement;

    // Add a class for styling the handle
    container.classList.add("sortable-container");

    // Initialize SortableJS
    new Sortable(container, {
      animation: 150, // ms, animation speed moving items when sorting, `0` — without animation
      handle: ".drag-handle", // Restrict drag start to elements with this class
      ghostClass: "sortable-ghost", // Class for the drop placeholder
      chosenClass: "sortable-chosen", // Class for the chosen item
      dragClass: "sortable-drag", // Class for the dragging item

      // Element is dropped
      onEnd: (evt) => {
        const { oldIndex, newIndex, item } = evt;
        if (oldIndex !== newIndex) {
          const delta = newIndex - oldIndex;
          sendReorderRequest(item, delta);
        }
      },
    });
  }

  function moveElementInDOM(element, delta) {
    const parent = element.parentNode;
    if (!parent) return;

    if (delta > 0) {
      // Move down
      const nextTarget = element.nextElementSibling?.nextElementSibling || null;
      parent.insertBefore(element, nextTarget);
    } else {
      // Move up
      const target = element.previousElementSibling;
      if (target) {
        parent.insertBefore(element, target);
      }
    }
  }

  function sendReorderRequest(element, delta) {
    const elementId = element.dataset.elementid;
    if (!elementId) {
      console.error("No data-element-id attribute found on element");
      return;
    }

    const baseUrl = element.dataset.parenturl || "";

    const requestBody = {
      ordering: {
        obj_id: elementId,
        delta: delta,
      },
    };

    fetch(baseUrl, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(requestBody),
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) {
          const error = new Error(`HTTP error! status: ${response.status}`);
          throw error;
        }
      })
      .catch((error) => {
        console.error("Error reordering element:", error);
        alert("Error reordering element. Please refresh the page.");
      });
  }
})();
