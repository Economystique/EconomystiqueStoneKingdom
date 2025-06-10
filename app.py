import os
import sqlite3
import json
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from collections import defaultdict
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
    conn = sqlite3.connect(os.path.join('db', 'inventory_db.db'))
    cursor = conn.cursor()
    
    # From Static
    cursor.execute("""
        SELECT inv_id, inv_desc, cat, sub_cat, unit, rop
        FROM inv_static
    """
    )
    invStatic = cursor.fetchall()
    
    # From Dynamic    
    cursor.execute("""
        SELECT inv_id, quantity FROM inv_dynamic
    """)
    invDynamic = cursor.fetchall()
    conn.close()
    
     # Sum quantities from inv_dynamic by inv_id
    quantity_map = defaultdict(float)
    for inv_id, quantity in invDynamic:
        quantity_map[inv_id] += quantity
    
    # Combine data
    merged_data = []
    for inv_id, inv_desc, cat, sub_cat, unit, rop in invStatic:
        total_qty = quantity_map.get(inv_id, 0)
        merged_data.append({
            "inv_id": inv_id,
            "inv_desc": inv_desc,
            "cat": cat,
            "sub_cat": sub_cat,
            "quantity": total_qty,
            "rop": rop,
            "unit": unit
        })
    
    # Extract categories
    categories = sorted(set(product['cat'] for product in merged_data))
    
    return render_template('products.html', products=merged_data, categories=categories)

@app.route('/sales')
@login_required
def sales():
    
 # Dummy data for sales
    dummy_sales = [
        {
            'product_id': 'PT001',
            'product_name': 'Chopao',
            'price': 100,
            'quantity_sold': '10'
        },
        {
            'product_id': 'PT002',
            'product_name': 'Bottle Water',
            'price': 100,
            'quantity_sold': '20'
        },
        {
            'product_id': 'PT003',
            'product_name': 'Butter',
            'price': 100,
            'quantity_sold': '10'
        },
        {
            'product_id': 'PT004',
            'product_name': 'Ice Cream',
            'price': 100,
            'quantity_sold': '30'
        },
        {
            'product_id': 'PT005',
            'product_name': 'Sanitary Pads',
            'price': 100,
            'quantity_sold': '20'
        },
        {
            'product_id': 'PT006',
            'product_name': 'Detergent',
            'price': 100,
            'quantity_sold': '40'
        },
        {
            'product_id': 'PT007',
            'product_name': 'Notebook',
            'price': 100,
            'quantity_sold': '30'
        },
        {
            'product_id': 'PT008',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '50'   
        },
        {
            'product_id': 'PT009',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '40'
        },
        {
            'product_id': 'PT010',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '60'
        },
        {
            'product_id': 'PT011',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '50'
        },
        {
            'product_id': 'PT012',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '70'
        },
        {
            'product_id': 'PT013',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '60'
        },
        {
            'product_id': 'PT014',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '80'
        },
        {
            'product_id': 'PT015',
            'product_name': 'Cat Food',
            'price': 100,
            'quantity_sold': '10'
        }
    ]

    return render_template('sales.html', sales_data=dummy_sales)

@app.route('/performance_comparison')
@login_required
def performance_comparison():

    # Dummy data for performance comparison
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2022', '2023', '2024', '2025']
    return render_template('performance_comparison.html', months=months, years=years)

#Dummy LOGIC
@app.route('/get_performance_data')
@login_required
def get_performance_data():
    month = request.args.get('month')
    year = request.args.get('year')

    # Simulated product data (same products as /sales)
    all_products = [
        'Chopao', 'Bottle Water', 'Butter', 'Ice Cream', 'Sanitary Pads',
        'Detergent', 'Notebook', 'Cat Food'
    ]

    # Dummy logic to assign values (varies slightly by month/year)
    import random
    random.seed(hash(month + year))  # same results for same inputs

    labels = all_products
    values = [random.randint(5, 20) * 100 for _ in labels]  # Sales amount in pesos

    return jsonify({'labels': labels, 'values': values})

@app.route('/wastage')
@login_required
def wastage():

    #Dummy data for wastage
    dummy_wastage = [
        {
            'inventory_id': 'IN001',
            'product_name': 'Will to live',
            'quantity': '100',
            'unit': 'my life',
            'wastage date': 'May 01, 2025',
            'remarks': 'wasting my life away'
        },
        {
            'inventory_id': 'IN002',
            'product_name': 'Mental stability',
            'quantity': '100',
            'unit': 'per brain cells',
            'wastage date': 'May 01, 2025',
            'remarks': 'Im losing it bro'
        },
        {
            'inventory_id': 'IN003',
            'product_name': 'Chopao',
            'quantity': '10',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Spoilage'
        },
        {
            'inventory_id': 'IN004',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN005',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN006',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN007',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN008',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN009',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN010',
            'product_name': 'Cat Food',
            'quantity': '25',
            'unit': 'pcs',
            'wastage date': 'May 01, 2025',
            'remarks': 'Item/s expired'
        },
        {
            'inventory_id': 'IN011',
            'product_name': 'Kim Ongchangco',
            'quantity': '35',
            'unit': 'per head',
            'wastage date': 'May 01, 2025',
            'remarks': 'bro is too old'
        },
        {
            'inventory_id': 'IN012',
            'product_name': 'Pixel Megatron I',
            'quantity': '1',
            'unit': 'cat',
            'wastage date': 'May 01, 2025',
            'remarks': 'bro is not even 1 yr old but is already too fat'
        },
        {
            'inventory_id': 'IN013',
            'product_name': 'Patato',
            'quantity': '1',
            'unit': 'kilo',
            'wastage date': 'May 01, 2025',
            'remarks': 'Patata? Patoto?'
        },
        {
            'inventory_id': 'IN014',
            'product_name': 'Tomato',
            'quantity': '1',
            'unit': 'kilo',
            'wastage date': 'May 01, 2025',
            'remarks': 'Tomayto or tomatoe? hmmmm...'
        },
        {
            'inventory_id': 'IN015',
            'product_name': 'Elsa',
            'quantity': '1',
            'unit': 'n/a',
            'wastage date': 'May 01, 2025',
            'remarks': 'Let it gooooo let it gooooo'
        },
        {
            'inventory_id': 'IN016',
            'product_name': 'Michael Jackson',
            'quantity': '69',
            'unit': 'dead',
            'wastage date': 'May 01, 2025',
            'remarks': 'hee hee'
        },
        {
            'inventory_id': 'IN017',
            'product_name': 'Emoglobin',
            'quantity': '1',
            'unit': 'alpha',
            'wastage date': 'May 01, 2025',
            'remarks': 'Cause tonoigh will be the noigh that i was born fer yew aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa lorem ipsum hehehe'
        }
    ]

    return render_template('wastage.html', wastage_data=dummy_wastage)

    return render_template('performance_comparison.html')

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