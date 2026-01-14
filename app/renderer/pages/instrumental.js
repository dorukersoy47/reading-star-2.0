import { navigateTo } from "../router.js";

export let title = "Instrumental Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "song-page";
  
  window.backendAPI.getInstrumental(data.instId).then((instrumentalData) => {
    el.innerHTML = `
      <p>${instrumentalData.title}</p>
      <audio id="player" controls></audio>
      <button type="button" class="button" id="ontoLyrics">Create Some Lyrics!</button>
    `;

    const audio = document.getElementById("player");
    
    audio.src = window.backendAPI.convertAudioURL(instrumentalData.audio_url);

    el.querySelector("#ontoLyrics").onclick = async () => {
      navigateTo({page:"createLyrics", data:{ instId : instrumentalData.id }});
    }
  });

  return el;
}