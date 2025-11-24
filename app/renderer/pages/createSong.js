import { navigateTo } from "../router.js";

export const title = "Create a New Song!";
export const header = true;
export const back = "home";

export function Render() {
  const el = document.createElement("div");
  el.className = "create-song-page";
  
  el.innerHTML = `
    <h1>Create a New Song!</h1>
  `;

  return el;
}