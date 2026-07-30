(function () {
  "use strict";

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPurge);
  } else {
    initPurge();
  }

  function initPurge() {
    if (
      !document.body.classList.contains("template-dynamic-view") ||
      !document.body.classList.contains("can_edit")
    ) {
      return;
    }

    const purgeBtn = document.getElementById("purge-content");
    const successMsg = document.getElementById("purge-success-message");

    if (!purgeBtn) {
      return;
    }

    purgeBtn.addEventListener("click", async () => {
      const url = purgeBtn.dataset.url;

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRF-TOKEN":
              document.querySelector('input[name="_authenticator"]')?.value || "",
          },
          credentials: "same-origin",
        });

        if (response.ok) {
          purgeBtn.classList.add("d-none");
          successMsg.classList.remove("d-none");
          setTimeout(() => {
            successMsg.classList.add("d-none");
            purgeBtn.classList.remove("d-none");
          }, 3000);
        }
      } catch (error) {
        console.error("Purge failed:", error);
      }
    });
  }
})();
