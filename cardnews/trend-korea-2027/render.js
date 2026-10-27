const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [dir, file, outdir] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(dir, file));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(600);
  const cards = await p.$$('section.card');
  for (let i = 0; i < cards.length; i++) {
    const r = await cards[i].evaluate(e => { const f = e.querySelector('.foot'); const prev = f.previousElementSibling; return Math.round(f.getBoundingClientRect().top - prev.getBoundingClientRect().bottom); });
    if (r < 24) console.log(file, 'card', i + 1, 'gap', r);
    await cards[i].screenshot({ path: path.join(dir, outdir, `${outdir}_${String(i + 1).padStart(2, '0')}.png`) });
  }
  await b.close();
})();
