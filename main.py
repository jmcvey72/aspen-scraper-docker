import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page()
        scraped_data = []

        def handle_response(response):
            if "markers/en-US" in response.url and "json" in response.headers.get("content-type", ""):
                try:
                    json_data = response.json()
                    for marker in json_data.get("markers", []):
                        scraped_data.append({
                            "Dealer Name": marker.get("name", ""),
                            "Address": marker.get("adress", ""),
                            "City": marker.get("city", ""),
                            "Province": marker.get("province", ""),
                            "Postal Code": marker.get("zip_code", ""),
                            "Phone": marker.get("phone", ""),
                            "Website": marker.get("website", ""),
                        })
                except Exception as e:
                    print(f"❌ Failed to parse JSON: {e}")

        page.on("response", handle_response)

        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=60000)
        page.wait_for_timeout(10000)

        browser.close()
        return scraped_data

if __name__ == "__main__":
    data = scrape_aspen_dealers()
    df = pd.DataFrame(data)
    df.to_csv("aspen_us_dealers.csv", index=False)
    print(f"✅ Scraped {len(df)} dealers and saved to aspen_us_dealers.csv")
