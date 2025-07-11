import pandas as pd
from playwright.sync_api import sync_playwright
import time

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context()
        page = context.new_page()

        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=90000)

        print("⏳ Waiting for JS variable window.storeLocator.locations...")
        for i in range(90):  # Wait up to 90 seconds
            try:
                if page.evaluate("window.storeLocator?.locations?.length > 0"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            print("❌ Timeout: dealer data never loaded.")
            return []

        print("✅ Data found! Extracting...")
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
        print(f"✅ Saved {len(df)} dealers to aspen_us_dealers.csv")
    else:
        print("⚠️ No data scraped.")
