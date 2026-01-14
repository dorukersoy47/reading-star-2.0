import { navigateTo } from "../router.js";
import { showLoadingScreen, hideLoadingScreen } from "../components/loading.js";

export const title = "Create the Instrumental!";

export function Render() {
  const el = document.createElement("div");
  el.className = "create-instrumental-page";
  
  el.innerHTML = `
    <form>
      <div class="creation-settings">
        <div class="creation-setting">
          <label for="genre">Genre</label>
          <select id="genre">
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
    </form>
  `;

  el.querySelector("#generate").onclick = async () => {
    const genre = document.getElementById('genre').value;
    try {
      showLoadingScreen();

      const result = await window.backendAPI.createInstrumental(genre);

      navigateTo({ page: "instrumental", data: { instId: result.id }, title: result.title });
    } catch (error) {
      console.error("Error generating instrumental:", error);
      alert("Failed to generate the instrumental. Please try again.");
    } finally {
      hideLoadingScreen();
    }
  }

  return el;
}