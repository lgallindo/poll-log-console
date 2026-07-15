import { playNotifSound } from './sound.js';

/**
 * @param {ReturnType<import('./store.js').createStore>} store
 * @param {{ onChange?: () => void }} [hooks]
 */
export function createPoller(store, hooks = {}) {
  const { options, state, mergeIncoming, toast } = store;
  let timer = null;

  async function fetchLogs() {
    try {
      const res = await fetch(options.logsUrl);
      if (!res.ok) return;
      const incoming = await res.json();
      const added = mergeIncoming(incoming);
      if (added && hooks.onChange) hooks.onChange();
    } catch (_) {
      /* soft-fail */
    }
  }

  async function boot() {
    if (!options.infoUrl) return;
    try {
      const res = await fetch(options.infoUrl);
      if (!res.ok) return;
      const info = await res.json();
      const bootMsgs = (options.bootLines || [
        '--- AGENTE FILOLOGICO BIOS v0.1 ---',
        `SERVER_TIME: ${info.server_time} (${info.timezone})`,
        `OS_DETECTED: ${info.os} | PORT: ${info.port}`,
        `API_KEY_STATE: ${info.api_key_status}`,
        'READY.',
        '------------------------------------',
      ]).map((msg) => ({ time: '', msg, type: 'res' }));
      if (state.logs.length === 0) {
        state.logs = bootMsgs;
        store.persist();
        if (hooks.onChange) hooks.onChange();
      }
    } catch (_) { /* soft-fail */ }
  }

  function start() {
    store.load();
    boot().then(() => fetchLogs());
    timer = setInterval(fetchLogs, options.pollMs);
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
  }

  function notify(message, type = 'sys') {
    toast(message, type);
    if (options.sound) playNotifSound();
    if (hooks.onChange) hooks.onChange();
  }

  return { fetchLogs, boot, start, stop, notify };
}
