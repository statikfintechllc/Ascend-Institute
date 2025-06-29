import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const statsPath = path.join(__dirname, "stats.json");
const outputGif = path.join(__dirname, "output", "ticker.gif");

const stats = JSON.parse(fs.readFileSync(statsPath, "utf8"));
if (!stats.length) throw new Error("⚠️ No stats found — check stats.json");

const isCI = process.env.CI === "true";
const args = ["--use-gl=egl"];
if (isCI) args.unshift("--no-sandbox", "--disable-setuid-sandbox");

const html = `
<html>
  <body style="margin:0; background:black;">
    <marquee behavior="scroll" direction="left" scrollamount="6"
      style="color:red; font-family:monospace; font-size:18px; padding:10px;">
      ${stats.map(s =>
        `📦 ${s.repo} :: ${s.clones} Clones | ${s.views} Views | ${s.uniques} Unique 🧠`
      ).join(" — ")}
    </marquee>
  </body>
</html>
`;

(async () => {
  const browser = await puppeteer.launch({ headless: true, args });
  const page = await browser.newPage();

  await page.setViewport({ width: 1024, height: 80 });
  await page.setContent(html);
  await new Promise(r => setTimeout(r, 500)); // wait for marquee render

  const client = await page.target().createCDPSession();
  await client.send("Page.startScreencast", {
    format: "jpeg",
    quality: 80,
    everyNthFrame: 1
  });

  const frames = [];
  client.on("Page.screencastFrame", async ({ data, sessionId }) => {
    frames.push(Buffer.from(data, "base64"));
    await client.send("Page.screencastFrameAck", { sessionId });
  });

  await new Promise(r => setTimeout(r, 6000)); // record for 6 seconds
  await client.send("Page.stopScreencast");
  await browser.close();

  if (!frames.length) throw new Error("❌ No frames captured — screencast failed.");

  const frameDir = path.join(__dirname, "output", "frames");
  fs.mkdirSync(frameDir, { recursive: true });

  frames.forEach((img, i) => {
    fs.writeFileSync(`${frameDir}/frame_${String(i).padStart(3, "0")}.jpg`, img);
  });

  execSync(`ffmpeg -y -framerate 10 -i ${frameDir}/frame_%03d.jpg -vf "scale=1024:80:flags=lanczos" -loop 0 ${outputGif}`);

  fs.rmSync(frameDir, { recursive: true, force: true });
  console.log(`[✅] ticker.gif created with ${frames.length} frames.`);
})();
