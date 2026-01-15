import { navigateTo } from "../router.js";
import { getIcon } from "../components/loadIcons.js";
import { formatDate } from "../components/utility.js";

export let title = "Instrumental Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "lyric-page";
  
  window.backendAPI.getInstrumental(data.instId).then((instrumentalData) => {
    el.innerHTML = `
      <div instrumental-page-left>
        <div class="lyric-btn-title" style="text-align: center; color:var(--title);">Lyric Sets</div>
        <div class="track" id="lyric-sets"></div>
      </div>
      <div class="lyric-page-right">
        <audio id="player" controls></audio>
        <div id="audio-btn-container" class="semi-transparent-bg">
          <button id="play-btn" class="header-button audio-button"></button>
          <button id="restart-btn" class="header-button audio-button"></button>
        </div>
        <br>
        <div class="lyric-meta">
          <div class="display-date" id="created"></div>
          <div class="display-date" id="played"></div>
        </div>
      </div>
    `;

    document.getElementById("created").textContent = `Created: ${formatDate(instrumentalData.created_at)}`
    document.getElementById("played").textContent = `Last Played: ${formatDate(instrumentalData.last_played)}`

    const audio = document.getElementById("player");
    
    audio.src = window.backendAPI.convertAudioURL(instrumentalData.audio_url);
    audio.controls = false;

    const playBtn = document.getElementById("play-btn");
    playBtn.innerHTML = getIcon("play");
    playBtn.onclick = () => {
      if (audio.paused) {
        audio.play();
        playBtn.innerHTML = getIcon("pause");
      } else {
        audio.pause();
        playBtn.innerHTML = getIcon("play");
      }
    };

    const restartBtn = document.getElementById("restart-btn");
    restartBtn.innerHTML = getIcon("restart");
    restartBtn.onclick = () => {
      audio.currentTime = 0;
      // audio.play();
      // playBtn.innerHTML = getIcon("pause");
    };

    const setContainer = document.getElementById("lyric-sets");
    window.backendAPI.getLyricSets(instrumentalData.id).then((lyricSets) => {
      if (lyricSets.length == 0){
        setContainer.innerHTML = `<p class="lyric-btn-title" style="font-size: 1.2rem">No lyric sets yet.</p>`;
      }
        
      for (const set of lyricSets) {
        const setbtn = document.createElement("button");
        setbtn.className = "button lyric-button instrumental-page-lyric-button";
        setbtn.innerHTML = `
          <div class="lyric-btn-left">
            <div class="lyric-btn-title">${set.title}</div>
          </div>
        `
        setbtn.onclick = () => navigateTo({page:"lyricSet", data:{ instId: instrumentalData.id, setId: set.id }, title:set.title});
        setContainer.appendChild(setbtn);
      }

      const createLyricsButton = document.createElement("button");
      createLyricsButton.type = "button";
      createLyricsButton.className = "button";
      createLyricsButton.id = "ontoLyrics";
      createLyricsButton.textContent = "Create New Lyrics!";
      createLyricsButton.onclick = async () => {
        navigateTo({ page: "createLyrics", data: { instId: instrumentalData.id } });
      };

      setContainer.appendChild(createLyricsButton);
    })
  });

  return el;
}