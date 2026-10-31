// Replace server details on a webGUI page before taking a screenshot.
//
// Edit REPLACE with your own names first (left: a regular expression that
// matches the whole text, right: the stand-in), then paste into the browser
// console. It keeps re-applying itself while the dashboard refreshes, until
// you reload the page. Nothing is sent anywhere and nothing on the server
// changes: it only edits the page in your browser.
(() => {
  const REPLACE = [
    [/^my-server-name$/i, 'Tower'],             // server name (header and tile)
    [/^My server description$/, 'Home server'], // description
    [/^Board Vendor .*$/, 'Motherboard vendor, model'],
    [/^BIOS Vendor .*$/, 'BIOS vendor, version'],
    [/^BIOS dated:.*$/, 'BIOS dated: 2024'],
    [/^my-compose-stack$/, 'my-stack'],
    [/^.*\d{4}, [A-Z]{3,4}$/, ''],              // date and time-zone line under the clock
    [/\b\d{1,3}(\.\d{1,3}){3}\b/, '10.0.0.10'], // any IPv4 address
  ];
  const HIDE_SMALL_IMAGES = true;               // container and app icons

  const scrub = () => {
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walk.nextNode())) {
      const t = n.nodeValue.trim();
      for (const [re, s] of REPLACE) {
        if (re.test(t)) { n.nodeValue = t.replace(re, s); break; }
      }
    }
    if (HIDE_SMALL_IMAGES) {
      document.querySelectorAll('img').forEach(i => {
        const r = i.getBoundingClientRect();
        if (r.width && r.width < 60 && !i.closest('#header') && !i.closest('.nav-tile')) i.style.visibility = 'hidden';
      });
    }
    document.title = 'Tower';
  };
  scrub();
  const obs = new MutationObserver(() => {
    obs.disconnect();
    scrub();
    obs.observe(document.body, { subtree: true, childList: true, characterData: true });
  });
  obs.observe(document.body, { subtree: true, childList: true, characterData: true });
  console.log('Scrubbed. Read the page before you screenshot it: anything not in REPLACE is still there.');
})();
