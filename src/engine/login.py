import logging
import sys
import os
from playwright.sync_api import sync_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.ocr_helper import solve_security_stamp

logger = logging.getLogger(__name__)

def login_to_itax(pin: str, password: str, test_mode: bool = True):
    """
    Automates KRA iTax by connecting directly to a running desktop Microsoft Edge instance over port 9222.
    """
    with sync_playwright() as p:
        try:
            logger.info("Connecting to live desktop Microsoft Edge instance via port 9222...")
            # Connects directly to Edge's open debugging pipeline
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            
            # Use the existing tab or open a clean one inside Edge
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            
            logger.info("Navigating to KRA iTax Portal...")
            page.goto("https://itax.kra.go.ke/KRA-Portal/", wait_until="load")
            page.wait_for_timeout(3000)
            
            # 1. Focus and interactively type the PIN payload
            logger.info(f"Typing PIN payload: {pin}")
            page.locator("#logid").click()
            page.keyboard.type(pin, delay=120)
            page.wait_for_timeout(500)
            
            # 2. Fire field blur natively using Tab to trigger KRA's background parameter scripts
            logger.info("Simulating field exit via 'Tab'...")
            page.keyboard.press("Tab")
            page.wait_for_timeout(2000)
            
            # 3. Click the 'Continue' anchor tag discovered by our earlier DOM scan
            logger.info("Clicking the validation 'Continue' button via Edge browser context...")
            page.locator("a:has-text('Continue')").first.click()
            
            # 4. Wait for the security math challenge label to reveal itself
            logger.info("Waiting for security math challenge element to appear...")
            page.wait_for_selector("#lblcaptcha", timeout=15000)
            
            challenge_text = page.locator("#lblcaptcha").text_content()
            logger.info(f"Extracted Portal Question: '{challenge_text.strip()}'")
            
            captcha_solution = solve_security_stamp(challenge_text)
            logger.info(f"Computed solution: {captcha_solution}")
            
            # 5. Inject remaining credentials natively
            logger.info("Injecting password and security token values...")
            page.locator("input[type='password']").focus()
            page.keyboard.type(password, delay=80)
            
            page.locator("#captcahText").focus()
            page.keyboard.type(captcha_solution, delay=80)
            
            logger.info("Form parameters successfully populated.")
            if test_mode:
                page.wait_for_timeout(5000)
                
        except Exception as e:
            logger.error(f"Execution failed during login process sequence: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    print("--- Running Microsoft Edge CDP Hijack Login Engine ---")
    login_to_itax(pin="A012345678Z", password="TestPassword123", test_mode=True)