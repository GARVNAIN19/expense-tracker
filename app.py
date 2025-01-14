from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Important for security

# Database setup
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            category TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table() # Create the table on startup

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()
    total_expenses = sum(expense['amount'] for expense in expenses)
    return render_template('index.html', expenses=expenses, total_expenses=total_expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        category = request.form['category']
        date = request.form['date']
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%d')

        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (amount, description, category, date) VALUES (?, ?, ?, ?)',
                     (amount, description, category, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')


@app.route('/view_expenses')
def view_expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('view_expenses.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)