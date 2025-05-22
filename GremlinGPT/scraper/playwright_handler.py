from playwright.async_api import async_playwright
from backend.globals import CFG

PROFILE = CFG["scraper"]["browser_profile"]


async def get_dom_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(PROFILE, headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        content = await page.content()
        await browser.close()
        return content
