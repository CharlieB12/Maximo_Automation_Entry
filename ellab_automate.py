
#!! Abbott sensitive data removed. HTML and CSS specific to IBM Maximo !!


from playwright.sync_api import sync_playwright, Locator, FrameLocator
import pandas as pd

df = pd.read_excel("C:\\Path_to_file", sheet_name="sheet_name", engine="openpyxl")
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
        print(len(df))
        print("wait")
        input()

        frame = page.locator("iframe[title=\"Production-version_private\"]")
        # Interact inside the frame
        time.sleep(4)
        frame.content_frame.get_by_role("link", name="Work Order Tracking").click()
        print("Press enter to begin:")
        input()
        total = len(df)
        count = 0
        for row in df.itertuples(index=True):
            if(abs(row.found32-row.left32)>2):
                print(f"32c tests OOT, ENDING PROGRAM {str(row.tag_id)}")
                break
            elif(abs(row.found250-row.left250)>1):
                print(f"250c tests OOT, ENDING PROGRAM {str(row.tag_id)}")
                break
            elif(abs(row.found275-row.left275)>1):
                print(f"275c tests OOT. ENDING PROGRAM {str(row.tag_id)}")
                break
            
            frame.content_frame.get_by_role("textbox", name="Tag Id").click()
            frame.content_frame.get_by_role("textbox", name="Tag Id").fill(str(row.tag_id))
            frame.content_frame.get_by_role("textbox", name="Tag Id").press("Enter")
            
            frame.content_frame.locator("[id='m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:0]']").click()
            frame.content_frame.get_by_role("tab", name="Data Sheet").click()
            frame.content_frame.get_by_role("textbox", name="As Found Input").click()
            frame.content_frame.get_by_role("textbox", name="As Found Input").fill(str(row.found32))
            frame.content_frame.get_by_role("textbox", name="As Found Input").press("Tab")
            frame.content_frame.get_by_role("textbox", name="As Found Output").fill(str(row.left32))
            frame.content_frame.get_by_role("cell", name="Description Long Description").nth(2).click()
            frame.content_frame.get_by_role("textbox", name="As Found Input").first.click()
            frame.content_frame.get_by_role("textbox", name="As Found Input").first.fill(str(row.found250))
            frame.content_frame.get_by_role("textbox", name="As Found Input").first.press("Tab")
            frame.content_frame.get_by_role("textbox", name="As Found Output").first.fill(str(row.left250))
            frame.content_frame.get_by_role("textbox", name="As Found Input").nth(1).click()
            frame.content_frame.get_by_role("textbox", name="As Found Input").nth(1).fill(str(row.found275))
            frame.content_frame.get_by_role("textbox", name="As Found Input").nth(1).press("Tab")
            frame.content_frame.get_by_role("textbox", name="As Found Output").nth(1).fill(str(row.left275))
            frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
            frame.content_frame.get_by_role("row", name="View Details 10 Description").get_by_label("No Adj Made").click()
            frame.content_frame.get_by_role("row", name="View Details 20 Description").get_by_label("No Adj Made").click()
            frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
            frame.content_frame.get_by_role("tab", name="Actuals").click()
            frame.content_frame.get_by_role("checkbox", name="Done").first.click()
            frame.content_frame.get_by_role("checkbox", name="Done").nth(1).click()
            frame.content_frame.get_by_role("checkbox", name="Done").nth(2).click()
            frame.content_frame.get_by_role("checkbox", name="Done").nth(3).click()
            frame.content_frame.get_by_role("tab", name="Tools").click()
            frame.content_frame.locator("#m1ff58cdc_bg_button_addrow-pb_addrow_a").click()
            frame.content_frame.get_by_role("textbox", name="Rotating Asset").click()
            frame.content_frame.get_by_role("textbox", name="Rotating Asset").fill("p-0115")
            frame.content_frame.get_by_role("tab", name="Labor").click()
            frame.content_frame.locator("#m4dfd8aef_bg_button_addrow-pb_addrow_a").click()
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).click()
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).fill("username")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor", exact=True).press("Tab")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Approved").press("Tab")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Labor Date").press("Tab")
            frame.content_frame.get_by_role("row", name="Close Details Task Select").get_by_label("Regular Hours").fill("1")
            frame.content_frame.get_by_role("menuitem", name="Save Work Order").click()
            frame.content_frame.get_by_role("menuitem", name="Perform Work Order").click()
            frame.content_frame.get_by_label("System Message").get_by_role("button", name="OK").click()
            frame.content_frame.get_by_role("button", name="OK").click()
            frame.content_frame.get_by_role("textbox", name="Password").click()
            frame.content_frame.get_by_role("textbox", name="Password").fill("password")
            frame.content_frame.get_by_role("textbox", name="Reason For Change:").click()
            frame.content_frame.get_by_role("textbox", name="Reason For Change:").fill("work done")
            frame.content_frame.get_by_label("Electronic Signature Authentication Dialog Button Group").get_by_role("button", name="OK").click()
            frame.content_frame.get_by_role("button", name="Close", exact=True).click()
            frame.content_frame.get_by_role("link", name="List ViewList View").click()
            count += 1
            print(f"{row.p_number} Complete. {count}/{total}")

        input("\nDone. Press Enter to close…")
        browser.close()

if __name__ == "__main__":
    run()