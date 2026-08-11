from playwright.sync_api import sync_playwright
import time
import os

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        print("Navigating to dashboard...")
        page.goto("http://127.0.0.1:8501")
        time.sleep(5)  # wait for streamlit to load
        os.makedirs("submission/evidence", exist_ok=True)
        page.screenshot(path="submission/evidence/cp2-dashboard.png")
        print("Screenshot saved to submission/evidence/cp2-dashboard.png")
        browser.close()

if __name__ == "__main__":
    main()
