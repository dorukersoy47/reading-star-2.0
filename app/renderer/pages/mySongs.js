import { navigateTo } from "../router.js";

export const title = "My Songs";

export function Render() {
  const el = document.createElement("div");
  el.className = "my-songs-page";
  
  el.innerHTML = `
    <div id="songList"></div>
  `;

  loadSongs(el);

  return el;
}

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const day = String(date.getDate());
  const month = String(date.getMonth() + 1);
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
};

async function loadSongs(rootElement) {
  const container = rootElement.querySelector("#songList");
  container.innerHTML = "<p>Loading songs...</p>";

  const result = await window.backendAPI.getAll();

  if (!result || result.length === 0) {
    container.innerHTML = "<p>No songs yet.</p>";
    return;
  }

  container.innerHTML = "";

  for (const instrumental of result) {
    const el = document.createElement("div");
    el.className = "track";

    const instBtn = document.createElement("button");
    instBtn.className = "instrumental-button button";
    instBtn.innerHTML = `
      <div class="inst-btn-left">
        <div class="inst-btn-title">${instrumental.title}</div>
        <div class="inst-btn-subtitle">Instrumental</div>
      </div>
      <div class="inst-btn-dates">
        <div class="inst-btn-date">Created: ${formatDate(instrumental.created_at)}</div>
        <div class="inst-btn-date">Last Played: ${formatDate(instrumental.last_played)}</div>
      </div>
    `;
    instBtn.onclick = () => navigateTo({page:"instrumental", data:{ instId: instrumental.id }, title:instrumental.title});
    el.appendChild(instBtn);

    for (const set of instrumental.lyricSets) {
      const setbtn = document.createElement("button");
      setbtn.className = "button lyric-button";
      setbtn.innerHTML = `
        <div class="lyric-btn-left">
          <div class="lyric-btn-title">${set.title}</div>
          <div class="lyric-btn-subtitle">Lyric Set</div>
        </div>
      `
      setbtn.onclick = () => navigateTo({page:"lyricSet", data:{ instId: instrumental.id, setId: set.id }, title:set.title});
      el.appendChild(setbtn);
    }

    container.appendChild(el);
  }
}