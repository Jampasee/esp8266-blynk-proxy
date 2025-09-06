from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Blynk API Configuration
BLYNK_AUTH_TOKEN = "SpF5BbbAfuy3PMCGR-oEU6awEexy-2n7"
BLYNK_SERVER = "blynk.cloud"

# Blynk API URLs
def get_blynk_url(pin):
    return f"https://{BLYNK_SERVER}/external/api/get?token={BLYNK_AUTH_TOKEN}&pin={pin}"

def update_blynk_url(pin, value):
    return f"https://{BLYNK_SERVER}/external/api/update?token={BLYNK_AUTH_TOKEN}&pin={pin}&value={value}"

def is_connected_url():
    return f"https://{BLYNK_SERVER}/external/api/isHardwareConnected?token={BLYNK_AUTH_TOKEN}"

@app.route('/')
def home():
    return jsonify({
        "message": "ESP8266 LED Control Proxy Server",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/api/get/<int:pin>')
def get_pin(pin):
    try:
        url = get_blynk_url(pin)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "pin": pin,
                "value": response.text.strip(),
                "status_code": response.status_code
            })
        else:
            return jsonify({
                "success": False,
                "error": f"HTTP {response.status_code} - {response.text}",
                "pin": pin
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Request failed: {str(e)}",
            "pin": pin
        }), 500

@app.route('/api/update/<int:pin>/<value>')
def update_pin(pin, value):
    try:
        url = update_blynk_url(pin, value)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "pin": pin,
                "value": value,
                "message": "Updated successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": f"HTTP {response.status_code} - {response.text}",
                "pin": pin,
                "value": value
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Request failed: {str(e)}",
            "pin": pin,
            "value": value
        }), 500

@app.route('/api/status')
def get_status():
    try:
        url = is_connected_url()
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            connected = response.text.strip().lower() == 'true'
            return jsonify({
                "success": True,
                "connected": connected,
                "message": "ESP8266 is online" if connected else "ESP8266 is offline"
            })
        else:
            return jsonify({
                "success": False,
                "error": f"HTTP {response.status_code} - {response.text}",
                "connected": False
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Request failed: {str(e)}",
            "connected": False
        }), 500

@app.route('/api/all-pins')
def get_all_pins():
    pins = {}
    for pin in range(1, 5):  # V1 to V4
        try:
            url = get_blynk_url(pin)
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                pins[f"V{pin}"] = response.text.strip()
            else:
                pins[f"V{pin}"] = "error"
                
        except requests.exceptions.RequestException:
            pins[f"V{pin}"] = "error"
    
    return jsonify({
        "success": True,
        "pins": pins
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "blynk-proxy",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
