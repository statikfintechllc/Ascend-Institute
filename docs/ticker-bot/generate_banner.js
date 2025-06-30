// docs/ticker-bot/generate_banner.js

import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "../../");

const statsPath = path.join(rootDir, "docs/ticker-bot/stats.json");
const outputGif = path.join(rootDir, "docs/ticker-bot/ticker.gif");
const frameDir = path.join(rootDir, "docs/ticker-bot/frames");

const stats = JSON.parse(fs.readFileSync(statsPath, "utf8"));
if (!stats.length) throw new Error("⚠️ No stats found — check stats.json");

const scrollText = stats.map(s =>
  `🔎 ${s.repo} :: ⭐ ${s.stars} | 🍴 ${s.forks} | 👁️ ${s.views} Views | 🧠 ${s.uniques} Clones | 👀 ${s.watchers} Watchers | 🪲 ${s.open_issues} Issues | 🧵 ${s.pulls_count} PRs | 🧬 ${s.language} | 📦 ${s.size_kb} KB | 🧭 ${s.default_branch} | 📅 ${s.updated_at.slice(0,10)}`
).join(" — ");

const pxPerChar = 18;
const scrollWidth = scrollText.length * pxPerChar;
const screenWidth = 1024;
const scrollSpeed = 45;
const fps = 24;
const framesNeeded = Math.ceil((scrollWidth + screenWidth) / scrollSpeed);
const durationMs = Math.ceil((framesNeeded / fps) * 1000);

const html = `
<html>
  <head>
    <style>
      body {
        margin: 0;
        background: black;
        overflow: hidden;
      }
      #ticker {
        color: red;
        font-family: monospace;
        font-size: 36px;
        padding: 20px;
        white-space: nowrap;
        position: absolute;
        will-change: transform;
        animation: scroll-left ${durationMs}ms linear forwards;
      }
      @keyframes scroll-left {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-${scrollWidth}px); }
      }
    </style>
  </head>
  <body>
    <div id="ticker">${scrollText}</div>
  </body>
</html>
`;

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--use-gl=egl"]
  });
  const page = await browser.newPage();
  await page.setViewport({ width: screenWidth, height: 120 });
  await page.setContent(html);
  await page.evaluate(ms => new Promise(res => setTimeout(res, ms)), durationMs + 500);

  const client = await page.target().createCDPSession();
  await client.send("Page.startScreencast", {
    format: "jpeg",
    quality: 85,
    everyNthFrame: 1
  });

  const frames = [];
  client.on("Page.screencastFrame", async ({ data, sessionId }) => {
    frames.push(Buffer.from(data, "base64"));
    await client.send("Page.screencastFrameAck", { sessionId });
  });

  console.log(`ℹ️ Duration: ${durationMs}ms | Frames: ${framesNeeded}`);

  await page.evaluate(ms => new Promise(res => setTimeout(res, ms)), durationMs + 1000);
  await client.send("Page.stopScreencast");
  await browser.close();

  if (!frames.length) throw new Error("❌ No frames captured — screencast failed.");

  fs.mkdirSync(frameDir, { recursive: true });
  frames.forEach((img, i) => {
    fs.writeFileSync(`${frameDir}/frame_${String(i).padStart(3, "0")}.jpg`, img);
  });

  execSync(`ffmpeg -y -framerate ${fps} -i ${frameDir}/frame_%03d.jpg -vf "scale=${screenWidth}:120:flags=lanczos" -loop 0 ${outputGif}`);
  fs.rmSync(frameDir, { recursive: true, force: true });

  console.log(`[✅] ticker.gif rendered with ${frames.length} frames.`);
})();
