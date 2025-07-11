import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        page = browser.new_page()
        data = []

        # Debug log every response
        def handle_response(response):
            url = response.url
            print("📡 Response URL:", url)

            if "locations" in url and response.status == 200:
                try:
                    json_data = response.json()
                    print("✅ Found dealer data!")

                    for loc in json_data:
                        data.append({
                            "name": loc.get("store"),
                            "address": loc.get("address"),
                            "city": loc.get("city"),
                            "state": loc.get("state"),
                            "zip": loc.get("zip"),
                            "phone": loc.get("phone"),
                            "lat": loc.get("lat"),
                            "lng": loc.get("lng"),
                            "url": loc.get("url")
                        })
                except Exception as e:
                    print("❌ Failed to parse JSON:", e)

        page.on("response", handle_response)

        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=60000)
        page.wait_for_timeout(8000)

        browser.close()
        return data

if __name__ == "__main__":
    data = scrape_aspen_dealers()
    df = pd.DataFrame(data)
    df.to_csv("aspen_us_dealers.csv", index=False)
    print(f"✅ Scraped {len(df)} dealers and saved to aspen_us_dealers.csv")
