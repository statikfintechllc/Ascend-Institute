import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const statsPath = path.join(__dirname, "stats.json");
const outputGif = path.join(__dirname, "output", "ticker.gif");
const outputMp4 = path.join(__dirname, "output", "temp.mp4");

const stats = JSON.parse(fs.readFileSync(statsPath, "utf8"));

const html = `
<html>
  <body style="margin:0; background:black;">
    <marquee behavior="scroll" direction="left" scrollamount="6" style="color:red; font-family:monospace; font-size:18px; padding:5px;">
      ${stats.map(s =>
        `📦 ${s.repo} :: ${s.clones} Clones | ${s.views} Views | ${s.uniques} Unique 🧠`
      ).join(" — ")}
    </marquee>
  </body>
</html>
`;

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--use-gl=egl"]
  });

  const page = await browser.newPage();
  await page.setContent(html);
  await page.setViewport({ width: 1024, height: 40 });

  // 🎥 Start screen recording
  const stream = await page.screenshot({ type: 'png' }); // temp fallback
  await page.evaluate(() => {
    window.scrollTo(0, 0);
  });

  // Use Chrome's DevTools Protocol for screencapture:
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

  // Let the marquee scroll for 6 seconds
  await new Promise(resolve => setTimeout(resolve, 6000));
  await client.send("Page.stopScreencast");
  await browser.close();

  // Save to .mp4 using ffmpeg
  const frameDir = path.join(__dirname, "output", "frames");
  fs.mkdirSync(frameDir, { recursive: true });

  frames.forEach((img, idx) => {
    fs.writeFileSync(`${frameDir}/frame_${String(idx).padStart(3, "0")}.jpg`, img);
  });

  execSync(`ffmpeg -y -framerate 10 -i ${frameDir}/frame_%03d.jpg -vf "scale=1024:-1:flags=lanczos" -loop 0 ${outputGif}`);

  // Clean up temp frames
  fs.rmSync(frameDir, { recursive: true, force: true });

  console.log("[✅] Animated ticker.gif created.");
})();
