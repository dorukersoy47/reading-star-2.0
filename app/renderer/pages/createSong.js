import { navigateTo } from "../router.js";

export function CreateSong() {
  const el = document.createElement("div");
  el.className = "create-song-page";
  
  el.innerHTML = `
    <button id="back">←</button>
    <h1>Create a New Song!</h1>
  `;

  el.querySelector("#back").onclick = () => navigateTo("home");

  return el;
}