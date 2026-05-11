
#!! Abbott sensitive data removed. HTML and CSS specific to IBM Maximo !!

from pipette_cert_parse import extract_calibration_fields
from playwright.sync_api import sync_playwright, Locator, FrameLocator
import pandas as pd
import os
import time

def run():
    with sync_playwright() as p:
        #Initiate browser
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            "maximo_website_link.com",
            wait_until="domcontentloaded",
        )

        #auto login maximo
        page.get_by_role("button", name="Log in with SAML").click()


        #Click through to main page
        print("wait")
        input()
        
        #initiates frame in which all maximo content resides
        frame = page.locator("iframe[title=\"Production-version_private\"]")
        # Interact inside the frame
        time.sleep(4)
        frame.content_frame.get_by_role("link", name="Work Order Tracking").click()

        #Press enter once in WOT to start processing certs
        print("Press enter to begin:")
        input()

        #Folder with pdfs from Rainin
        folder_path = "path_to_folder"
        #creates list of files in folder
        files = os.listdir(folder_path)

        #Variables for showing progress
        num_files = len(files)
        count = 0

        #Main loop for parsing through pipette certificates
        for file in files:
            count += 1

            #grabs specific certs file path and enters it into pipette parse module.
            file_path = os.path.join(folder_path, file)
            #returns different fields based on pdf certificate
            result = extract_calibration_fields(file_path)

            #playwright processing
            frame.content_frame.get_by_role("textbox", name="Asset").click()
            frame.content_frame.get_by_role("textbox", name="Asset").fill(result["asset_id"])
            frame.content_frame.get_by_role("textbox", name="Asset").press("Enter")
            frame.content_frame.locator("[id='m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:0]']").click()
            frame.content_frame.get_by_role("tab", name="Data Sheet").click()

            #Checks as found and as left content
            if(result["as_found"] == 'Passed' and result["as_left"] == 'Passed'):
                frame.content_frame.get_by_role("textbox", name="As Found Set Point").click()
                frame.content_frame.get_by_role("textbox", name="As Found Set Point").fill("1")
                frame.content_frame.get_by_role("textbox", name="As Left Set Point").click()
                frame.content_frame.get_by_role("textbox", name="As Left Set Point").fill("1")
                if(result["adjustment"] == "No-Adjustment made"):
                    frame.content_frame.get_by_role("checkbox", name="No Adj Made").click()
            elif(result["as_found"] != 'Passed' and result["as_left"] == 'Passed'):
                frame.content_frame.get_by_role("textbox", name="As Found Set Point").click()
                frame.content_frame.get_by_role("textbox", name="As Found Set Point").fill("0")
                frame.content_frame.get_by_role("textbox", name="As Left Set Point").click()
                frame.content_frame.get_by_role("textbox", name="As Left Set Point").fill("1")
            else:
                print("pipette failed")
                break


            frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
            frame.content_frame.get_by_role("tab", name="Log").click()
            frame.content_frame.locator("[id='m524afe2e_bg_button_addrow-pb_addrow_a']").click()
            frame.content_frame.get_by_role("textbox", name="Details").click()

            #Cert fields returned from "extract_calibration_fields" function
            as_found = result["as_found"]
            as_left = result["as_left"]
            pm = result["preventive_maintenance"]
            adjustment = result["adjustment"]
            p_number = result["asset_id"]

            #log comment to be entered in maximo based off of fields
            log_comment = "Checked Vendor Certificate \n" \
            f"As found: {as_found} \n" \
            f"As left: {as_left} \n" \
            f"PM: {pm} \n" \
            f"{adjustment} \n" \
            "Passed all checks"

            frame.content_frame.get_by_role("textbox", name="Details").fill(log_comment)
            frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
            frame.content_frame.get_by_role("tab", name="Actuals").click()
            frame.content_frame.get_by_role("checkbox", name="Done").first.click()
            frame.content_frame.get_by_role("checkbox", name="Done").nth(1).click()
            frame.content_frame.get_by_role("checkbox", name="Done").nth(2).click()
            frame.content_frame.locator("#m4dfd8aef_bg_button_addrow-pb_addrow_a").click()
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).click()
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).fill("username")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).press("Tab")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Approved").press("Tab")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor Date").press("Tab")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Regular Hours").fill(".25")
            frame.content_frame.get_by_role("menuitem", name="Perform Work Order").click()
            frame.content_frame.get_by_label("System Message").get_by_role("button", name="OK").click()
            frame.content_frame.get_by_role("button", name="OK").click()
            frame.content_frame.get_by_role("textbox", name="Password").fill("password")
            frame.content_frame.get_by_role("textbox", name="Password").press("Tab")
            frame.content_frame.get_by_role("textbox", name="Reason For Change:").fill("work done")
            frame.content_frame.get_by_label("Electronic Signature Authentication Dialog Button Group").get_by_role("button", name="OK").click()
            frame.content_frame.get_by_role("button", name="Close", exact=True).click()
            frame.content_frame.get_by_role("link", name="List ViewList View").click()

            print(f"{count}/{num_files} - {p_number}")
        input("\nDone. Press Enter to close…")
        browser.close()

if __name__ == "__main__":
    run()



