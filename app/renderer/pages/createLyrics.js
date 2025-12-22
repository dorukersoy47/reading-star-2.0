import { navigateTo } from "../router.js";

export const title = "Create the Lyrics!";

export function Render() {
  const el = document.createElement("div");
  el.className = "create-lyrics-page";
  
  el.innerHTML = `
    <form>
      <div class="prompt-text">
        <textarea id="text-box" class="prompt-box" name="prompt" placeholder="Describe the theme for the lyrics..."></textarea>
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

  el.querySelector("#generate").onclick = () => navigateTo("createLyrics");

  return el;
}