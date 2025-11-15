import { navigateTo } from "./router.js";

window.onload = () => {
  navigateTo("home");
};

const func = async () => {
  const response = await window.versions.ping()
  console.log(response) // prints out 'pong'
}

func()