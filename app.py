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
# TEST COMMIT
def dashboard():
    # Dummy data for top products
    best_sellers = [
        {
            'name': 'Chopao',
            'rank': 1,
        },
        {
            'name': 'Bottle Water',
            'rank': 2,
        },
        {
            'name': 'Ice Cream',
            'rank': 3,
        }
    ]

    # Dummy data for least sold products
    least_products = [
        {
            'name': 'Butter',
            'rank': 1,
        },
        {
            'name': 'Sanitary Pads',
            'rank': 2,
        },
        {
            'name': 'Notebook',
            'rank': 3,
        } 
    ]

    # Dummy data for expired products
    near_expiry = [
        {'name': 'Milk', 'quantity': 45, 'expiry_date': '2024-03-15'},
        {'name': 'Yogurt', 'quantity': 30, 'expiry_date': '2024-03-16'},
        {'name': 'Bread', 'quantity': 25, 'expiry_date': '2024-03-14'},
        {'name': 'Fresh Juice', 'quantity': 20, 'expiry_date': '2024-03-15'},
        {'name': 'Cheese', 'quantity': 15, 'expiry_date': '2024-03-13'}
    ]

    #Dummy data for critical items
    critical_items = [
        {
            'name': 'Milk',
            'quantity': 45,
            
        },
        {
            'name': 'Milk',
            'quantity': 45,
            
        },
        {
            'name': 'Milk',
            'quantity': 45,
            
        },
        {
            'name': 'Milk',
            'quantity': 45,
            
        },{
            'name': 'Milk',
            'quantity': 45,
            
        }
    ]

    # Dummy data for sales performance
    sales_data = [
        {'month': '01', 'total_sales': 50},
        {'month': '02', 'total_sales': 150},
        {'month': '03', 'total_sales': 250},
        {'month': '04', 'total_sales': 200},
        {'month': '05', 'total_sales': 300},
        {'month': '06', 'total_sales': 150},
        {'month': '07', 'total_sales': 200},
        {'month': '08', 'total_sales': 100},
        {'month': '09', 'total_sales': 150},
        {'month': '10', 'total_sales': 200},
        {'month': '11', 'total_sales': 350},
        {'month': '12', 'total_sales': 400}
    ]
    return render_template('dashboard.html',
                         sales_data=sales_data,
                         least_products=least_products,
                         near_expiry=near_expiry,
                         best_sellers=best_sellers,
                         critical_items=critical_items)

@app.route('/products')
@login_required
def products():
    # Dummy data for design preview
    dummy_products = [
        {
            'sku': 'PT001',
            'product_name': 'Chopao',
            'category': 'Food',
            'brand': 'Zentra',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT002',
            'product_name': 'Bottle Water',
            'category': 'Beverage',
            'brand': 'SAHUR!',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT003',
            'product_name': 'Butter',
            'category': 'Dairy',
            'brand': 'VitaNest',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT004',
            'product_name': 'Ice Cream',
            'category': 'FrozenFood',
            'brand': 'Sunryze',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT005',
            'product_name': 'Sanitary Pads',
            'category': 'Hygiene',
            'brand': 'VelvoCare',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT006',
            'product_name': 'Detergent',
            'category': 'Home Supplies',
            'brand': 'Nimbus2000',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT007',
            'product_name': 'Notebook',
            'category': 'Stationery',
            'brand': 'Buzzbi',
            'quantity': '20,711',
            'rop': '500'
        },
        {
            'sku': 'PT008',
            'product_name': 'Cat Food',
            'category': 'Miscellaneous',
            'brand': 'FelineFuel',
            'quantity': '20,711',
            'rop': '500'
        },
    ]
    return render_template('products.html', products=dummy_products)

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
def on_loaded():
    webview.windows[0].gui.window.showMaximized()

def start_server():
    app.run(port=5000)

if __name__ == '__main__':
    # Start Flask server in a separate thread
    threading.Thread(target=start_server, daemon=True).start()
    
    # Create and show the window
    webview.create_window('Economystique', 
                         'http://127.0.0.1:5000',
                         maximized=True,
                         resizable=True,
                         min_size=(640, 360))
    webview.start(on_loaded, gui='qt')