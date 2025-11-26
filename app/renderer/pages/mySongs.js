import { navigateTo } from "../router.js";

export function MySongs() {
  const el = document.createElement("div");
  el.className = "my-songs-page";
  
  el.innerHTML = `
    <button id="back">←</button>
    <h1>My Songs</h1>
  `;

  el.querySelector("#back").onclick = () => navigateTo("home");

  return el;
}