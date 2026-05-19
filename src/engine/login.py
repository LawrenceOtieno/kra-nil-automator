import logging
import sys
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Initialize local environment secrets
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

logger = logging.getLogger(__name__)

def login_to_itax():
    """
    Navigates and populates credentials using explicit field activation events,
    then pauses for manual security stamp entry before executing the login pipeline.
    """
    pin = os.getenv("KRA_PIN")
    password = os.getenv("KRA_PASSWORD")
    
    if not pin or not password:
        logger.error("Missing credentials! Check your local .env file.")
        return

    with sync_playwright() as p:
        try:
            logger.info("Connecting to live desktop Microsoft Edge instance via port 9222...")
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            
            logger.info("Navigating to KRA iTax Portal...")
            page.goto("https://itax.kra.go.ke/KRA-Portal/", wait_until="load")
            page.wait_for_timeout(2000)
            
            # 1. Type PIN with explicit element activation
            logger.info("Typing secure environment PIN payload...")
            pin_field = page.locator("#logid")
            pin_field.click()
            pin_field.fill("")  # Clears field and updates structural DOM state
            pin_field.type(pin, delay=100)
            page.wait_for_timeout(500)
            
            # 2. Trigger validation loops
            logger.info("Simulating field exit via 'Tab'...")
            page.keyboard.press("Tab")
            page.wait_for_timeout(2500)
            
            # 3. Click Continue
            logger.info("Clicking the validation 'Continue' button...")
            page.locator("a:has-text('Continue')").first.click()
            
            # 4. Wait for form transition fields
            logger.info("Waiting for password input field to render...")
            page.wait_for_selector("input[type='password']", timeout=15000)
            
            # 5. Type Password with explicit element activation
            logger.info("Injecting secure password...")
            password_field = page.locator("input[type='password']").first
            password_field.click()
            password_field.fill("")  # Clears any virtual keyboard cache hooks
            password_field.type(password, delay=100)
            page.wait_for_timeout(500)
            
            # Focus on security stamp answer box
            captcha_field = page.locator("#captcahText, input[name='captchaText']").first
            captcha_field.click()
            captcha_field.fill("")
            
            # 6. High-Timeout Dynamic Wait Loop
            logger.info("=== MANUAL STAMP ACTION TIMELOCK ACTIVE ===")
            logger.info("Take your time! Look at Edge, calculate the math problem, and type it in.")
            
            # 5-minute patient waiting window
            for _ in range(600):  
                current_value = captcha_field.input_value()
                if len(current_value.strip()) > 0:
                    logger.info(f"Detected manual input: '{current_value}'. Processing submission sequence...")
                    page.wait_for_timeout(800)  # Breath window to guarantee final character registration
                    break
                page.wait_for_timeout(500)
            else:
                logger.warning("Timed out waiting for manual security stamp entry after 5 minutes.")
                return
            
            # 7. Force Submission Paths
            logger.info("Invoking page submission pipelines...")
            
            # Path A: Trigger page form execution script directly
            page.evaluate("try { loginSubmit(); } catch(e) {}")
            
            # Path B: Backup click ignoring typical structural wait-checks
            try:
                page.locator("#Image4, img[src*='login']").first.click(timeout=1000, force=True)
            except:
                pass
            
            # Keep browser alive briefly to witness the dashboard load fully
            page.wait_for_timeout(6000)
            logger.info("Login wrapper script operation complete.")
                
        except Exception as e:
            logger.error(f"Execution failed: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    print("--- Running Smart-Wait Edge Login Engine ---")
    login_to_itax()