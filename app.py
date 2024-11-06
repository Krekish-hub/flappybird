from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["https://krekish-hub.github.io"])

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://krekish-hub.github.io'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route('/api/save_score', methods=['OPTIONS'])
@app.route('/api/highscores', methods=['OPTIONS'])
def options_request():
    return jsonify({}), 200  # Пустой ответ для OPTIONS

@app.route('/api/save_score', methods=['POST'])
def save_score():
    data = request.json
    user_id = data.get('userId')
    score = data.get('record')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE users SET record = GREATEST(record, %s)
                      WHERE user_id = %s''', (score, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/api/highscores', methods=['GET'])
def get_highscores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, record FROM users ORDER BY record DESC LIMIT 10')
    highscores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(highscores), 200

def get_db_connection():
    conn = psycopg2.connect(
        dbname='datab',
        user='postgres',
        password='1',
        host='localhost',
        port=5432,
        options="-c client_encoding=utf8"
    )
    return conn

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
