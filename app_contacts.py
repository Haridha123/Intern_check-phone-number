                                                                                            # -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import threading
import time
from datetime import datetime
from whatsapp.selenium_checker import check_whatsapp_number, create_persistent_driver, initialize_whatsapp_session

app = Flask(__name__)

# Global variables for session management
driver_instance = None
session_initialized = False
checking_status = {"running": False, "progress": 0, "total": 0, "results": []}

def initialize_driver():
    global driver_instance, session_initialized
    try:
        driver_instance = create_persistent_driver()
        session_initialized = initialize_whatsapp_session(driver_instance)
        return session_initialized
    except Exception as e:
        print(f"Error initializing driver: {e}")
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/initialize", methods=["POST"])
def initialize_session():
    global session_initialized
    if not session_initialized:
        success = initialize_driver()
        return jsonify({"success": success})
    return jsonify({"success": True, "message": "Already initialized"})

@app.route("/api/check-single", methods=["POST"])
def check_single():
    global driver_instance, session_initialized
    
    if not session_initialized:
        return jsonify({"error": "Session not initialized"})
    
    data = request.get_json()
    number = data.get("number", "").strip()
    
    if not number:
        return jsonify({"error": "No number provided"})
    
    try:
        result = check_whatsapp_number(number, driver_instance)
        return jsonify({
            "number": number,
            "registered": result,
            "message": "Found in contacts" if result else "Not in contacts",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/check-batch", methods=["POST"])
def check_batch():
    global driver_instance, session_initialized, checking_status
    
    if not session_initialized:
        return jsonify({"error": "Session not initialized"})
    
    data = request.get_json()
    numbers = data.get("numbers", [])
    
    if not numbers:
        return jsonify({"error": "No numbers provided"})
    
    # Reset status
    checking_status = {"running": True, "progress": 0, "total": len(numbers), "results": []}
    
    def batch_process():
        global checking_status
        for i, number in enumerate(numbers):
            try:
                result = check_whatsapp_number(number.strip(), driver_instance)
                checking_status["results"].append({
                    "number": number,
                    "registered": result,
                    "message": "Found in contacts" if result else "Not in contacts"
                })
                checking_status["progress"] = i + 1
                time.sleep(1)  # Small delay between checks
            except Exception as e:
                checking_status["results"].append({
                    "number": number,
                    "error": str(e)
                })
        checking_status["running"] = False
    
    thread = threading.Thread(target=batch_process)
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Batch checking started", "total": len(numbers)})

@app.route("/api/status")
def get_status():
    return jsonify(checking_status)

@app.route("/api/session-status")
def session_status():
    return jsonify({
        "initialized": session_initialized,
        "driver_active": driver_instance is not None
    })

if __name__ == "__main__":
    print(" Starting WhatsApp Checker Web Interface...")
    print(" Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
