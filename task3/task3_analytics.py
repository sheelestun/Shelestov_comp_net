import time

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Переход на HTTP сайт
    page.goto("http://example.com")
    time.sleep(2)

    # Переход на HTTPS сайт
    page.goto("https://example.com")
    time.sleep(2)

    browser.close()