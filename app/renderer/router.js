import { Header } from "./components/header.js";
import * as HomePage from "./pages/home.js";
import * as CreateInstrumentalPage from "./pages/createInstrumental.js";
import * as CreateLyricsPage from "./pages/createLyrics.js";
import * as MySongsPage from "./pages/mySongs.js";
import * as LyricSetPage from "./pages/lyricSet.js";
import * as InstrumentalPage from "./pages/instrumental.js";
import * as SettingsPage from "./pages/settings.js";
import * as PlaySongPage from "./pages/playSong.js";

const routes = {
  home: HomePage,
  createInstrumental: CreateInstrumentalPage,
  createLyrics: CreateLyricsPage,
  mySongs: MySongsPage,
  lyricSet: LyricSetPage,
  instrumental: InstrumentalPage,
  settings: SettingsPage,
  playSong: PlaySongPage
};

const historyStack = [];
let currentScreen = null;
let currentData = null;
let currentTitle = null;

export function navigateTo({page, data = null, pushHistory = true, title = null}) {
  const header = document.getElementById("header");
  header.innerHTML = "";

  if (pushHistory && currentScreen) {
    historyStack.push({ page: currentScreen, data: currentData, title: currentTitle});
  }

  header.appendChild(Header(historyStack.length > 0, title || routes[page].title));

  const app = document.getElementById("app");
  app.innerHTML = "";
  app.appendChild(routes[page].Render(data));

  currentScreen = page;
  currentData = data;
  currentTitle = title;
}

export function goBack() {
  if (historyStack.length > 0) {
    const previous = historyStack.pop();
    navigateTo({page:previous.page, data:previous.data, pushHistory:false, title:previous.title});
  }
}