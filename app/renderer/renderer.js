import { navigateTo } from "./router.js";
import { loadIcons } from "./components/loadIcons.js";

window.onload = async () => {
  await loadIcons();

  const songs = await window.songAPI.loadAllSongs();
  console.log("Loaded songs:", songs);

  navigateTo("home");
};

const test = async () => {
  const response = await window.versions.ping();
  console.log(response); // prints out 'pong'
}

test();