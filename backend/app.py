from flask import Flask
from flask_cors import CORS
from routes.analyze import analyze_bp

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

app.register_blueprint(analyze_bp)

@app.route('/health', methods=['GET'])
def health():
    return {"status": "Backend is running!"}

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')