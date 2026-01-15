const { contextBridge, ipcRenderer } = require('electron')

const API_BASE = 'http://127.0.0.1:8000';

function convertAudioURL(audio_url) {
    return `${API_BASE}${audio_url}`;
}

contextBridge.exposeInMainWorld('versions', {
  node: () => process.versions.node,
  chrome: () => process.versions.chrome,
  electron: () => process.versions.electron,
  ping: () => ipcRenderer.invoke('ping')
});

// expose the backend API to the renderer process securely
// the methods defined invoke an IPC event handled by main.js
// methods are called by writing `window.backendAPI.method(parameters)`
contextBridge.exposeInMainWorld('backendAPI', {
  getAll: () => ipcRenderer.invoke('getAll'),
  getInstrumental: (instId) => ipcRenderer.invoke('getInstrumental', instId),
  getLyricSets: (instId) => ipcRenderer.invoke('getLyricSets', { instId }),
  getLyricSet: (instId, setId) => ipcRenderer.invoke('getLyricSet', { instId, setId }),
  createInstrumental: (genre) => ipcRenderer.invoke('createInstrumental', { genre }),
  createLyricSet: (instId, topic, stanza_count, syllable_count) => ipcRenderer.invoke('createLyricSet', { instId, topic, stanza_count, syllable_count }),
  convertAudioURL
});