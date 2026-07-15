import { createStore } from '../core/store.js';
import { createPoller } from '../core/poller.js';
import { handleCommand } from '../core/commands.js';
import { playNotifSound } from '../core/sound.js';

/**
 * Alpine.data factory: Alpine.data('dosAuditConsole', alpineComponent)
 */
export function alpineComponent(opts = {}) {
  const store = createStore(opts);
  let poller;

  return {
    title: store.options.title,
    get console() { return store.state; },
    init() {
      poller = createPoller(store, {
        onChange: () => { /* Alpine reactivity via mutating store.state */ },
      });
      // Re-bind console to Alpine-reactive object
      this.console = store.state;
      poller.start();
      window.addEventListener('dos:toast', (ev) => {
        const d = ev.detail || {};
        if (d.message != null) this.showToast(d.message, d.type || 'sys');
      });
    },
    showToast(message, type = 'sys') {
      store.toast(message, type);
      if (store.options.sound) playNotifSound();
    },
    copyConsole() { handleCommand(store, (m, t) => this.showToast(m, t), ':w'); },
    clearConsole() { handleCommand(store, (m, t) => this.showToast(m, t), 'cls'); },
    onCommand() {
      handleCommand(store, (m, t) => this.showToast(m, t), this.console.input);
      this.console.input = '';
    },
    destroy() { if (poller) poller.stop(); },
  };
}

export function registerAlpine(Alpine, name = 'dosAuditConsole') {
  Alpine.data(name, alpineComponent);
}
