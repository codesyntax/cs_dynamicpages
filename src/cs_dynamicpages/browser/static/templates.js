async function applyTemplate(uid) {
  // The data we want to send
  const data = {
    uid: uid,
  };

  try {
    // Make the request using fetch()
    let base_url = document.getElementsByTagName("body")[0].dataset["baseUrl"];
    const response = await fetch(`${base_url}/@apply-template`, {
      method: "POST", // Request method
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json", // Type of data we are sending
      },
      body: JSON.stringify(data), // Convert data to JSON string
    });

    // Handle the server's response
    if (response.ok) {
      sessionStorage.setItem("toast-message", "Template applied succesfuly.");
      location.reload();
    } else {
      console.error("Server error:", response.status);
      alert("An error occurred while sending data.");
    }
  } catch (error) {
    // Handle network errors
    console.error("Network error:", error);
  }
}

async function deleteTemplate(uid) {
  // The data we want to send
  const data = {
    uid: uid,
  };

  try {
    // Make the request using fetch()
    let base_url = document.getElementsByTagName("body")[0].dataset["baseUrl"];
    const response = await fetch(`${base_url}/@templates`, {
      method: "DELETE", // Request method
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json", // Type of data we are sending
      },
      body: JSON.stringify(data), // Convert data to JSON string
    });

    // Handle the server's response
    if (response.ok) {
      sessionStorage.setItem("toast-message", "Template deleted succesfuly.");
      location.reload();
    } else {
      console.error("Server error:", response.status);
      alert("An error occurred while sending data.");
    }
  } catch (error) {
    // Handle network errors
    console.error("Network error:", error);
  }
}

async function sendData(uid, name) {
  // The data we want to send
  const data = {
    uid: uid,
    name: name,
  };

  try {
    // Make the request using fetch()
    let base_url = document.getElementsByTagName("body")[0].dataset["baseUrl"];
    const response = await fetch(`${base_url}/@templates`, {
      method: "POST", // Request method
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json", // Type of data we are sending
      },
      body: JSON.stringify(data), // Convert data to JSON string
    });

    // Handle the server's response
    if (response.ok) {
      sessionStorage.setItem("toast-message", "Template saved succesfuly.");
      location.reload();
    } else {
      console.error("Server error:", response.status);
      alert("An error occurred while sending data.");
    }
  } catch (error) {
    // Handle network errors
    console.error("Network error:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("addAsTemplate");
  if (addBtn) {
    addBtn.addEventListener("click", () => {
      let target_uid = addBtn.dataset["uid"];
      let template_name = document.getElementById("template-name").value;
      sendData(target_uid, template_name);
    });
  }

  Array.from(document.getElementsByClassName("apply-template")).forEach(
    (element) => {
      element.addEventListener("click", (event) => {
        let target_uid = event.target.dataset["uid"];
        applyTemplate(target_uid);
      });
    },
  );

  Array.from(document.getElementsByClassName("confirmDeleteElement")).forEach(
    (element) => {
      element.addEventListener("click", (event) => {
        let target_uid = event.target.dataset["uid"];
        deleteTemplate(target_uid);
      });
    },
  );

  // Template preview logic
  const previewModalEl = document.getElementById('previewTemplateModal');
  let previewModal;
  if (previewModalEl) {
    previewModal = new bootstrap.Modal(previewModalEl);
  }

  Array.from(document.getElementsByClassName("preview-template-btn")).forEach(
    (element) => {
      element.addEventListener("click", async (event) => {
        event.preventDefault(); // Prevent standard navigation
        
        const url = element.getAttribute("href");
        const templateName = element.getAttribute("data-template-name");
        const modalBody = document.getElementById("previewTemplateBody");
        const modalTitle = document.getElementById("previewTemplateModalLabel");
        
        if (modalTitle && templateName) {
          modalTitle.textContent = "Template: " + templateName;
        }
        
        // Show loading state
        modalBody.innerHTML = '<div class="p-5 text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        if (previewModal) previewModal.show();

        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error("Network response was not ok");
          
          const htmlString = await response.text();
          
          // Parse the HTML string into a DOM
          const parser = new DOMParser();
          const doc = parser.parseFromString(htmlString, "text/html");
          
          // Extract the specific content
          const dynamicContent = doc.querySelector("main#dynamic_pages_content");
          
          if (dynamicContent) {
            // Remove unwanted editing/interactive elements for a clean preview
            const elementsToRemove = dynamicContent.querySelectorAll(
              '.edit-options, .rows-mangement, .offcanvas, .modal, script, .toast-container'
            );
            elementsToRemove.forEach(el => el.remove());

            // Put the extracted and cleaned HTML into the modal body
            modalBody.innerHTML = dynamicContent.innerHTML;
          } else {
            modalBody.innerHTML = '<div class="p-4 text-danger">Content not found in template.</div>';
          }
        } catch (error) {
          console.error("Error fetching template:", error);
          modalBody.innerHTML = '<div class="p-4 text-danger">Failed to load template preview.</div>';
        }
      });
    }
  );
});
