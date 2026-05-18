import os
import sys
import logging
from playwright.sync_api import sync_playwright

# --- SYSTEMIC LOGGER CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("AutomationEngine")

# --- CREDENTIAL RESOLUTION HANDLER ---
user_pin = ""
user_password = ""

# If args are passed from our dynamic Flask interface web submission
if "--pin" in sys.argv and "--password" in sys.argv:
    try:
        pin_idx = sys.argv.index("--pin") + 1
        pass_idx = sys.argv.index("--password") + 1
        user_pin = sys.argv[pin_idx].strip().upper()
        user_password = sys.argv[pass_idx].strip()
        logger.info("Dynamic runtime session credentials loaded via application CLI parameters pool.")
    except Exception as arg_err:
        logger.error(f"Failed parsing systemic command-line flags: {arg_err}")

# Fallback block: If no command args exist, look inside local .env configurations (for backward compatibility)
if not user_pin or not user_password:
    from dotenv import load_dotenv
    load_dotenv()
    user_pin = os.getenv("KRA_PIN", "").strip().upper()
    user_password = os.getenv("KRA_PASSWORD", "").strip()
    logger.info("Fallback activated: Credentials resolved out of local workspace environment pools.")

# Validation Gateway
if not user_pin or not user_password:
    logger.critical("Engine Initialization Failure: No identity attributes provided for this processing thread.")
    sys.exit(1)

def run_login_pipeline():
    logger.info("Initializing Playwright sync attachment thread...")
    
    with sync_playwright() as p:
        try:
            # Connect directly to our pre-warmed background browser port instance
            logger.info("Hooking running Edge instance over CDP channel on port 9222...")
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            
            # Access the default context or active tabs
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            
            # 1. Target Portal Navigation
            logger.info("Directing browser focus to target portal domain...")
            page.goto("https://itax.kra.go.ke/KRA-Portal/", timeout=45000)
            page.wait_for_load_state("networkidle")
            
            # 2. Inject Dynamic User PIN
            logger.info(f"Injecting User Identifier Target State: {user_pin}")
            page.locator("#logInAs").wait_for(state="visible", timeout=10000)
            page.fill("#logInAs", user_pin)
            
            # 3. Simulate Gateway Intermediary Action to trigger validation rules
            page.keyboard.press("Tab")
            page.wait_for_timeout(500)
            
            # 4. Inject Password Parameter Asset
            logger.info("Injecting protected account access token vector...")
            page.locator("#txtPrisPswd").wait_for(state="visible", timeout=10000)
            page.fill("#txtPrisPswd", user_password)
            
            # 5. Hand off execution thread to operator for Security Math Challenge
            logger.info("!!! MANUAL INTERVENTION REQUIRED !!!")
            logger.info("Please calculate the math captcha on the screen and type it directly into the browser window.")
            
            # 6. Safety countdown tracking window to allow operator calculation entry
            countdown = 12
            for i in range(countdown, 0, -1):
                logger.info(f"Awaiting user arithmetic inputs... {i}s remaining")
                page.wait_for_timeout(1000)
                
            # 7. Force Submission Paths
            logger.info("Invoking page submission pipelines...")
            
            # Step A: Type a final tab out of the captcha field to ensure state registry
            page.keyboard.press("Tab")
            page.wait_for_timeout(300)
            
            # Step B: Direct, unmitigated hardware click simulation on the official Login button
            try:
                logger.info("Simulating physical hardware pointer strike on Login button...")
                # Targets the red login button asset directly and forces the action overriding hidden layout overlays
                page.locator("#Image4, img[src*='login'], input[type='image']").first.click(force=True, timeout=3000)
            except Exception as click_err:
                logger.warning(f"Selector click stalled ({click_err}), resorting to context evaluation script injection fallback...")
                # Ultimate fallback script path execution
                page.evaluate("try { loginSubmit(); } catch(e) {}")
            
            # Keep browser alive briefly to witness the dashboard load fully
            page.wait_for_timeout(6000)
            logger.info("Login wrapper script operation complete.")
            
        except Exception as runtime_err:
            logger.error(f"Execution thread crash event intercepted: {runtime_err}")

if __name__ == "__main__":
    run_login_pipeline()