import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserLink (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER NOT NULL,
            uuid TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/link/<uuid>')
def link(uuid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_user_id FROM UserLink WHERE uuid=?", (uuid,))
    result = cursor.fetchone()
    conn.close()

    user_id = result[0] if result else None
    return render_template('link.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)