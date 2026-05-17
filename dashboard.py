import os
import sys
import subprocess
import logging
from dotenv import load_dotenv

# Set up clean terminal logging formatting
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Dashboard Hub")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_environment():
    """Verifies that the .env file exists and contains the necessary credentials."""
    load_dotenv()
    pin = os.getenv("KRA_PIN")
    password = os.getenv("KRA_PASSWORD")
    
    print("=== [ SYSTEM CONFIGURATION CHECK ] ===")
    if pin and password:
        hidden_pass = password[0] + "*" * (len(password) - 2) + password[-1] if len(password) > 2 else "***"
        print(f" STATUS:     [ OK ] Local environment values loaded.")
        print(f" TARGET PIN: {pin}")
        print(f" PASSWORD:   {hidden_pass}")
    else:
        print(" STATUS:     [ ERROR ] Missing credentials in your .env file!")
        print("             Please ensure KRA_PIN and KRA_PASSWORD are set correctly.")
    print("======================================\n")

def launch_debug_edge():
    """Forces old Edge instances to close and opens a fresh remote debugging session using robust paths."""
    logger.info("Recycling desktop Microsoft Edge processes...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    logger.info("Launching isolated Edge window bound to debugging port 9222...")
    
    # Common absolute installation paths for Microsoft Edge on Windows 64-bit and 32-bit
    possible_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "msedge.exe" 
    ]
    
    args = [
        "--remote-debugging-port=9222",
        "--remote-debugging-address=127.0.0.1",
        "--user-data-dir=D:\\Projects\\kra-nil-automator\\edge_profile"
    ]
    
    launched = False
    for path in possible_paths:
        try:
            subprocess.Popen([path] + args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            launched = True
            break
        except FileNotFoundError:
            continue
            
    # Ultimate fallback using the Windows command shell interpretation engine
    if not launched:
        try:
            cmd_string = f'start msedge --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="D:\\Projects\\kra-nil-automator\\edge_profile"'
            subprocess.Popen(cmd_string, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            launched = True
        except Exception as e:
            logger.error(f"Failed to launch Edge via fallback shell: {e}")
            
    if launched:
        print("\n[ SUCCESS ] Debug browser is now active on your screen. Leave it open!\n")
    else:
        print("\n[ ERROR ] Could not automatically start Edge. Please open it manually via command line if needed.\n")

def run_login_engine():
    """Executes the login engine module directly from inside the dashboard context."""
    print("\nExecuting Login Automation Sequence...")
    print("--------------------------------------------------")
    try:
        subprocess.run([sys.executable, "-m", "src.engine.login"])
    except Exception as e:
        logger.error(f"Dashboard failed to hand off execution path: {e}")
    print("--------------------------------------------------\n")

def main_menu():
    while True:
        clear_terminal()
        print("==================================================")
        print("          KRA NIL AUTOMATOR DEVELOPER HUB        ")
        print("==================================================")
        print(" [1] Run System Configuration & Credentials Check ")
        print(" [2] Launch Dedicated Debugging Edge Instance     ")
        print(" [3] Execute Login Engine (Smart-Wait Mode)      ")
        print(" [4] Exit Dashboard                              ")
        print("==================================================")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            clear_terminal()
            check_environment()
            input("Press Enter to return to main menu...")
        elif choice == '2':
            clear_terminal()
            launch_debug_edge()
            input("Press Enter to return to main menu...")
        elif choice == '3':
            clear_terminal()
            run_login_engine()
            print("Handoff complete! You can now manually fill your Nil Returns in the Edge window.")
            input("\nPress Enter to return to main menu...")
        elif choice == '4':
            print("\nExiting Automator Hub. Happy tax filing!")
            break
        else:
            input("\nInvalid selection. Press Enter to try again...")

if __name__ == "__main__":
    main_menu()