
#!! Abbott sensitive data removed. HTML and CSS specific to IBM Maximo !!

from playwright.sync_api import sync_playwright, Locator, FrameLocator
import pandas as pd


df = pd.read_excel("excel_file_path.xlsx", sheet_name="sheet_name", engine="openpyxl")
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            "maximo_website_link.com",
            wait_until="domcontentloaded",
        )

        print("wait")
        input()


        frame = page.locator("iframe[title=\"Production-version_private\"]")
        # Interact inside the frame
        time.sleep(4)
        frame.content_frame.get_by_role("link", name="Work Order Tracking").click()
        print("Press enter to begin:")
        input()
        for row in df.itertuples(index=True):
            if str(row.WorkOrder) != "nan":
                frame.content_frame.get_by_role("textbox", name="Work Order").click()
                frame.content_frame.get_by_role("textbox", name="Work Order").fill(str(row.WorkOrder))
                frame.content_frame.get_by_role("textbox", name="Work Order").press("Enter")
                frame.content_frame.locator("[id='m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:0]']").click()
                frame.content_frame.locator("#mc83937fc-img").click()
                time.sleep(2)
                frame.content_frame.get_by_label("April 6,").get_by_text("6").click()
                frame.content_frame.get_by_text("08:00 AM").click()
                frame.content_frame.get_by_role("button", name="OK").click()
                frame.content_frame.get_by_role("menuitem", name="Change Status").click()
                frame.content_frame.get_by_role("img", name="Drop-down image").click()
                frame.content_frame.get_by_role("menuitem", name="Received", exact=True).click()
                frame.content_frame.get_by_role("button", name="OK").click()
                frame.content_frame.get_by_role("button", name="Close", exact=True).click()
                frame.content_frame.get_by_role("link", name="List ViewList View").click()

                print(f"{str(row.Description)} ---- Received")

        input("\nDone. Press Enter to close…")
        browser.close()

if __name__ == "__main__":
    run()