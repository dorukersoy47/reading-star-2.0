import { navigateTo } from "../router.js";

export const title = "Song Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "song-page";
  
  el.innerHTML = `
    <div id="lyrics"></div>
  `;

  formatLyrics(el, data.setData.lyrics);

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