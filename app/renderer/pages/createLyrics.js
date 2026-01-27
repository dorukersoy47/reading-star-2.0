import { navigateTo } from "../router.js";
import { showLoadingScreen, hideLoadingScreen } from "../components/loading.js";
import { lengthToStanzaCount, complexityToSyllableCount } from "../components/utility.js";

export const title = "Create the Lyrics!";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "create-lyrics-page";
  
  el.innerHTML = `
    <form>
      <div class="prompt-text">
        <textarea id="prompt" class="prompt-box" name="prompt" placeholder="Describe the topic for your lyrics..."></textarea>
      </div>
      <div class="creation-settings">
        <div class="creation-setting">
          <label for="length">Length</label>
          <select id="length">
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
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
    const topic = document.getElementById("prompt").value;
    const length = document.getElementById("length").value;
    const complexity = document.getElementById("complexity").value;

    const stanza_count = lengthToStanzaCount(length);
    const syllable_count = complexityToSyllableCount(complexity)

    try {
      showLoadingScreen();
      const result = await window.backendAPI.createLyricSet(data.instId, topic, stanza_count, syllable_count);
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