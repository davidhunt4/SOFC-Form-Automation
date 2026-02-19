from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Open the Chrome window with a separate profile for Selenium
options = Options()
profile_path = os.path.abspath("selenium-chrome-data")
options.add_argument(f"user-data-dir={profile_path}")

print("Opening Chrome browser with Selenium profile...\n")

driver = webdriver.Chrome(options=options)

try:
    # Navigate to Gmail
    print("Opening Gmail...")
    driver.get("https://mail.google.com")
    
    # Wait for Gmail to load (look for compose button or main UI)
    print("Waiting for Gmail to load...")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='navigation'] | //div[contains(@class, 'T-I-KE')]"))
        )
        print("✓ Gmail loaded successfully")
    except:
        print("⚠️  Gmail may not be loaded or you need to log in")
        print("   Make sure you're logged into Gmail in this browser profile")
    
    time.sleep(2)
    
    # Navigate to SEC Finance label
    print("\nLooking for SEC Finance label...")
    
    # First, let's see what labels are visible (for debugging)
    try:
        all_labels = driver.find_elements(By.XPATH, "//nav//a | //div[contains(@class, 'aim')]//a")
        print(f"Found {len(all_labels)} navigation elements")
        for label in all_labels[:10]:  # Show first 10
            try:
                text = label.text.strip()
                if text:
                    print(f"  - {text}")
            except:
                pass
    except:
        pass
    
    # Try multiple ways to find the SEC Finance label
    sec_finance_label = None
    selectors = [
        "//a[contains(text(), 'SEC Finance')]",
        "//span[contains(text(), 'SEC Finance')]/ancestor::a",
        "//a[contains(@title, 'SEC Finance')]",
        "//*[contains(text(), 'SEC Finance')]"
    ]
    
    print("\nTrying to locate SEC Finance label...")
    for selector in selectors:
        try:
            sec_finance_label = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            print(f"✓ Found SEC Finance label")
            break
        except:
            continue
    
    if sec_finance_label:
        sec_finance_label.click()
        time.sleep(1)
        print("✓ Opened SEC Finance label")
    else:
        print("✗ Could not find SEC Finance label with any selector")
        driver.quit()
        print("Browser closed.")
        exit(1)
    
    # Wait for the confirmation email to arrive (check for up to 5 minutes)
    print("\nWaiting for confirmation email with subject 'Please confirm your submission of SOFC eCheck Request'...")
    email_found = False
    max_attempts = 60  # 60 attempts * 5 seconds = 5 minutes
    attempt = 0
    
    while not email_found and attempt < max_attempts:
        try:
            # Look for unread email with the specific subject
            confirmation_email = driver.find_element(
                By.XPATH,
                "//tr[contains(@class, 'zE')]//span[contains(text(), 'Please confirm your submission of SOFC eCheck Request')]"
            )
            
            if confirmation_email:
                email_found = True
                print("✓ Confirmation email found!")
                
                # Click on the email row to open it
                email_row = confirmation_email.find_element(By.XPATH, "./ancestor::tr")
                email_row.click()
                time.sleep(1.5)
                print("✓ Opened email")
                
                # Find and click the confirmation link in the email
                try:
                    # Wait for email body to load
                    print("Looking for confirmation link in email...")
                    time.sleep(1)
                    
                    # Try multiple selectors for the link
                    link_selectors = [
                        "//a[contains(@href, 'adobesign')]",
                        "//a[contains(@href, 'adobe')]",
                        "//a[contains(text(), 'confirm')]",
                        "//a[contains(text(), 'Click')]",
                        "//a[contains(text(), 'click')]",
                        "//div[@role='main']//a[contains(@href, 'http')]"
                    ]
                    
                    confirmation_link = None
                    for link_selector in link_selectors:
                        try:
                            links = driver.find_elements(By.XPATH, link_selector)
                            if links:
                                confirmation_link = links[0]  # Get first match
                                print(f"✓ Found confirmation link using: {link_selector}")
                                print(f"  Link URL: {confirmation_link.get_attribute('href')}")
                                break
                        except:
                            continue
                    
                    if confirmation_link:
                        confirmation_link.click()
                        print("✓ Clicked confirmation link!")
                        time.sleep(2)
                        print("\n✓✓✓ Gmail automation test completed successfully! ✓✓✓")
                    else:
                        print("✗ Could not find any link in the email")
                    
                except Exception as e:
                    print(f"✗ Error finding/clicking confirmation link: {e}")
                
        except Exception:
            # Email not found yet, wait and try again
            attempt += 1
            print(f"  Waiting for confirmation email... (attempt {attempt}/{max_attempts})")
            time.sleep(5)
            driver.refresh()
            time.sleep(2)
    
    if not email_found:
        print("✗ Confirmation email did not arrive within 5 minutes")
    
    print("\nWaiting 3 seconds before closing browser...")
    time.sleep(3)

except Exception as e:
    print(f"\n✗ Error occurred: {e}")
    time.sleep(3)
    
finally:
    driver.quit()
    print("Browser closed.")
