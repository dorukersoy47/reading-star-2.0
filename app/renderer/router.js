import { Header } from "./components/header.js";
import * as HomePage from "./pages/home.js";
import * as CreateSongPage from "./pages/createSong.js";
import * as MySongsPage from "./pages/mySongs.js";
import * as SongPage from "./pages/song.js";

const routes = {
  home: HomePage,
  createSong: CreateSongPage,
  mySongs: MySongsPage,
  song: SongPage
};

const historyStack = [];
let currentScreen = null;
let currentData = null;

export function navigateTo(page, data = null, pushHistory = true) {
  const header = document.getElementById("header");
  header.innerHTML = "";

  if (pushHistory && currentScreen) {
    historyStack.push({ page: currentScreen, data: currentData });
  }

  header.appendChild(Header(historyStack.length > 0, routes[page].title));

  const app = document.getElementById("app");
  app.innerHTML = "";
  app.appendChild(routes[page].Render(data));

  currentScreen = page;
  currentData = data;
}

export function goBack() {
  if (historyStack.length > 0) {
    const previous = historyStack.pop();
    navigateTo(previous.page, previous.data, false);
  }
}