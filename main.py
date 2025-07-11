import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import subprocess
import sys

# Ensure Playwright dependencies are installed (only needed locally)
if __name__ == "__main__" and "playwright" in sys.argv[0]:
    subprocess.run(["playwright", "install", "chromium"], check=True)

def scrape_aspen_dealers():
    with sync_playwright() as p:
        print("🚀 Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("➡️ Visiting Aspen dealer locator page...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=90000)

        try:
            print("⏳ Waiting for locator JS variable to populate...")
            page.wait_for_function(
                "window.storeLocator && window.storeLocator.locations && window.storeLocator.locations.length > 0",
                timeout=60000
            )
        except PlaywrightTimeoutError:
            print("❌ Timeout waiting for storeLocator.locations to load.")
            browser.close()
            return []

        print("✅ Dealer data detected! Extracting now...")
        dealer_data = page.evaluate("""
            () => {
                return window.storeLocator.locations.map(loc => ({
                    name: loc.store,
                    address: loc.address,
                    city: loc.city,
                    state: loc.state,
                    zip: loc.zip,
                    phone: loc.phone,
                    lat: loc.lat,
                    lng: loc.lng,
                    url: loc.url
                }));
            }
        """)
        browser.close()
        return dealer_data

if __name__ == "__main__":
    print("🧹 Starting scrape task...")
    data = scrape_aspen_dealers()
    if data:
        df = pd.DataFrame(data)
        df.to_csv("aspen_us_dealers.csv", index=False)
        print(f"✅ Scraped {len(df)} dealers and saved to aspen_us_dealers.csv")
    else:
        print("⚠️ No data scraped.")
