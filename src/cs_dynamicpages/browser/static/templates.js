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

try {
  document.getElementById("addAsTemplate").addEventListener("click", () => {
    let target_uid = document.getElementById("addAsTemplate").dataset["uid"];
    let template_name = document.getElementById("template-name").value;
    sendData(target_uid, template_name);
  });
} catch {
  console.log("No add button");
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
