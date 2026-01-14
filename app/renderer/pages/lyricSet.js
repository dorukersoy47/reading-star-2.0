import { navigateTo } from "../router.js";
import { formatDate } from "../components/utility.js"

export let title = "Lyric Set Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "lyric-page";
  
  el.innerHTML = `
    <div class="lyric-page-left">
      <div id="lyrics"></div>
    </div>
    <div class="lyric-page-right">
      <div class="lyric-meta">
        <div class="display-date">Created at: ${}</div>
      </div>
    </div>
  `;

  window.backendAPI.getLyricSet(data.instId, data.setId).then((setData) => {
    formatLyrics(el, setData.lyrics);
  });

  return el;
}

function formatLyrics(container, lyrics) {
  container.innerHTML = "";

  for (const line of lyrics) {
    const p = document.createElement("p");
    p.className = "lyric-line";
    const lineText = line.map(syllable => syllable.join("")).join(" ");
    p.textContent = lineFormat(escapeHtml(lineText));
    container.appendChild(p);
  }
}

function lineFormat(str) {
  return String(str).replace(/~/g, "");
}

// utility function to escape HTML
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
}