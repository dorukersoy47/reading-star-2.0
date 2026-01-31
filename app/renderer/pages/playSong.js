import { navigateTo } from "../router.js";

export let title = "Lyric Set Page";

export function Render(data) {
  const el = document.createElement("div");
  el.className = "lyric-page-not";
  
  el.innerHTML = `
    <div class="instrumental-subtitle display-date" id="instrumental"></div>
    <audio id="player"></audio>
    <div class="song-lyrics">
      <p id="previous" class="secondary-line" ></p>
      <p id="current" class="primary-line""></p>
      <p id="next" class="secondary-line"></p>
    </div>
  `;

  window.backendAPI.getInstrumental(data.instId).then((instData) => {
    document.getElementById("instrumental").textContent = `${instData.title}`
    const audio = document.getElementById("player");
    audio.src = window.backendAPI.convertAudioURL(instData.audio_url);
    audio.controls = false;

    window.backendAPI.getLyricSet(data.instId, data.setId).then((setData) => {
      window.backendAPI.getLyricRhythm(data.instId, data.setId).then((rhythmData) => {
        Countdown(0).then(() => {
          audio.play();
          Play(setData.lyrics, rhythmData);
        });
      });
    });
  });

  return el;
}

function Countdown(seconds) {
  return new Promise((resolve) => {
    let count = seconds;
    const countdownInterval = setInterval(() => {
      // DISPLAY SOMEWHERE
      console.log(`Starting in ${count}...`);
      count--;
      
      if (count <= 0) {
        clearInterval(countdownInterval);
        resolve();
      }
    }, 1000);
  });
}

function Play(lyrics, rhythmData) {
  let currentLineIndex = 0;
  let currentWordIndex = 0;
  let currentSyllableIndex = 0;
  
  function updateDisplay() {
    const previousElement = document.getElementById("previous");
    const currentElement = document.getElementById("current");
    const nextElement = document.getElementById("next");
    
    // previous line
    if (currentLineIndex > 0) {
      previousElement.innerHTML = formatLine(lyrics[currentLineIndex - 1]);
    } else {
      previousElement.innerHTML = "";
    }
    
    // current line with highlighting
    currentElement.innerHTML = formatLine(
      lyrics[currentLineIndex], currentWordIndex, currentSyllableIndex
    );
    
    // next line
    if (currentLineIndex < lyrics.length - 1) {
      nextElement.innerHTML = formatLine(lyrics[currentLineIndex + 1]);
    } else {
      nextElement.innerHTML = "";
    }
  }
  
  function formatLine(line, highlightWordIndex = -1, highlightSyllableIndex = -1) {
    if (!line) return "";
    
    return line.map((word, wordIndex) => {
      return word.map((syllable, syllableIndex) => {
        const isCurrent = wordIndex === highlightWordIndex && syllableIndex === highlightSyllableIndex;
        
        return isCurrent ? `<strong>${syllable}</strong>` : syllable;
      }).join('');
    }).join(' ');
  }
  
  function advance() {
    currentSyllableIndex++;
    
    // check if we need to move to next word
    if (currentLineIndex < lyrics.length && 
        currentWordIndex < lyrics[currentLineIndex].length &&
        currentSyllableIndex >= lyrics[currentLineIndex][currentWordIndex].length) {
      currentSyllableIndex = 0;
      currentWordIndex++;
      
      // check if we need to move to next line
      if (currentWordIndex >= lyrics[currentLineIndex].length) {
        currentWordIndex = 0;
        currentLineIndex++;
      }
    }
    
    // check if song is finished
    if (currentLineIndex >= lyrics.length) {
      return false; // song finished
    }
    
    updateDisplay();
    return true; // song not finished
  }
  
  function startSinging() {
    updateDisplay(); // Initial display
    
    function scheduleNextSyllable() {
      const timings = rhythmData.on_beat_timings;
      if (currentLineIndex < timings.length) {
        // calculate the total syllable index within the current line
        let totalSyllableIndex = 0;
        for (let wordIdx = 0; wordIdx < currentWordIndex; wordIdx++) {
          if (wordIdx < lyrics[currentLineIndex].length) {
            totalSyllableIndex += lyrics[currentLineIndex][wordIdx].length;
          }
        }
        totalSyllableIndex += currentSyllableIndex;
        
        if (totalSyllableIndex < timings[currentLineIndex].length) {
          const delay = timings[currentLineIndex][totalSyllableIndex];
          
          setTimeout(() => {
            if (advance()) {
              scheduleNextSyllable();
            }
          }, delay);
        }
      }
    }
    
    scheduleNextSyllable();
  }
  
  startSinging();
}