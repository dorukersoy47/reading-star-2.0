import { navigateTo } from "../router.js";

export const header = false;
export const title = "Home";

export function Render() {
  const el = document.createElement("div");
  el.className = "home-page";
  
  el.innerHTML = `
    <h1 class="home-title">ReadingStar 2.0</h1>
    <div class="home-buttons">
      <button id="mysongs" class="button">My Songs</button>
      <button id="create" class="button">Create a New Song!</button>
    </div>
  `;

  el.querySelector("#create").onclick = () => navigateTo("createSong");
  el.querySelector("#mysongs").onclick = () => navigateTo("mySongs");

  return el;
}