// Deterministic reel renderer: window.renderAt(t) sets every element's state for time t (seconds).
(function () {
  const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
  const scenes = [...document.querySelectorAll('.scene')];
  window.REEL_DURATION = Math.max(...scenes.map(s => +s.dataset.end));
  window.renderAt = function (t) {
    // slow drifting background
    document.documentElement.style.setProperty('--drift', (t * 6).toFixed(2) + 'px');
    for (const s of scenes) {
      const a = +s.dataset.start, b = +s.dataset.end;
      const last = s.hasAttribute('data-hold');
      let o = 0;
      if (t >= a && t < b) o = 1;
      if (t >= b - 0.3 && t < b && !last) o = Math.max(0, (b - t) / 0.3);
      if (last && t >= a) o = 1;
      s.style.opacity = o;
      s.style.visibility = o > 0 ? 'visible' : 'hidden';
      for (const el of s.querySelectorAll('[data-in]')) {
        const p = ease((t - a - +el.dataset.in) / 0.45);
        const kind = el.dataset.fx || 'up';
        el.style.opacity = p;
        if (kind === 'up') el.style.transform = `translateY(${(1 - p) * 60}px)`;
        if (kind === 'pop') el.style.transform = `scale(${0.85 + 0.15 * p})`;
        if (kind === 'left') el.style.transform = `translateX(${(1 - p) * -80}px)`;
        if (kind === 'right') el.style.transform = `translateX(${(1 - p) * 80}px)`;
      }
      for (const el of s.querySelectorAll('[data-strike]')) {
        const p = ease((t - a - +el.dataset.strike) / 0.4);
        el.style.setProperty('--strike', (p * 100) + '%');
      }
      for (const el of s.querySelectorAll('[data-count]')) {
        const p = ease((t - a - +el.dataset.countAt) / 1.2);
        el.textContent = Math.round(p * +el.dataset.count);
      }
    }
  };
  window.renderAt(0);
})();
