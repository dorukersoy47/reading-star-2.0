export function showLoadingScreen() {
  const loadingScreen = document.createElement("div");
  loadingScreen.id = "loading-screen";
  loadingScreen.innerHTML = `
    <div class="loading-overlay">
      <div class="spinner"></div>
      <p>Generating...</p>
    </div>
  `;
  document.body.appendChild(loadingScreen);
}

export function hideLoadingScreen() {
  const loadingScreen = document.getElementById("loading-screen");
  if (loadingScreen) {
    document.body.removeChild(loadingScreen);
  }
}