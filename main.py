import pandas as pd
from playwright.sync_api import sync_playwright
import subprocess
import os

# Ensure Playwright and Chromium are installed
subprocess.run(["playwright", "install", "chromium"], check=True)

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=60000)

        print("⏳ Waiting for dealer data to load...")
        page.wait_for_function(
            "window.storeLocator && window.storeLocator.locations && window.storeLocator.locations.length > 0",
            timeout=60000
        )

        print("✅ Dealer data found! Extracting...")
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
    print("🚀 Starting scrape...")
    try:
        data = scrape_aspen_dealers()
        df = pd.DataFrame(data)
        output_file = "aspen_us_dealers.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Scraped {len(df)} dealers and saved to {output_file}")
    except Exception as e:
        print("❌ Error occurred:", e)
        raise

