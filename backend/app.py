from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': '🎬 DreamScape Backend Running!',
        'status': 'online'
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'backend_ready': True
    })

if __name__ == '__main__':
    print('🎬 Starting DreamScape Backend...')
    app.run(debug=True, port=5000)
