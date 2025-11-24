const container = document.getElementById("background");

const colors = [
    "#f5c6f8ff",
    "#c0e6ffff",
    "#cdf9edff",
    "#cfc3fdff"
];

const NUM_BLOBS = 6;

function createBlob() {
  const blob = document.createElement("div");
  blob.classList.add("blob");

  const size = 200 + Math.random() * 200;

  blob.style.setProperty("--size", size + "px");
  blob.style.setProperty("--color", colors[Math.floor(Math.random() * colors.length)]);

  container.appendChild(blob);

  return blob;
}

function randomPosition() {
  // extra overflow so blobs drift outside edges nicely
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
//  make the blobs move in the beginning
  const blobs = [];

  for (let i = 0; i < NUM_BLOBS; i++) {
    const blob = createBlob();
    blobs.push(blob);
    moveBlob(blob); // initial position
  }

  // move blobs every 8 seconds
  setInterval(() => {
    blobs.forEach(moveBlob);
  }, 8000);
}

init();
