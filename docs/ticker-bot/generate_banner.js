const puppeteer = require("puppeteer");
const fs = require("fs");
const stats = require("./stats.json");

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
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html);
  await page.setViewport({ width: 1024, height: 40 });

  await page.screenshot({ path: "ticker-bot/output/ticker.gif" });
  await browser.close();
})();
