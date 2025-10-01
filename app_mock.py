from flask import Flask, render_template, request, jsonify
import threading
import time
from datetime import datetime

# Simple mock function for testing
def check_whatsapp_registration(number, driver=None):
    # Mock function that randomly returns True/False for testing
    import random
    time.sleep(1)  # Simulate checking time
    return random.choice([True, False])

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/initialize", methods=["POST"])
def initialize_session():
    return jsonify({"success": True, "message": "Mock session initialized"})

@app.route("/api/check-single", methods=["POST"])
def check_single():
    data = request.get_json()
    number = data.get("number", "").strip()
    
    if not number:
        return jsonify({"error": "No number provided"})
    
    try:
        result = check_whatsapp_registration(number)
        return jsonify({
            "number": number,
            "registered": result,
            "message": "REGISTERED on WhatsApp" if result else "NOT REGISTERED on WhatsApp",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/session-status")
def session_status():
    return jsonify({
        "initialized": True,
        "driver_active": True
    })

if __name__ == "__main__":
    print("Starting WhatsApp Registration Checker (Mock Mode)...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
