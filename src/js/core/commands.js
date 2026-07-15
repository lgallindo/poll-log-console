/** Command handlers for the console prompt. */
export function handleCommand(store, notify, cmd) {
  const c = String(cmd || '').trim();
  if (c === ':w') {
    const text = store.state.logs.map((l) => `[${l.time}] ${l.msg}`).join('\n');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text);
    }
    notify('CONSOLE_COPIED');
    return true;
  }
  if (c === ':q') {
    store.state.minimized = true;
    return true;
  }
  if (c === 'cls') {
    store.clear();
    notify('CONSOLE_PURGED');
    return true;
  }
  return false;
}
