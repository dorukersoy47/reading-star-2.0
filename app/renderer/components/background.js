const container = document.getElementById("background");

const colors = [
    "#cfc3fdff",
    "#c0e6ffff",
    "#f5c6f8ff",
    "#cdf9edff"
];

const NUM_BLOBS = 6;

function createBlob(i) {
  const blob = document.createElement("div");
  blob.classList.add("blob");

  const size = 10 + Math.random() * 10;

  blob.style.setProperty("--size", size + "rem");
  blob.style.setProperty("--color", colors[i % colors.length]);

  container.appendChild(blob);

  return blob;
}

function randomPosition() {
  const extra = 200;

  return {
    x: Math.random() * (window.innerWidth + extra) - extra / 2,
    y: Math.random() * (window.innerHeight + extra) - extra / 2
  };
}

function moveBlob(blob) {
  const { x, y } = randomPosition();
  blob.style.transform = `translate(${x}px, ${y}px)`;
}

function init() {
  const blobs = [];

  for (let i = 0; i < NUM_BLOBS; i++) {
    const blob = createBlob(i);
    blobs.push(blob);
    moveBlob(blob);
  }

  // move blobs every 8 seconds
  setInterval(() => {
    blobs.forEach(moveBlob);
  }, 8000);
}

init();
