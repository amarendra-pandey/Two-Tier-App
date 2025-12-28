from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Backend: Logic to connect to the MySQL database (Tier 2)
def get_db_connection():
    return mysql.connector.connect(
        host="db", # <--- FIX: Use the service name from docker-compose
        user="root",
        password="password",
        database="testdb"
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM messages')
        data = cursor.fetchall() # Get data from MySQL
        cursor.close()
        conn.close()
        return render_template('index.html', messages=[row[0] for row in data])
    except Exception as e:
        # If this fails, you will see the error in your browser
        return f"Database Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Port 5000 is required for the project [cite: 31]