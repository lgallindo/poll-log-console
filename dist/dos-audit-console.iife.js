/*! dos-audit-console IIFE v0.1.0 */
(function (global) {
  'use strict';

  function defaultOptions(opts) {
    return Object.assign({
      logsUrl: '/api/v1/logs',
      infoUrl: '/api/v1/info',
      pollMs: 3000,
      storageKey: 'dos_logs',
      maxLocalLogs: 500,
      sound: true,
      title: 'C:\\SYSTEM\\AUDIT_LOG.EXE',
      bootLines: null,
      actions: ['copy', 'clear']
    }, opts || {});
  }

  function playNotifSound() {
    try {
      var Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      var ctx = new Ctx();
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
      osc.start();
      osc.stop(ctx.currentTime + 0.1);
    } catch (e) {}
  }

  function createStore(opts) {
    var options = defaultOptions(opts);
    var state = { minimized: true, input: '', logs: [], notifClass: '' };
    function persist() {
      try {
        state.logs = state.logs.slice(-options.maxLocalLogs);
        localStorage.setItem(options.storageKey, JSON.stringify(state.logs));
      } catch (e) {}
    }
    function load() {
      try {
        var raw = localStorage.getItem(options.storageKey);
        if (raw) state.logs = JSON.parse(raw);
      } catch (e) {}
    }
    function mergeIncoming(incoming) {
      if (!Array.isArray(incoming)) return 0;
      var added = 0;
      incoming.forEach(function (n) {
        var exists = state.logs.some(function (l) { return l.time === n.time && l.msg === n.msg; });
        if (!exists) { state.logs.push(n); added++; }
      });
      if (added) persist();
      return added;
    }
    function clear() {
      state.logs = [];
      try { localStorage.removeItem(options.storageKey); } catch (e) {}
    }
    function toast(message, type) {
      type = type || 'sys';
      state.logs.push({ time: new Date().toLocaleTimeString(), msg: '[' + String(type).toUpperCase() + '] ' + message, type: type });
      persist();
      state.notifClass = type === 'err' ? 'error' : 'active';
      setTimeout(function () { state.notifClass = ''; }, 2000);
      return state;
    }
    return { options: options, state: state, persist: persist, load: load, mergeIncoming: mergeIncoming, clear: clear, toast: toast };
  }

  function handleCommand(store, notify, cmd) {
    var c = String(cmd || '').trim();
    if (c === ':w') {
      var text = store.state.logs.map(function (l) { return '[' + l.time + '] ' + l.msg; }).join('\n');
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text);
      notify('CONSOLE_COPIED');
      return true;
    }
    if (c === ':q') { store.state.minimized = true; return true; }
    if (c === 'cls') { store.clear(); notify('CONSOLE_PURGED'); return true; }
    return false;
  }

  function createPoller(store, hooks) {
    hooks = hooks || {};
    var timer = null;
    function fetchLogs() {
      return fetch(store.options.logsUrl).then(function (res) {
        if (!res.ok) return;
        return res.json().then(function (incoming) {
          var added = store.mergeIncoming(incoming);
          if (added && hooks.onChange) hooks.onChange();
        });
      }).catch(function () {});
    }
    function boot() {
      if (!store.options.infoUrl) return Promise.resolve();
      return fetch(store.options.infoUrl).then(function (res) {
        if (!res.ok) return;
        return res.json().then(function (info) {
          var lines = store.options.bootLines || [
            '--- POLL-LOG-CONSOLE BIOS v0.1 ---',
            'SERVER_TIME: ' + info.server_time + ' (' + info.timezone + ')',
            'OS_DETECTED: ' + info.os + ' | PORT: ' + info.port,
            'API_KEY_STATE: ' + info.api_key_status,
            'READY.',
            '------------------------------------'
          ];
          if (store.state.logs.length === 0) {
            store.state.logs = lines.map(function (msg) { return { time: '', msg: msg, type: 'res' }; });
            store.persist();
            if (hooks.onChange) hooks.onChange();
          }
        });
      }).catch(function () {});
    }
    return {
      start: function () {
        store.load();
        boot().then(fetchLogs);
        timer = setInterval(fetchLogs, store.options.pollMs);
      },
      stop: function () { if (timer) clearInterval(timer); timer = null; },
      fetchLogs: fetchLogs,
      boot: boot
    };
  }

  var FRAGMENT = '<div class="dos-console is-minimized" data-dos-root>' +
    '<div class="dos-header" data-dos-header><div class="dos-header-left">' +
    '<div class="notif-light" data-dos-notif></div>' +
    '<span data-dos-title-full style="display:none"></span><span data-dos-title-mini>C:\\</span></div>' +
    '<div class="dos-header-actions" data-dos-actions style="display:none">' +
    '<button type="button" data-dos-copy title="Copy Logs">📋</button>' +
    '<button type="button" data-dos-clear title="Clear Logs">🗑️</button><span>[-]</span></div></div>' +
    '<div class="dos-body" data-dos-body hidden><div data-dos-lines></div>' +
    '<div class="dos-prompt"><span class="dos-prompt-gt">&gt;</span>' +
    '<input type="text" data-dos-input autocomplete="off"><div class="dos-cursor"></div></div></div></div>';

  function escapeHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function mount(target, opts) {
    var el = typeof target === 'string' ? document.querySelector(target) : target;
    if (!el) throw new Error('DosAuditConsole.mount: target not found');
    var store = createStore(opts);
    var root = el.querySelector('[data-dos-root]');
    if (!root) { el.innerHTML = FRAGMENT; root = el.querySelector('[data-dos-root]'); }
    var notif = root.querySelector('[data-dos-notif]');
    var titleFull = root.querySelector('[data-dos-title-full]');
    var titleMini = root.querySelector('[data-dos-title-mini]');
    var actions = root.querySelector('[data-dos-actions]');
    var body = root.querySelector('[data-dos-body]');
    var lines = root.querySelector('[data-dos-lines]');
    var input = root.querySelector('[data-dos-input]');
    titleFull.textContent = store.options.title;

    function render() {
      var minimized = store.state.minimized;
      root.classList.toggle('is-minimized', minimized);
      body.hidden = minimized;
      actions.style.display = minimized ? 'none' : 'flex';
      titleFull.style.display = minimized ? 'none' : 'inline';
      titleMini.style.display = minimized ? 'inline' : 'none';
      notif.className = 'notif-light' + (store.state.notifClass ? (' ' + store.state.notifClass) : '');
      var wasAtBottom = body.scrollHeight - body.scrollTop - body.clientHeight < 50;
      lines.innerHTML = store.state.logs.map(function (log) {
        return '<div class="dos-line"><span class="dos-line-time">' + escapeHtml(log.time || '') +
          '</span><span class="dos-msg-' + (log.type || 'sys') + '">' + escapeHtml(log.msg || '') + '</span></div>';
      }).join('');
      if (!minimized && wasAtBottom) body.scrollTop = body.scrollHeight;
    }

    function notify(message, type) {
      store.toast(message, type || 'sys');
      if (store.options.sound) playNotifSound();
      render();
    }

    var poller = createPoller(store, { onChange: render });
    root.querySelector('[data-dos-header]').addEventListener('click', function (e) {
      e.stopPropagation();
      store.state.minimized = !store.state.minimized;
      render();
    });
    root.addEventListener('click', function () {
      if (store.state.minimized) { store.state.minimized = false; render(); }
    });
    root.querySelector('[data-dos-copy]').addEventListener('click', function (e) {
      e.stopPropagation(); handleCommand(store, notify, ':w'); render();
    });
    root.querySelector('[data-dos-clear]').addEventListener('click', function (e) {
      e.stopPropagation(); handleCommand(store, notify, 'cls'); render();
    });
    input.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      handleCommand(store, notify, input.value);
      input.value = '';
      render();
    });
    poller.start();
    render();
    return { store: store, poller: poller, toast: notify, render: render, destroy: function () { poller.stop(); } };
  }

  function alpineComponent(opts) {
    var store = createStore(opts);
    var poller;
    return {
      title: store.options.title,
      console: store.state,
      init: function () {
        var self = this;
        poller = createPoller(store, { onChange: function () {} });
        poller.start();
      },
      showToast: function (message, type) {
        store.toast(message, type || 'sys');
        if (store.options.sound) playNotifSound();
      },
      copyConsole: function () { handleCommand(store, this.showToast.bind(this), ':w'); },
      clearConsole: function () { handleCommand(store, this.showToast.bind(this), 'cls'); },
      onCommand: function () {
        handleCommand(store, this.showToast.bind(this), this.console.input);
        this.console.input = '';
      }
    };
  }

  function bindHtmxBeep(bodySelector, options) {
    options = options || { sound: true };
    bodySelector = bodySelector || '#dos-body';
    document.body.addEventListener('htmx:afterSwap', function (e) {
      if (!e.target) return;
      var id = bodySelector.replace(/^#/, '');
      if (e.target.id === id || (e.target.matches && e.target.matches(bodySelector))) {
        if (options.sound) playNotifSound();
      }
    });
  }

  var api = {
    mount: mount,
    createStore: createStore,
    createPoller: createPoller,
    playNotifSound: playNotifSound,
    handleCommand: handleCommand,
    alpineComponent: alpineComponent,
    bindHtmxBeep: bindHtmxBeep,
    registerAlpine: function (Alpine, name) {
      Alpine.data(name || 'dosAuditConsole', alpineComponent);
    },
    sound: { beep: playNotifSound }
  };
  global.DosAuditConsole = api;
})(typeof window !== 'undefined' ? window : globalThis);
