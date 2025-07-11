import pandas as pd
from playwright.sync_api import sync_playwright
import time

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=60000)

        # Wait up to 60 seconds for the JS variable to be populated
        print("⏳ Waiting for dealer data to load (max 60s)...")
        for i in range(60):
            try:
                ready = page.evaluate("Boolean(window.storeLocator && window.storeLocator.locations && window.storeLocator.locations.length > 0)")
                if ready:
                    break
            except:
                pass
            time.sleep(1)
        else:
            print("❌ Timeout waiting for storeLocator.locations to load.")
            return []

        print("✅ Dealer data found! Extracting...")
        dealer_data = page.evaluate("""
            () => window.storeLocator.locations.map(loc => ({
                name: loc.store,
                address: loc.address,
                city: loc.city,
                state: loc.state,
                zip: loc.zip,
                phone: loc.phone,
                lat: loc.lat,
                lng: loc.lng,
                url: loc.url
            }))
        """)
        browser.close()
        return dealer_data

if __name__ == "__main__":
    data = scrape_aspen_dealers()
    if data:
        df = pd.DataFrame(data)
        df.to_csv("aspen_us_dealers.csv", index=False)
        print(f"✅ Scraped {len(df)} dealers and saved to aspen_us_dealers.csv")
    else:
        print("⚠️ No data scraped.")

