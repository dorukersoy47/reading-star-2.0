import { Home } from "./pages/home.js";
import { CreateSong } from "./pages/createSong.js";
import { MySongs } from "./pages/mySongs.js";

const routes = {
  home: Home,
  createSong: CreateSong,
  mySongs: MySongs
};

export function navigateTo(page) {
  const app = document.getElementById("app");
  app.innerHTML = "";
  app.appendChild(routes[page]());
}