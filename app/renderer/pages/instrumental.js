import { navigateTo } from "../router.js";

export let title = "Instrumental Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "song-page";
  
  window.backendAPI.getInstrumental(data.instId).then((instrumentalData) => {
    el.innerHTML = `
      <p>${instrumentalData.title}</p>
      <p>${instrumentalData.music}</p>
      <button type="button" class="button" id="ontoLyrics">Create Some Lyrics!</button>
    `;

    el.querySelector("#ontoLyrics").onclick = async () => {
      navigateTo("createLyrics", { instId : instrumentalData.id });
    }
  });

  return el;
}