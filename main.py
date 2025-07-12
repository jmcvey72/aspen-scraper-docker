import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_aspen_dealers():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page()
        data = []

        def handle_response(response):
            try:
                if "json" in response.headers.get("content-type", ""):
                    print(f"\n📡 URL: {response.url}")
                    json_data = response.json()
                    print(f"🧾 JSON Preview: {str(json_data)[:500]}")  # show first 500 chars
            except Exception as e:
                pass  # skip non-JSON or error responses

        page.on("response", handle_response)

        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/outlets/find-dealer/", timeout=60000)
        page.wait_for_timeout(10000)

        browser.close()
        return data

if __name__ == "__main__":
    data = scrape_aspen_dealers()
    df = pd.DataFrame(data)
    df.to_csv("aspen_us_dealers.csv", index=False)
    print(f"✅ Scraped {len(df)} dealers and saved to aspen_us_dealers.csv")
