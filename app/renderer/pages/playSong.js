import { navigateTo } from "../router.js";

export let title = "Lyric Set Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "lyric-page-not";
  
  el.innerHTML = `
    <div class="instrumental-subtitle display-date" id="instrumental"></div>
    <div class="lyric-page">
    </div>
  `;

  window.backendAPI.getLyricSet(data.instId, data.setId).then((setData) => {
    formatLyrics(document.getElementById("lyrics"), setData.lyrics);
    document.getElementById("created").textContent = `Created: ${formatDate(setData.created_at)}`
    document.getElementById("played").textContent = `Last Played: ${formatDate(setData.last_played)}`
  });

  window.backendAPI.getInstrumental(data.instId).then((instData) => {
    document.getElementById("instrumental").textContent = `${instData.title}`
  });

  return el;
}