import { Header } from "./components/header.js";
import * as HomePage from "./pages/home.js";
import * as CreateSongPage from "./pages/createSong.js";
import * as MySongsPage from "./pages/mySongs.js";

const routes = {
  home: HomePage,
  createSong: CreateSongPage,
  mySongs: MySongsPage
};

export function navigateTo(page, back) {
  const header = document.getElementById("header");
  header.innerHTML = "";
  if (routes[page].header === true) {
    header.appendChild(Header());
    header.querySelector("#title").innerText = routes[page].title;
    header.querySelector("#back").onclick = () => navigateTo(back);
  }
  const app = document.getElementById("app");
  app.innerHTML = "";
  app.appendChild(routes[page].Render());
}