import { navigateTo } from "../router.js";

export function Header() {
  const el = document.createElement("div");
  el.className = "header";
  
  el.innerHTML = `
    <div class="header-left">
        <button id="back" class="header-button">←</button>
    </div>
    <div class="header-center">
        <h1 id="title"></h1>
    </div>
    <div class="header-right">
        <button id="help" class="header-button">❓</button>
        <button id="settings" class="header-button">⚙️</button>
        <button id="quit" class="header-button">✖️</button>
    </div>
  `;

//   el.querySelector("#help").onclick = () => navigateTo("help");
//   el.querySelector("#settings").onclick = () => navigateTo("settings");
  el.querySelector("#quit").onclick = () => window.close();

  return el;
}