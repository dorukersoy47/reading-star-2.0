import { navigateTo } from "../router.js";

export const title = "Create the Instrumental!";

export function Render() {
  const el = document.createElement("div");
  el.className = "create-instrumental-page";
  
  el.innerHTML = `
    <form>
      <div class="prompt-text">
        <textarea id="prompt" class="prompt-box" name="prompt" placeholder="Describe the theme for the instrumental..."></textarea>
      </div>
      <div class="creation-settings">
        <div class="creation-setting">
          <label for="speed">Speed</label>
          <select id="speed">
            <option value="slow">Slow</option>
            <option value="medium">Medium</option>
            <option value="fast">Fast</option>
          </select>
        </div>
        <div class="creation-setting">
          <label for="length">Length</label>
          <select id="length">
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
      </div>
      <button type="button" class="button" id="generate">Generate</button>
    </form>
  `;

  el.querySelector("#generate").onclick = async () => {
    const promptText = document.getElementById('prompt').value;
    const speed = "hmm"
    const length = "hmm"
    const result = await window.backendAPI.createInstrumental(promptText, speed, length)
    navigateTo({page:"instrumental", data:{ instId : result.id }, title:result.title});
  }

  return el;
}