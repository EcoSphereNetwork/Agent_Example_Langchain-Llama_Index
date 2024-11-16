from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication


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


@app.route('/api/logs', methods=['GET'])
def fetch_logs():
    """
    Endpoint to fetch analyzed logs.
    """
    logs = enhanced_log_parser(log_dir="./logs")
    return jsonify(logs)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
