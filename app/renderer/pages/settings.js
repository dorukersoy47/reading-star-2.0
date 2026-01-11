export const title = "Settings";

export function Render() {
  const el = document.createElement("div");
  el.className = "settings-page";
  
  el.innerHTML = `
    <form>
      <div class="setting">
        <label for="difficulty">Difficulty:</label>
        <select id="difficulty">
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <div class="setting">
        <label for="volume">Volume:</label>
        <input type="range" id="volume" min="0" max="100">
      </div>
      <div class="setting">
        <label for="enableScoring">Enable Scoring:</label>
        <input type="checkbox" id="enableScoring">
      </div>
      <button type="button" class="button" id="saveSettings">Save</button>
    </form>
  `;

  return el;
}