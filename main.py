import pandas as pd
from playwright.sync_api import sync_playwright
import subprocess

# Ensure Chromium is available
subprocess.run(["playwright", "install", "chromium"], check=True)

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=60000)

        print("⏳ Waiting for storeLocator DOM element...")
        page.wait_for_selector("#storeLocator", timeout=60000)

        print("✅ Page structure loaded. Trying to extract dealer JS data...")
        dealer_data = page.evaluate("""
            () => {
                if (!window.storeLocator || !window.storeLocator.locations) {
                    return [];
                }
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
    print("🚀 Starting scrape...")
    try:
        data = scrape_aspen_dealers()
        df = pd.DataFrame(data)
        df.to_csv("aspen_us_dealers.csv", index=False)
        print(f"✅ Scraped {len(df)} dealers and saved to aspen_us_dealers.csv")
    except Exception as e:
        print("❌ Error occurred:", e)
        raise

