from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open your target page
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    
    page.wait_for_timeout(2000)

    # Locate elements
    source = page.locator("#column-a")
    target = page.locator("#column-b")

    # Drag source to target
    source.drag_to(target)

    page.wait_for_timeout(5000)
    browser.close()