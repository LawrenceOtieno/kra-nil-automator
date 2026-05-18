import os
import sys
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    message = request.args.get("message", "")
    status = request.args.get("status", "")
    return render_template("index.html", message=message, status=status)

@app.route("/launch-browser", methods=["POST"])
def launch_browser():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen([sys.executable, "-c", "import dashboard; dashboard.launch_debug_edge()"], cwd=script_dir)
        return redirect(url_for("index", message="Dedicated debugging Edge window launched successfully!", status="success"))
    except Exception as e:
        return redirect(url_for("index", message=f"Browser execution fault: {e}", status="error"))

@app.route("/run-login", methods=["POST"])
def run_login():
    # 🌟 CAPTURE DYNAMIC IN-MEMORY CREDENTIALS FROM ACTIVE WEB USER
    pin = request.form.get("pin", "").strip().upper()
    password = request.form.get("password", "").strip()
    
    if not pin or not password:
        return redirect(url_for("index", message="Aborted: Runtime fields cannot be blank.", status="error"))
    
    try:
        # Pass the dynamic credentials as command-line positional flags straight to the execution hook
        subprocess.Popen([
            sys.executable, "-m", "src.engine.login", 
            "--pin", pin, 
            "--password", password
        ])
        return redirect(url_for("index", message=f"Automation engine ignited for profile {pin}! Complete the math challenge in the Edge window.", status="success"))
    except Exception as e:
        return redirect(url_for("index", message=f"Failed to hook automation subprocess: {e}", status="error"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)