import { goBack, navigateTo } from "../router.js";

async function loadIcon(target, path) {
  const el = typeof target === "string" ? document.getElementById(target) : target;
  if (!el) return;
  try {
    let svgText = await fetch(path).then(r => r.text());
    svgText = svgText.replace(/\s(width|height)="[^"]*"/g, "");
    svgText = svgText.replace(/\sstroke="[^"]*"/g, ' stroke="currentColor"');
    svgText = svgText.replace("<svg", '<svg class="icon" stroke-width="2.5"');
    el.innerHTML = svgText;
  } catch (err) {
    console.warn("loadIcon failed", path, err);
  }
}

const makeBtn = (id, iconPath, onClick) => {
  const b = document.createElement("button");
  b.id = id;
  b.className = "header-button";
  b.setAttribute("aria-label", id);
  if (onClick) b.onclick = onClick;
  loadIcon(b, iconPath);
  return b;
}

export function Header(canGoBack, title) {
  const el = document.createElement("div");
  el.className = "header";

  const hLeft = document.createElement("div");
  hLeft.className = "header-left";
  if (canGoBack) {
    hLeft.appendChild(makeBtn("back", "assets/icons/arrow-left.svg", () => goBack()));
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

  hRight.appendChild(makeBtn("help", "assets/icons/circle-question-mark.svg"));
  hRight.appendChild(makeBtn("settings", "assets/icons/settings.svg"));
  hRight.appendChild(makeBtn("quit", "assets/icons/x.svg", () => window.close()));

  el.appendChild(hLeft);
  el.appendChild(hCenter);
  el.appendChild(hRight);

  return el;
}