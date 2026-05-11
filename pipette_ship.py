
#!! Abbott sensitive data removed. HTML and CSS specific to IBM Maximo !!

from playwright.sync_api import sync_playwright, Locator, FrameLocator
import pandas as pd

#Initializes excel sheet
df = pd.read_excel("excel_file.xlsx", sheet_name="sheet_name", engine="openpyxl")
import time

def run():
    with sync_playwright() as p:
        #Initializes playwright and launches browser
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            "maximo_website_link.com",
            wait_until="domcontentloaded",
        )

        #Wait until page loads, press enter once on maximo default template page.
        print("wait")
        input()

        #Grabs the frame with content needed for data entry
        frame = page.locator("iframe[title=\"Production-version_private\"]")
        time.sleep(4)
        #Clicks WOT
        frame.content_frame.get_by_role("link", name="Work Order Tracking").click()

        #Program begins here once enter is pressed in console.
        print("Press enter to begin:")
        input()
        
        #Variables for keeping track of which pipette is being processed
        num_rows = len(df)
        count = 0

        #Main logic and entering loop. Loops through until all pipetttes are entered.
        for row in df.itertuples(index=True):
            if str(row.Asset) != "nan":
                frame.content_frame.get_by_role("textbox", name="Asset").click()
                frame.content_frame.get_by_role("textbox", name="Asset").fill(str(row.Asset))
                frame.content_frame.get_by_role("textbox", name="Asset").press("Enter")
                frame.content_frame.locator("[id='m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:0]']").click()
                frame.content_frame.locator("#mc83937fc-img").click()
                time.sleep(2)
                frame.content_frame.get_by_role("button", name="OK").click()
                frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
                frame.content_frame.get_by_role("tab", name="Log").click()
                frame.content_frame.get_by_role("button", name="New Row").click()
                frame.content_frame.get_by_role("textbox", name="Details").click()
                frame.content_frame.get_by_role("textbox", name="Details").fill("Shipped to Rainin for calibration on (date). FedEx Tracking #: (num)")
                frame.content_frame.locator("[id='m344e2d37-tb']").click()
                frame.content_frame.locator("[id='m344e2d37-tb']").fill("Shipped.")
                frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
                frame.content_frame.get_by_role("tab", name="Actuals").click()
                frame.content_frame.locator("#m4dfd8aef_bg_button_addrow-pb_addrow_a").click()
                frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).click()
                frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).fill("username")
                frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).press("Tab")
                frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Approved").press("Tab")
                frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor Date").press("Tab")
                frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Regular Hours").fill(".25")
                frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
                frame.content_frame.get_by_role("menuitem", name="Change Status").click()
                frame.content_frame.get_by_role("img", name="Drop-down image").click()
                frame.content_frame.get_by_role("menuitem", name="Sent Off-Site For Cal / Repair").click()
                frame.content_frame.get_by_role("button", name="OK").click()
                frame.content_frame.get_by_role("button", name="Close", exact=True).click()
                frame.content_frame.get_by_role("link", name="List ViewList View").click()
                #Iterate count and print state
                count += 1
                print(f"{count}/{num_rows} - {str(row.Asset)}")

        input("\nDone. Press Enter to close…")
        browser.close()

if __name__ == "__main__":
    run()