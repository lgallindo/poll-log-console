/**
 * Core store — framework-agnostic log state.
 * @typedef {{ time: string, msg: string, type: string }} LogEntry
 * @typedef {{
 *   logsUrl?: string,
 *   infoUrl?: string,
 *   pollMs?: number,
 *   storageKey?: string,
 *   maxLocalLogs?: number,
 *   sound?: boolean,
 *   title?: string,
 *   bootLines?: string[]|null,
 *   actions?: string[]
 * }} DosOptions
 */

export function defaultOptions(opts = {}) {
  return {
    logsUrl: '/api/v1/logs',
    infoUrl: '/api/v1/info',
    pollMs: 3000,
    storageKey: 'dos_logs',
    maxLocalLogs: 500,
    sound: true,
    title: 'C:\\SYSTEM\\AUDIT_LOG.EXE',
    bootLines: null,
    actions: ['copy', 'clear'],
    ...opts,
  };
}

export function createStore(opts = {}) {
  const options = defaultOptions(opts);
  /** @type {{ minimized: boolean, input: string, logs: LogEntry[], notifClass: string }} */
  const state = {
    minimized: true,
    input: '',
    logs: [],
    notifClass: '',
  };

  function persist() {
    try {
      const trimmed = state.logs.slice(-options.maxLocalLogs);
      state.logs = trimmed;
      localStorage.setItem(options.storageKey, JSON.stringify(trimmed));
    } catch (_) { /* ignore quota */ }
  }

  function load() {
    try {
      const raw = localStorage.getItem(options.storageKey);
      if (raw) state.logs = JSON.parse(raw);
    } catch (_) { /* ignore */ }
  }

  function mergeIncoming(incoming) {
    if (!Array.isArray(incoming)) return 0;
    let added = 0;
    for (const n of incoming) {
      const exists = state.logs.some((l) => l.time === n.time && l.msg === n.msg);
      if (!exists) {
        state.logs.push(n);
        added += 1;
      }
    }
    if (added) persist();
    return added;
  }

  function clear() {
    state.logs = [];
    try { localStorage.removeItem(options.storageKey); } catch (_) { /* ignore */ }
  }

  function toast(message, type = 'sys') {
    const now = new Date().toLocaleTimeString();
    state.logs.push({
      time: now,
      msg: `[${String(type).toUpperCase()}] ${message}`,
      type,
    });
    persist();
    state.notifClass = type === 'err' ? 'error' : 'active';
    setTimeout(() => { state.notifClass = ''; }, 2000);
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('dos:toast', { detail: { message, type } }));
    }
    return state;
  }

  return { options, state, persist, load, mergeIncoming, clear, toast };
}
