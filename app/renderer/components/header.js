import { goBack, navigateTo } from "../router.js";
import { getIcon } from "./loadIcons.js";

const makeBtn = (id, name, onClick) => {
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
    hLeft.appendChild(makeBtn("back", "arrow-left", () => goBack()));
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

  hRight.appendChild(makeBtn("help", "circle-question-mark"));
  hRight.appendChild(makeBtn("settings", "settings"));
  hRight.appendChild(makeBtn("quit", "x", () => window.close()));

  el.appendChild(hLeft);
  el.appendChild(hCenter);
  el.appendChild(hRight);

  return el;
}