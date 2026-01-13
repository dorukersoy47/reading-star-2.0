import { Header } from "./components/header.js";
import * as HomePage from "./pages/home.js";
import * as CreateInstrumentalPage from "./pages/createInstrumental.js";
import * as CreateLyricsPage from "./pages/createLyrics.js";
import * as MySongsPage from "./pages/mySongs.js";
import * as LyricSetPage from "./pages/lyricSet.js";
import * as InstrumentalPage from "./pages/instrumental.js";
import * as SettingsPage from "./pages/settings.js";

const routes = {
  home: HomePage,
  createInstrumental: CreateInstrumentalPage,
  createLyrics: CreateLyricsPage,
  mySongs: MySongsPage,
  lyricSet: LyricSetPage,
  instrumental: InstrumentalPage,
  settings: SettingsPage
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