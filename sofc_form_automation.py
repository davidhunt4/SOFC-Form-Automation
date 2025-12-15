from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils import get_non_processed, get_relevant_values
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# 1. Connect to Google Sheets
# ----------------------------

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("handy-cell-478015-u7-397b5b7f6c77.json", scopes=scope)
client = gspread.authorize(creds)

# Open sheet and get row values
sheet = client.open("SEC Expense Report").sheet1

# Google Drive API client
drive_service = build("drive", "v3", credentials=creds)

rows = sheet.get_all_values()

non_processed_rows = get_non_processed(rows)

# ----------------------------
# 2. Form Filling
# ----------------------------

# These are the general values in every completed form
gen_values = ["Student Engineers' Council", os.getenv('ACCOUNT_NUM')]

# These are the links
links = {
    "Reimbursement": "https://tamusignature.na4.adobesign.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhCVLKBrDc_cWAihnWcWMVHUGPdRT5kRj6SzN56sQzngdaeHdgaQPcPaq27JukrcVKc*",
    "Invoice": "https://tamusignature.na4.adobesign.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhCVLKBrDc_cWAihnWcWMVHUGPdRT5kRj6SzN56sQzngdaeHdgaQPcPaq27JukrcVKc*",
    "SOFC Credit Card Payment (must be submitted 3-4 weeks in advance)": "https://tamusignature.na4.adobesign.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhAKgftRg2hWBXFO5dH8oeHcW5Vd1pZdBq8-TC0mXLnRYMY2cw7wVVWXI_Di03isn2s*"
}

# These arrays map the input values to the form field numbers
maps = {
    "Reimbursement": [0, 1, 7, 17, 26, 2, 8, 9, 11, 10, 18, 19, 20, 21, 22, 23, 24, 25, 27],
    "Invoice": [0, 1, 17, 26, 2, 7, 8, 9, 11, 18, 19, 20, 21, 22, 23, 24, 25, 27],
    "SOFC Credit Card Payment (must be submitted 3-4 weeks in advance)": [0, 1, 6, 14, 5, 2, 4, 7, 9]
}

# Open the Chrome window with Chrome profile
options = Options()
profile_path = os.path.abspath("selenium-chrome-data")
options.add_argument(f"user-data-dir={profile_path}")
driver = webdriver.Chrome(options=options)

for row in non_processed_rows:
    # First, identify what kind of payment and get relevant values
    payment_type = row[10]

    try:
        current_map = maps[payment_type]
    except KeyError as e: # approval-to-charge case
        print(f"{payment_type} payment type not supported, skipping row.")
        continue

    answer = input(f'Process {payment_type} submitted by {row[1]} ({row[3]})? (yes/no): ')
    if answer.lower() != 'yes':
        continue

    input_values = get_relevant_values(row, payment_type) # get values from this row in the sheet
    full_values = gen_values + input_values + [0] * 9 # this is the list of EVERY value to put into the form

    driver.get(links[payment_type]) # open up the correct link in Chrome window
    time.sleep(3)

    # Selecting correct buttons (for Direct Deposit, TAMU Student, Not Affiliated)
    if payment_type in ["Reimbursement", "Invoice"]:
        radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio']")
        for button in radio_buttons:
            button_value = button.get_attribute("value")
            if button_value == "Direct Deposit":
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)
            elif payment_type == "Invoice" and button_value == "Not Affiliated":
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)
            elif payment_type == "Reimbursement" and button_value == "TAMU Student":
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)

    # Filling in text fields

    fields = driver.find_elements(By.XPATH, "//input | //textarea")

    for value, field_index in zip(full_values, current_map):
        try:
            target_field = fields[field_index]  # Get the WebElement at that index
            target_field.clear()                # Clear any existing text
            target_field.send_keys(value)       # Type the value into the field
            print(f"Entered '{value}' into field #{field_index}")
        except Exception as e:
            print(f"Could not enter '{value}' into field #{field_index}: {e}")
    
    confirm = input('Form Submitted and Signed? (yes/no): ')
    while confirm.lower() != 'yes':
        confirm = input('Form Submitted and Signed? (yes/no): ')
    
print('All rows completed!')
