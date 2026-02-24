import csv


from playwright.sync_api import sync_playwright


def sync_work():
    # открыть соединение
    with sync_playwright() as p:
        # инициализация браузера (с явным открытием браузера)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context() #page init
        page = context.new_page()

        network_requests = []
        page.on("request", lambda request: network_requests.append({
            "url": request.url,
            "method": request.method,
            "type": request.resource_type,
            "headers": request.headers
        }))

        base_url = "https://market.yandex.ru/"

        for page_num in range(1, 3):
            page.goto(f"{base_url}?cp={page_num}", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

        with open("network_traffic.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "method", "type", "headers"], delimiter=";")
            writer.writeheader()
            writer.writerows(network_requests)

        page.screenshot(path='./demo.png')
        browser.close()

sync_work()