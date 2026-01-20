export function confirm(title, message) {
  return new Promise(resolve => {
    const el = document.createElement("div");
    el.className = "blur-overlay";

    el.innerHTML = `
      <div class="confirmation-box" role="dialog" aria-modal="true">
        <h2>${title}</h2>
        <p>${message}</p>
        <div class="confirmation-buttons">
          <button class="button cancel-button" id="cancel">Cancel</button>
          <button class="button danger-button" id="confirm">Delete</button>
        </div>
      </div>
    `;

    document.body.appendChild(el);

    el.querySelector("#cancel").onclick = () => {
      el.remove();
      resolve(false);
    };

    el.querySelector("#confirm").onclick = () => {
      el.remove();
      resolve(true);
    };
  });
}
