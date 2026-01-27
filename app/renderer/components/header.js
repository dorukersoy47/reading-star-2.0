import { goBack, navigateTo } from "../router.js";
import { getIcon } from "./loadIcons.js";

export function makeIconBtn(id, name, onClick) {
  const b = document.createElement("button");
  b.id = id;
  b.className = "header-button";
  b.setAttribute("aria-label", id);
  if (onClick) b.onclick = onClick;
  b.innerHTML = getIcon(name);
  return b;
}

export function Header(canGoBack, title) {
  const el = document.createElement("div");
  el.className = "header";

  const hLeft = document.createElement("div");
  hLeft.className = "header-left";
  if (canGoBack) {
    hLeft.appendChild(makeIconBtn("back", "arrow-left", () => goBack()));
  }

  const hCenter = document.createElement("div");
  hCenter.className = "header-center";
  if (title !== null) {
    const p = document.createElement("p");
    p.id = "title";
    p.textContent = title;
    hCenter.appendChild(p);
  }

  const hRight = document.createElement("div");
  hRight.className = "header-right";

  hRight.appendChild(makeIconBtn("help", "circle-question-mark"));
  hRight.appendChild(makeIconBtn("settings", "settings", () => navigateTo({page:"settings"})));
  let xButton = makeIconBtn("quit", "x", () => window.close());
  xButton.className = "header-button header-button-x";
  hRight.appendChild(xButton);

  el.appendChild(hLeft);
  el.appendChild(hCenter);
  el.appendChild(hRight);

  return el;
}