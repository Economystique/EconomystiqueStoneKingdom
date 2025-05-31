import os
import sqlite3
import json
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import torch
from transformers import pipeline, GPTNeoForCausalLM, GPT2Tokenizer
import webview
import threading

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(os.path.join('db', 'users_db.db'))
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT pw_hash FROM user_data WHERE user_name = ?", (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password, result['pw_hash'].encode('utf-8')):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

        conn.close()    
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        confirm_password = request.form['confirm_password'].encode('utf-8')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_data WHERE user_name = ?", (username,))
        if cursor.fetchone():
            flash('Username already exists.', 'error')
            conn.close()
            return redirect(url_for('signup'))
        
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        cursor.execute("INSERT INTO user_data (user_name, pw_hash) VALUES (?, ?)",
                      (username, pw_hash.decode('utf-8')))
        conn.commit()
        conn.close()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get sales performance data
    cursor.execute("""
        SELECT strftime('%Y-%m', date) as month,
               SUM(total_amount) as total_sales
        FROM sales
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    """)
    sales_data = cursor.fetchall()
    
    # Get expired products
    cursor.execute("""
        SELECT *
        FROM inventory
        WHERE expiry_date < date('now')
    """)
    expired_products = cursor.fetchall()
    
    # Get best selling products
    cursor.execute("""
        SELECT p.name,
               COUNT(*) as sale_count,
               SUM(s.total_amount) as total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.id
        GROUP BY p.id
        ORDER BY sale_count DESC
        LIMIT 5
    """)
    best_sellers = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                         sales_data=sales_data,
                         expired_products=expired_products,
                         best_sellers=best_sellers)

@app.route('/inventory')
@login_required
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get ingredients
    cursor.execute("SELECT * FROM inventory ORDER BY name")
    ingredients = cursor.fetchall()
    
    # Get products
    cursor.execute("SELECT * FROM products ORDER BY name")
    products = cursor.fetchall()

    conn.close()
    
    return render_template('inventory.html',
                         ingredients=ingredients,
                         products=products)

@app.route('/sales')
@login_required
def sales():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get sales data
    cursor.execute("""
        SELECT s.*,
               p.name as product_name
        FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.date DESC
    """)
    sales_data = cursor.fetchall()
    
    conn.close()
    
    return render_template('sales.html', sales_data=sales_data)

@app.route('/pos')
@login_required
def pos():
    conn = get_db_connection()
    cursor = conn.cursor()
 
    # Get available products
    cursor.execute("SELECT * FROM products WHERE stock > 0 ORDER BY name")
    products = cursor.fetchall()
    
    conn.close()
    
    return render_template('pos.html', products=products)

@app.route('/account')
@login_required
def account():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data WHERE user_name = ?", (session['username'],))
    user_data = cursor.fetchone()
    
    conn.close()
    
    return render_template('account.html', user_data=user_data)

# API endpoints for AJAX calls
@app.route('/api/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    if product['stock'] < quantity:
        conn.close()
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_item = {
        'id': product['id'],
        'name': product['name'],
        'price': product['price'],
        'quantity': quantity,
        'total': product['price'] * quantity
    }
    
    conn.close()
    return jsonify(cart_item)

@app.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json()
    cart_items = data.get('cart_items', [])
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for item in cart_items:
            # Update product stock
            cursor.execute("""
                UPDATE products
                SET stock = stock - ?
                WHERE id = ?
            """, (item['quantity'], item['id']))
            
            # Record sale
            cursor.execute("""
                INSERT INTO sales (product_id, quantity, total_amount, date)
                VALUES (?, ?, ?, datetime('now'))
            """, (item['id'], item['quantity'], item['total']))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Checkout successful'})
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales_forecast', methods=['POST'])
@login_required
def sales_forecast():
    data = request.get_json()
    product_id = data.get('product_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get historical sales data
    cursor.execute("""
        SELECT date, quantity
        FROM sales
        WHERE product_id = ?
        ORDER BY date
    """, (product_id,))
    sales_history = cursor.fetchall()
    
    if not sales_history:
        conn.close()
        return jsonify({'error': 'No sales history found'}), 404
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(sales_history, columns=['date', 'quantity'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # Simple forecasting using moving average
    forecast = df['quantity'].rolling(window=7).mean().iloc[-1]

    conn.close()
    return jsonify({
        'forecast': round(forecast, 2),
        'history': df['quantity'].tolist()
    })

def start_server():
    app.run(port=5000)

if __name__ == '__main__':
    # Start Flask server in a separate thread
    threading.Thread(target=start_server, daemon=True).start()
    
    # Create and show the window
    webview.create_window('Economystique', 
                         'http://127.0.0.1:5000',
                         width=1920,
                         height=1080,
                         resizable=True,
                         min_size=(640, 360))
    webview.start()