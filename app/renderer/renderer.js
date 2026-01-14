import { navigateTo } from "./router.js";
import { loadIcons } from "./components/loadIcons.js";

window.onload = async () => {
  await loadIcons();
  navigateTo({page:"home"});
};

const test = async () => {
  const response = await window.versions.ping();
  console.log(response); // prints out 'pong'
}

test();