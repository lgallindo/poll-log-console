/**
 * HTMX helpers — beep on OOB/ partial log swap.
 * Host still uses hx-get on #hardcopy-body with HTML partials.
 */
import { playNotifSound } from '../core/sound.js';

export function bindHtmxBeep(bodySelector = '#hardcopy-body', options = { sound: true }) {
  document.body.addEventListener('htmx:afterSwap', (e) => {
    if (!e.target || !e.target.matches) return;
    if (e.target.matches(bodySelector) || e.target.id === bodySelector.replace(/^#/, '')) {
      if (options.sound) playNotifSound();
    }
  });
}
