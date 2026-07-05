// Runs automatically on every Netlify deploy (see netlify.toml).
// The admin panel stores each catalog item as its own flat file at the
// repo root, named like "some-release.item.json" (this is what makes the
// admin's search box work — Decap CMS can only search "folder"
// collections, not one single big file — while still needing zero
// subfolders, since the ".item.json" suffix is what keeps these files
// distinct from everything else in the root).
// The site itself still just fetches one items.json, so this script
// glues all the individual *.item.json files back together into that
// one file every time you publish a change.
const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const outFile = path.join(rootDir, 'items.json');

const files = fs
  .readdirSync(rootDir)
  .filter((f) => f.endsWith('.item.json'));

const items = files
  .map((f) => {
    const raw = fs.readFileSync(path.join(rootDir, f), 'utf8');
    try {
      return JSON.parse(raw);
    } catch (err) {
      console.error(`Skipping ${f} — not valid JSON (${err.message})`);
      return null;
    }
  })
  .filter(Boolean);

fs.writeFileSync(outFile, JSON.stringify({ items }, null, 2));
console.log(`Built items.json from ${items.length} *.item.json file(s) at the repo root`);
