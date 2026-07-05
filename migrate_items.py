#!/usr/bin/env python3
"""
One-time migration for THE VAULT.

Your admin panel used to store every catalog item inside one big
items.json. To get a real search box in the admin panel (needed once you
have hundreds/thousands of items), each item now needs to be its own
file — but still flat at the repo root, no subfolders. So each item
becomes its own "<slug>.item.json" file sitting right next to
index.html, style.css, etc.

This script reads your CURRENT items.json (download it from your live
GitHub repo first) and writes one <slug>.item.json file per entry, in
whatever directory you run it from.

Usage:
    python3 migrate_items.py path/to/your/items.json

Then upload the generated *.item.json files to your repo root, flat,
alongside everything else, together with the updated config.yml,
netlify.toml, build.js, admin.html. Commit, let Netlify redeploy once,
and you're done — the admin panel will show the new search box, and the
live site keeps working exactly the same.
"""
import json
import os
import re
import sys


def slugify(title, seen):
    slug = re.sub(r"[^a-z0-9]+", "-", (title or "item").lower()).strip("-") or "item"
    base = slug
    i = 2
    while slug in seen:
        slug = f"{base}-{i}"
        i += 1
    seen.add(slug)
    return slug


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 migrate_items.py path/to/items.json")
        sys.exit(1)

    src = sys.argv[1]
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", data if isinstance(data, list) else [])
    if not items:
        print("No items found in that file — nothing to migrate.")
        return

    seen = set()
    for item in items:
        slug = slugify(item.get("title"), seen)
        out_path = f"{slug}.item.json"
        with open(out_path, "w", encoding="utf-8") as out:
            json.dump(item, out, indent=2, ensure_ascii=False)
        print(f"  wrote {out_path}")

    print(f"\nDone — {len(items)} item(s) written as flat *.item.json files.")
    print("Upload them to your repo root (no subfolder), along with the")
    print("updated config.yml, netlify.toml, build.js and admin.html.")


if __name__ == "__main__":
    main()
