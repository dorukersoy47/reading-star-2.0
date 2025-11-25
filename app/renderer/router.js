import { Header } from "./components/header.js";
import * as HomePage from "./pages/home.js";
import * as CreateSongPage from "./pages/createSong.js";
import * as MySongsPage from "./pages/mySongs.js";

const routes = {
  home: HomePage,
  createSong: CreateSongPage,
  mySongs: MySongsPage
};

const historyStack = [];
let currentScreen = null;

export function navigateTo(page, pushHistory = true) {
  const header = document.getElementById("header");
  header.innerHTML = "";

  if (pushHistory && currentScreen) {
    historyStack.push(currentScreen);
  }

  header.appendChild(Header(historyStack.length > 0, routes[page].title));

  const app = document.getElementById("app");
  app.innerHTML = "";
  app.appendChild(routes[page].Render());

  currentScreen = page;
}

export function goBack() {
  if (historyStack.length > 0) {
    const previous = historyStack.pop();
    navigateTo(previous, false);
  }
}