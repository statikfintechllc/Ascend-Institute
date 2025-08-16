#!/usr/bin/env node

import { mkdir, writeFile } from "fs/promises";

const base = "docs/G.M.svg";
const files = [
  `${base}/assets/gremlin-mcp-scrap-card.svg`,
  `${base}/scripts/generate-gremlin-mcp-scrap.mjs`,
  `${base}/package.json`,
  `.github/workflows/update-gremlin-mcp-scrap-card.yml`
];

const dirs = [
  `${base}/assets`,
  `${base}/scripts`,
  `.github/workflows`
];

(async () => {
  for (const dir of dirs) await mkdir(dir, { recursive: true });
  for (const file of files) await writeFile(file, "");
  console.log("✅ G.M.svg structure ready");
})();
