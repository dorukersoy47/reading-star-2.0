const { app, BrowserWindow, ipcMain } = require('electron/main')
const path = require('node:path')
const fs = require('fs/promises')

// TEMPORARY TESTING LOCATION
const SONGS_DIR = path.join(__dirname, 'songs') // path.join(app.getPath('userData'), 'songs')

async function ensureSongsFolder() {
    await fs.mkdir(SONGS_DIR, { recursive: true });
}

async function loadAllSongs() {
    const songFolders = await fs.readdir(SONGS_DIR);
    const songs = [];

    for (const folderName of songFolders) {
        const songPath = path.join(SONGS_DIR, folderName);
        const stats = await fs.stat(songPath);
        if (!stats.isDirectory()) continue;

        const instrumentalPath = path.join(songPath, 'instrumental.json');

        try {
            const instrumentalData = JSON.parse(await fs.readFile(instrumentalPath, 'utf-8'));
            songs.push({ id: folderName, path: songPath, instrumental: instrumentalData });
        } catch (err) {
            console.error("Error reading song:", err);
        }
    }
    return songs;
}

async function loadLyricsForSong(songPath) {
    const lyricsPath = path.join(songPath, 'lyrics');
    let files;

    try {
        files = await fs.readdir(lyricsPath);
    } catch {
        return [];
    }

    const sets = [];
    for (const file of files) {
        if (!file.endsWith('.json')) continue;
        const json = JSON.parse(await fs.readFile(path.join(lyricsPath, file), 'utf-8'));
        sets.push({ id: file.replace('.json', ''), data: json });
    }
    return sets;
}

ipcMain.handle('loadAllSongs', loadAllSongs);
ipcMain.handle('loadLyricsForSong', (_, songPath) => loadLyricsForSong(songPath));

const createWindow = () => {
  const win = new BrowserWindow({
    fullscreen: true,
    resizable: false,
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })
  win.loadFile('renderer/index.html')
  // win.webContents.openDevTools()
}

app.whenReady().then(async () => {
  ipcMain.handle('ping', () => 'pong')
  await ensureSongsFolder()
  createWindow()
})