import { navigateTo } from "../router.js";

export const title = "My Songs";
export const header = true;
// export const back = "home";

export function Render() {
  const el = document.createElement("div");
  el.className = "my-songs-page";
  
  el.innerHTML = `
    <h1>My Songs</h1>
  `;

  return el;
}