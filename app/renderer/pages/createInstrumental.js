import { navigateTo } from "../router.js";
import { showLoadingScreen, hideLoadingScreen } from "../components/loading.js";

export const title = "Create the Instrumental!";

export function Render() {
  const el = document.createElement("div");
  el.className = "create-instrumental-page";
  
  el.innerHTML = `
    <div class="creation-form">
      <div class="prompt-text">
        <textarea id="prompt" class="prompt-box" name="prompt" placeholder="Give keywords to describe the mood..."></textarea>
      </div>
      <div class="creation-settings">
        <div class="creation-setting inst-creation-setting">
          <label for="genre">Genre</label>
          <select id="genre" class="genre">
            <option value="nursery_rhyme">Nursery Rhyme</option>
            <option value="hip_hop">Hip Hop</option>
            <option value="rock">Rock</option>
            <option value="jazz">Jazz</option>
            <option value="classical">Classical</option>
            <option value="reggae">Reggae</option>
            <option value="rnb">R&B</option>
            <option value="punk">Punk</option>
            <option value="metal">Metal</option>
            <option value="bollywood">Bollywood</option>
          </select>
        </div>
      </div>
      <button type="button" class="button" id="generate">Generate</button>
    </div>
  `;

  el.querySelector("#generate").onclick = async () => {
    const genre = document.getElementById('genre').value;
    const keywords = document.getElementById('prompt').value;
    try {
      showLoadingScreen();

      const result = await window.backendAPI.createInstrumental(genre, keywords);

      navigateTo({ page: "instrumental", pushHistory: false, data: { instId: result.id }, title: result.title });
    } catch (error) {
      console.error("Error generating instrumental:", error);
      alert("Failed to generate the instrumental. Please try again.");
    } finally {
      hideLoadingScreen();
    }
  }

  return el;
}