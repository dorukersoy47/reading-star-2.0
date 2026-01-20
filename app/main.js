const { app, BrowserWindow, ipcMain } = require('electron/main')
const path = require('node:path')
const { dialog } = require('electron')

const API_BASE_URL = 'http://127.0.0.1:8000/instrumentals';

/* GET */
// get all instrumentals and their lyric sets
ipcMain.handle('getAll', async () => {
    const response = await fetch(`${API_BASE_URL}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
});

// get an instrumental from its ID
ipcMain.handle('getInstrumental', async (_, instId) => {
    const response = await fetch(`${API_BASE_URL}/${instId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
});

// get all lyric sets of an instrumental
ipcMain.handle('getLyricSets', async (_, instId) => {
    const response = await fetch(`${API_BASE_URL}/${instId}/lyrics`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
});

// get a lyric set from its and its instrumental's ID
ipcMain.handle('getLyricSet', async (_, { instId, setId }) => {
    const response = await fetch(`${API_BASE_URL}/${instId}/lyrics/${setId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
});


/* POST */
// create a new instrumental
ipcMain.handle('createInstrumental', async (_, { genre }) => {
    const response = await fetch(`${API_BASE_URL}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ genre })
    });
    return await response.json();
})

// create a new lyrics set
ipcMain.handle('createLyricSet', async (_, { instId, topic, stanza_count, syllable_count }) => {
    const response = await fetch(`${API_BASE_URL}/${instId}/lyrics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, stanza_count, syllable_count })
    });
    return await response.json();
})


/* DELETE */
// delete an instrumental
ipcMain.handle('deleteInstrumental', async (_, instId) => {
    const response = await fetch(`${API_BASE_URL}/${instId}`, { method: 'DELETE' });
    if (!response.ok) { throw new Error(`Failed to delete instrumental: ${response.status}`); }
    return true;
});

// delete a lyric set
ipcMain.handle('deleteLyricSet', async (_, { instId, setId }) => {
    const response = await fetch(`${API_BASE_URL}/${instId}/lyrics/${setId}`, { method: 'DELETE' });
    if (!response.ok) { throw new Error(`Failed to delete lyric set: ${response.status}`); }
    return true;
});


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
  createWindow()
})