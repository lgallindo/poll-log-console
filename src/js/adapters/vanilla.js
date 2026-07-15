import { createStore } from '../core/store.js';
import { createPoller } from '../core/poller.js';
import { handleCommand } from '../core/commands.js';
import { playNotifSound } from '../core/sound.js';

const FRAGMENT = `
<div class="dos-console is-minimized" data-dos-root>
  <div class="dos-header" data-dos-header>
    <div class="dos-header-left">
      <div class="notif-light" data-dos-notif></div>
      <span data-dos-title-full style="display:none"></span>
      <span data-dos-title-mini>C:\\</span>
    </div>
    <div class="dos-header-actions" data-dos-actions style="display:none">
      <button type="button" data-dos-copy title="Copy Logs">📋</button>
      <button type="button" data-dos-clear title="Clear Logs">🗑️</button>
      <span>[-]</span>
    </div>
  </div>
  <div class="dos-body" data-dos-body hidden>
    <div data-dos-lines></div>
    <div class="dos-prompt">
      <span class="dos-prompt-gt">&gt;</span>
      <input type="text" data-dos-input autocomplete="off">
      <div class="dos-cursor"></div>
    </div>
  </div>
</div>`;

function typeClass(type) {
  return `dos-msg-${type || 'sys'}`;
}

export function mount(target, opts = {}) {
  const el = typeof target === 'string' ? document.querySelector(target) : target;
  if (!el) throw new Error('DosAuditConsole.mount: target not found');

  const store = createStore(opts);
  const root = el.querySelector('[data-dos-root]') || (() => {
    el.innerHTML = FRAGMENT;
    return el.querySelector('[data-dos-root]');
  })();

  const notif = root.querySelector('[data-dos-notif]');
  const titleFull = root.querySelector('[data-dos-title-full]');
  const titleMini = root.querySelector('[data-dos-title-mini]');
  const actions = root.querySelector('[data-dos-actions]');
  const body = root.querySelector('[data-dos-body]');
  const lines = root.querySelector('[data-dos-lines]');
  const input = root.querySelector('[data-dos-input]');

  titleFull.textContent = store.options.title;

  function render() {
    const minimized = store.state.minimized;
    root.classList.toggle('is-minimized', minimized);
    body.hidden = minimized;
    actions.style.display = minimized ? 'none' : 'flex';
    titleFull.style.display = minimized ? 'none' : 'inline';
    titleMini.style.display = minimized ? 'inline' : 'none';
    notif.className = 'notif-light' + (store.state.notifClass ? ` ${store.state.notifClass}` : '');

    const wasAtBottom = body.scrollHeight - body.scrollTop - body.clientHeight < 50;
    lines.innerHTML = store.state.logs.map((log) => (
      `<div class="dos-line"><span class="dos-line-time">${escapeHtml(log.time || '')}</span>` +
      `<span class="${typeClass(log.type)}">${escapeHtml(log.msg || '')}</span></div>`
    )).join('');
    if (!minimized && wasAtBottom) body.scrollTop = body.scrollHeight;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  const poller = createPoller(store, { onChange: render });

  function notify(message, type = 'sys') {
    store.toast(message, type);
    if (store.options.sound) playNotifSound();
    render();
  }

  root.querySelector('[data-dos-header]').addEventListener('click', (e) => {
    e.stopPropagation();
    store.state.minimized = !store.state.minimized;
    render();
  });
  root.addEventListener('click', () => {
    if (store.state.minimized) {
      store.state.minimized = false;
      render();
    }
  });
  root.querySelector('[data-dos-copy]').addEventListener('click', (e) => {
    e.stopPropagation();
    handleCommand(store, notify, ':w');
    render();
  });
  root.querySelector('[data-dos-clear]').addEventListener('click', (e) => {
    e.stopPropagation();
    handleCommand(store, notify, 'cls');
    render();
  });
  input.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    handleCommand(store, notify, store.state.input = input.value);
    input.value = '';
    store.state.input = '';
    render();
  });

  window.addEventListener('dos:toast', (ev) => {
    const d = ev.detail || {};
    if (d && d._fromSelf) return;
  });

  poller.start();
  render();

  return {
    store,
    poller,
    toast: notify,
    render,
    destroy: () => poller.stop(),
  };
}
