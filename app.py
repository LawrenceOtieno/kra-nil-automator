import os
import sys
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

app = Flask(__name__)

def load_credentials():
    load_dotenv()
    return {
        "pin": os.getenv("KRA_PIN", ""),
        "password": os.getenv("KRA_PASSWORD", "")
    }

@app.route("/")
def index():
    creds = load_credentials()
    message = request.args.get("message", "")
    status = request.args.get("status", "")
    return render_template("index.html", pin=creds["pin"], password=creds["password"], message=message, status=status)

@app.route("/save", methods=["POST"])
def save_config():
    pin = request.form.get("pin", "").strip().upper()
    password = request.form.get("password", "").strip()
    try:
        with open(".env", "w") as f:
            f.write(f"KRA_PIN={pin}\n")
            f.write(f"KRA_PASSWORD={password}\n")
        return redirect(url_for("index", message="Environment variables synchronized successfully!", status="success"))
    except Exception as e:
        return redirect(url_for("index", message=f"Failed to save configurations: {e}", status="error"))

@app.route("/launch-browser", methods=["POST"])
def launch_browser():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen([sys.executable, "-c", "import dashboard; dashboard.launch_debug_edge()"], cwd=script_dir)
        return redirect(url_for("index", message="Dedicated debugging Edge interface launched. Keep it open!", status="success"))
    except Exception as e:
        return redirect(url_for("index", message=f"Browser execution fault: {e}", status="error"))

@app.route("/run-login", methods=["POST"])
def run_login():
    creds = load_credentials()
    if not creds["pin"] or not creds["password"]:
        return redirect(url_for("index", message="Aborted: Missing active credentials profile.", status="error"))
    try:
        subprocess.Popen([sys.executable, "-m", "src.engine.login"])
        return redirect(url_for("index", message="Automation engine active! Look at your open Edge window, solve the math problem, and type the answer in.", status="success"))
    except Exception as e:
        return redirect(url_for("index", message=f"Failed to spin up script automation loop: {e}", status="error"))

if __name__ == "__main__":
    print("\n--- Starting KRA Nil Automator Pro Premium Flask Subsystem Engine ---")
    print("Open your web browser and navigate to: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)