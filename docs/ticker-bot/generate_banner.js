import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

// Path handling
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "../../");

// Puppeteer args
const isCI = process.env.CI === "true";
const args = ["--use-gl=egl"];
if (isCI) args.unshift("--no-sandbox", "--disable-setuid-sandbox");

// Paths
const statsPath = path.join(rootDir, "docs/ticker-bot/stats.json");
const outputGif = path.join(rootDir, "docs/ticker-bot/ticker.gif");
const frameDir = path.join(rootDir, "docs/ticker-bot/frames");

// Load stats
const stats = JSON.parse(fs.readFileSync(statsPath, "utf8"));
if (!stats.length) throw new Error("⚠️ No stats found — check stats.json");

// Compose marquee
const scrollText = stats.map(s =>
  `🔎 ${s.repo} :: ⭐ ${s.stars} | 🍴 ${s.forks} | 👁️ ${s.views} Views | 🧠 ${s.uniques} Clones`
).join(" — ");

const html = `
<html>
  <body style="margin:0; background:black;">
    <marquee behavior="scroll" direction="left" scrollamount="2" loop="infinite"
      style="color:red; font-family:monospace; font-size:36px; padding:20px;">
      ${scrollText}
    </marquee>
  </body>
</html>
`;

(async () => {
  const browser = await puppeteer.launch({ headless: true, args });
  const page = await browser.newPage();
  await page.setViewport({ width: 1024, height: 120 });
  await page.setContent(html);
  await new Promise(r => setTimeout(r, 500));

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

  // Dynamically calculate screencast duration
  const chars = scrollText.length;
  const scrollSpeed = 20; // px/sec (approx)
  const pixels = chars * 18; // est px per char
  const duration = Math.max(Math.ceil((pixels / scrollSpeed / 1024) * 1000), 15000);

  await new Promise(r => setTimeout(r, duration));
  await client.send("Page.stopScreencast");
  await browser.close();

  if (!frames.length) throw new Error("❌ No frames captured — screencast failed.");

  fs.mkdirSync(frameDir, { recursive: true });

  frames.forEach((img, i) => {
    fs.writeFileSync(`${frameDir}/frame_${String(i).padStart(3, "0")}.jpg`, img);
  });

  execSync(`ffmpeg -y -framerate 24 -i ${frameDir}/frame_%03d.jpg -vf "scale=1024:120:flags=lanczos" -loop 0 ${outputGif}`);
  fs.rmSync(frameDir, { recursive: true, force: true });

  console.log(`[✅] ticker.gif rendered with ${frames.length} frames.`);
})();
