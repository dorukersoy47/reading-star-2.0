import { navigateTo } from "../router.js";
import { showLoadingScreen, hideLoadingScreen } from "../components/loading.js";

export const title = "Create the Lyrics!";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "create-lyrics-page";
  
  el.innerHTML = `
    <div class="creation-form">
      <input id="prompt" class="prompt-box" type="text" placeholder="Describe a short topic for your lyrics...">
      <input id="keywords" class="prompt-box" type="text" placeholder="Keywords to include (comma-separated)...">
      <div class="creation-settings">
        <div class="creation-setting">
          <label for="song-length">Song Length</label>
          <select id="song-length">
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
        <div class="creation-setting">
          <label for="line-length">Line Length</label>
          <select id="line-length">
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
        <div class="creation-setting">
          <label for="complexity">Complexity</label>
          <select id="complexity">
            <option value="simple">Simple</option>
            <option value="moderate">Moderate</option>
            <option value="complex">Complex</option>
          </select>
        </div>
      </div>
      <button type="button" class="button" id="generate">Generate</button>
    </div>
  `;

  el.querySelector("#generate").onclick = async () => {
    const topic = document.getElementById("prompt").value;
    const keywords = document.getElementById("keywords").value;
    const song_length = document.getElementById("song-length").value;
    const line_length = document.getElementById("line-length").value;
    const complexity = document.getElementById("complexity").value;

    try {
      showLoadingScreen();
      const result = await window.backendAPI.createLyricSet(data.instId, topic, keywords, song_length, line_length, complexity);
      navigateTo({ page: "lyricSet", pushHistory: false, data: { instId: data.instId, setId: result.id }, title: result.title });
    } catch (error) {
      console.error("Error generating lyrics:", error);
      alert("Failed to generate the lyrics. Please try again.");
    } finally {
      hideLoadingScreen();
    }
  }

  return el;
}