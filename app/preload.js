const { contextBridge, ipcRenderer } = require('electron')

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
  getLyricSet: (instId, setId) => ipcRenderer.invoke('getLyricSet', { instId, setId }),
  createInstrumental: (text, speed, length) => ipcRenderer.invoke('createInstrumental', { text, speed, length }),
  createLyricSet: (instId, text, complexity) => ipcRenderer.invoke('createLyricSet', { instId, text, complexity })
});