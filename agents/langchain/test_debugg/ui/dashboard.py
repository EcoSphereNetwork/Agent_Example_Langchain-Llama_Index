from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Endpoint to handle queries from the frontend.
    """
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    # Use the dynamic dispatcher to execute the query
    response = execute_query_dynamically(query)
    return jsonify({"response": response})


def monitor_logs():
    """
    Background thread to monitor logs and emit updates via WebSocket.
    """
    log_path = "./logs"
    last_mod_times = {}

    while True:
        time.sleep(5)  # Check every 5 seconds
        for file in os.listdir(log_path):
            if file.endswith(".log"):
                filepath = os.path.join(log_path, file)
                mod_time = os.path.getmtime(filepath)
                if filepath not in last_mod_times or last_mod_times[filepath] != mod_time:
                    last_mod_times[filepath] = mod_time
                    with open(filepath, "r") as f:
                        lines = f.readlines()[-10:]  # Last 10 lines
                        socketio.emit("log_update", {"file": file, "lines": lines})


@app.route('/api/logs', methods=['GET'])
def fetch_logs():
    """
    Endpoint to fetch analyzed logs.
    """
    logs = enhanced_log_parser(log_dir="./logs")
    return jsonify(logs)


if __name__ == '__main__':
    threading.Thread(target=monitor_logs).start()
    socketio.run(app, debug=True, port=5000)
