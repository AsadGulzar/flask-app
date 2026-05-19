from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT version();')
    db_version = cur.fetchone()

    cur.close()
    conn.close()

    return f"PostgreSQL Version: {db_version}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
