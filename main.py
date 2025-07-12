import pandas as pd
from playwright.sync_api import sync_playwright
import gspread
from google.oauth2.service_account import Credentials

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
                            "Website": marker.get("website", "")
                        })
                except Exception as e:
                    print("Error parsing response:", e)

        page.on("response", handle_response)
        print("➡️ Visiting Aspen dealer locator...")
        page.goto("https://www.aspenfuels.us/store-locator/")
        page.wait_for_timeout(5000)
        browser.close()

        df = pd.DataFrame(scraped_data)
        df.to_csv("aspen_us_dealers.csv", index=False)
        print("✅ Scraped", len(scraped_data), "dealers and saved to aspen_us_dealers.csv")

        # Upload to Google Sheets
        upload_to_google_sheet(
            "aspen_us_dealers.csv",
            "https://docs.google.com/spreadsheets/d/1Lf1juxeVFhvqQRT8l0iN6A_jJEBZnkP9dgNj8dZ9KXY/edit"
        )

def upload_to_google_sheet(csv_path, spreadsheet_url):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("teak-amphora-464115-j9-61acbdb757b6.json", scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(spreadsheet_url)
    worksheet = sheet.get_worksheet(0)

    df = pd.read_csv(csv_path)
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

if __name__ == "__main__":
    scrape_aspen_dealers()

