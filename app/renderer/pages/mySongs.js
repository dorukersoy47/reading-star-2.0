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

async function loadSongs(rootElement) {
  const container = rootElement.querySelector("#songList");
  container.innerHTML = "<p>Loading songs...</p>";

  const songs = await window.songAPI.loadAllSongs();

  if (!songs || songs.length === 0) {
    container.innerHTML = "<p>No songs yet.</p>";
    return;
  }

  container.innerHTML = "";

  for (const song of songs) {
    const el = document.createElement("div");
    el.className = "track";

    if (song.instrumental) {
      const instBtn = document.createElement("button");
      instBtn.className = "instrumental-button button";
      instBtn.textContent = song.instrumental.title;
      instBtn.onclick = () => navigateTo("instrumental", { instData: song.instrumental, songPath: song.path });
      el.appendChild(instBtn);
    }

    if (song.path) {
      const sets = await window.songAPI.loadLyricsForSong(song.path);
      if (sets && sets.length) {
        for (const set of sets) {
          const setbtn = document.createElement("button");
          setbtn.className = "button lyric-button";
          setbtn.textContent = set.data.title;
          setbtn.onclick = () => navigateTo("song", { setData: set.data, songPath: song.path });
          el.appendChild(setbtn);
        }
      }
    }

    container.appendChild(el);
  }
}