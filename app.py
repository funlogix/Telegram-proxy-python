from flask import Flask, request, jsonify, Response
import requests
import os

app = Flask(__name__)

# Get token from env or header
def get_bot_token():
    return request.headers.get("X-Telegram-Token") or os.getenv("TELEGRAM_BOT_TOKEN")

@app.route('/<path:method>', methods=['GET', 'POST'])
def proxy(method):
    token = get_bot_token()
    if not token:
        return jsonify({"error": "Missing Telegram bot token"}), 401

    url = f"https://api.telegram.org/bot{token}/{method}"

    try:
        if request.method == 'POST':
            response = requests.post(url, json=request.get_json())
        else:
            response = requests.get(url, params=request.args)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/file/<path:file_path>', methods=['GET'])
def download_file(file_path):
    token = get_bot_token()
    if not token:
        return jsonify({"error": "Missing Telegram bot token"}), 401

    url = f"https://api.telegram.org/file/bot{token}/{file_path}"

    try:
        response = requests.get(url, stream=True)
        return Response(response.iter_content(chunk_size=8192), content_type=response.headers['Content-Type'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Telegram Proxy is running."
