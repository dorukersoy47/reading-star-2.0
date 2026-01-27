import { goBack, navigateTo } from "../router.js";
import { formatDate } from "../components/utility.js"
import { getIcon } from "../components/loadIcons.js";
import { confirm } from "../components/confirm.js";

export let title = "Lyric Set Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "lyric-page-not";
  
  el.innerHTML = `
    <div class="instrumental-subtitle display-date" id="instrumental"></div>
    <div class="lyric-page">
      <div class="lyric-page-left">
        <div id="lyrics" class="white-box"></div>
      </div>
      <div class="lyric-page-right">
        <div class="lyric-meta">
          <div class="display-date" id="created"></div>
          <div class="display-date" id="played"></div>
        </div>
        <button class="header-button header-button-x delete-button" id="delete"></button>
      </div>
      <div class="bottom-button-container">
        <button type="button" class="button bottom-button" id="play">Play</button>
      </div>
    </div>
  `;

  window.backendAPI.getLyricSet(data.instId, data.setId).then((setData) => {
    formatLyrics(document.getElementById("lyrics"), setData.lyrics);
    document.getElementById("created").textContent = `Created: ${formatDate(setData.created_at)}`
    document.getElementById("played").textContent = `Last Played: ${formatDate(setData.last_played)}`

    const deleteBtn = document.getElementById("delete");
    deleteBtn.innerHTML = getIcon("delete");
    deleteBtn.onclick = async () => {
      const confirmed = await confirm(`Are you sure you want to delete the "${setData.title}" lyric set?`, 'This cannot be undone.');

      if (!confirmed) return;

      await window.backendAPI.deleteLyricSet(data.instId, data.setId);
      goBack();
    };
  });

  window.backendAPI.getInstrumental(data.instId).then((instData) => {
    document.getElementById("instrumental").textContent = `${instData.title}`
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