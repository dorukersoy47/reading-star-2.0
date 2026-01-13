import { navigateTo } from "../router.js";

export const title = "Create the Lyrics!";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "create-lyrics-page";
  
  el.innerHTML = `
    <form>
      <div class="prompt-text">
        <textarea id="prompt" class="prompt-box" name="prompt" placeholder="Describe the theme for the lyrics..."></textarea>
      </div>
      <div class="creation-settings">
        <div class="creation-setting">
          <label for="complexity">Complexity</label>
          <select id="complexity">
            <option value="simple">Simple</option>
            <option value="medium">Medium</option>
            <option value="complex">Complex</option>
          </select>
        </div>
      </div>
      <button type="button" class="button" id="generate">Generate</button>
    </form>
  `;

  el.querySelector("#generate").onclick = async () => {
    const promptText = document.getElementById('prompt').value;
    const complexity = "hmm";
    const result = await window.backendAPI.createLyricSet(data.instId, promptText, complexity);
    navigateTo({page:"lyricSet", data:{ instId : data.instId, setId : result.id}, title:result.title});
  }

  return el;
}