const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

// ✅ Always resolve relative to this file
const rootDir = path.resolve(__dirname, "..", "..");
const statsPath = path.join(__dirname, "stats.json");
const outputPath = path.join(__dirname, "output", "ticker.gif");

let stats;
try {
  stats = JSON.parse(fs.readFileSync(statsPath, "utf8"));
} catch (err) {
  console.error("[ERROR] Could not read stats.json:", err.message);
  process.exit(1);
}

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
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  await page.setContent(html);
  await page.setViewport({ width: 1024, height: 40 });

  await page.screenshot({ path: outputPath });
  await browser.close();
})();
