// Live contrast scan for the Unraid webGUI.
//
// Paste into the browser console on any webGUI page (Dashboard, Main,
// Plugins, ...) with the theme installed. It walks every visible text node,
// finds the real background behind it (the first ancestor with an opaque
// background colour) and lists anything under 4.5:1. Colours in oklch() are
// skipped (Unraid's own header components use them).
//
// An empty list means the page passes. Known stock exceptions: Unraid's
// orange "Update Available" badge and the brief "checking..." on Plugins.
(() => {
  const parse = s => {
    if (/oklch/.test(s)) return null;
    const m = s.match(/[\d.]+/g);
    return m ? m.map(Number) : null;
  };
  const lum = c => {
    const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
  };
  const bgOf = e => {
    while (e) {
      const c = parse(getComputedStyle(e).backgroundColor);
      if (c && (c.length < 4 || c[3] > 0.5)) return c;
      e = e.parentElement;
    }
    return [0, 0, 0];
  };
  const out = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walk.nextNode())) {
    const text = n.nodeValue.trim();
    if (!text) continue;
    const el = n.parentElement;
    const cs = getComputedStyle(el);
    if (cs.visibility !== 'visible' || cs.display === 'none' || +cs.opacity < 0.3) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const fg = parse(cs.color);
    if (!fg) continue;
    const a = lum(fg), b = lum(bgOf(el));
    const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    if (ratio < 4.5) out.push(`${ratio.toFixed(2)}  "${text.slice(0, 40)}"  ${cs.color}`);
  }
  const unique = [...new Set(out)];
  console.log(unique.length ? unique.join('\n') : 'No text under 4.5:1 on this page.');
  return unique;
})();
