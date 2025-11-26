export const icons = new Map();

export async function loadIcons() {
  const names = ["arrow-left", "circle-question-mark", "settings", "x"];
  await Promise.all(names.map(async name => {
    const path = `assets/icons/${name}.svg`;
    try {
      let txt = await fetch(path).then(r => r.text());
      txt = txt.replace(/\s(width|height)="[^"]*"/g, "");
      txt = txt.replace(/\sstroke="[^"]*"/g, ' stroke="currentColor"');
      txt = txt.replace("<svg", '<svg class="icon" stroke-width="2.5"');
      icons.set(name, txt);
    } catch (e) {
      console.warn("preloadIcons failed", name, e);
    }
  }));
}

export function getIcon(name) {
  return icons.get(name);
}