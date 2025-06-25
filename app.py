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
import random
import torch
from transformers import pipeline, GPTNeoForCausalLM, GPT2Tokenizer
import webview
import threading
import smtplib
from email.message import EmailMessage

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
        login_identifier = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_name, pw_hash FROM user_data WHERE user_name = ? OR email = ?", (login_identifier, login_identifier))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password, result['pw_hash'].encode('utf-8')):
            session['username'] = result['user_name']
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
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        confirm_password = request.form['confirm_password'].encode('utf-8')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_data WHERE user_name = ? OR email = ?", (username, email))
        if cursor.fetchone():
            flash('Username or email already exists.', 'error')
            conn.close()
            return redirect(url_for('signup'))
        
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        cursor.execute("INSERT INTO user_data (user_name, email, pw_hash) VALUES (?, ?, ?)",
                      (username, email, pw_hash.decode('utf-8')))
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

#for manage button in inventory/products
@app.route('/manage')
def manage():
    #add here
    return render_template('manage.html')

@app.route('/sales')
@login_required
def sales():
    conn = sqlite3.connect(os.path.join('db/salesdb', 'sales_now.db'))
    cursor = conn.cursor()
    
    # From Static
    cursor.execute("""
        SELECT inv_id, inv_desc, quantity_sold, price, sales_total
        FROM sales_today
    """
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    today_sales = [
        {
            'inv_id': row[0],
            'inv_desc': row[1],
            'quantity_sold': row[2],
            'price': row[3],
            'sales_total': row[4],
        } for row in rows
    ]

    return render_template('sales.html', sales_data = today_sales)

@app.route('/sales_forecast', methods=['GET'])
@login_required
def sales_forecast():
    product_id = request.args.get('product', type=int)

    products = [
        {'id': 1, 'name': 'Chocolate Cake'},
        {'id': 2, 'name': 'Red Velvet'},
        {'id': 3, 'name': 'Cheesecake'}
    ]

    selected_product = next((p for p in products if p['id'] == product_id), None)

    month_labels = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']

    actual_data = []
    forecast_data_full_line = []
    current_month = 5  # June (index 6, so forecast starts from July)

    sales_trend_message = ""

    if selected_product:
        for i in range(12):
            actual_data.append(None if i > current_month else random.randint(100, 200))
            forecast_data_full_line.append(random.randint(150, 250))

        # Forecast trend analysis for next month only
        if current_month + 1 < 12:
            forecast_current = forecast_data_full_line[current_month]       
            forecast_next = forecast_data_full_line[current_month + 1]     

            if forecast_current and forecast_next:
                diff = forecast_next - forecast_current
                pct_change = (diff / forecast_current) * 100
                trend = "INCREASE" if diff > 0 else "DECREASE"
                trend_color = "#3fd55b" if diff > 0 else "red"
                next_month_name = month_labels[current_month + 1]

                sales_trend_message = (
                    f"Sales are expected to <strong><span style='color: {trend_color};'>{trend}</span></strong> "
                    f"in <strong>{next_month_name}</strong> by "
                    f"<strong><span style='color: {trend_color};'>{abs(pct_change):.1f}%</span></strong> "
                    f"based on forecasted values."
                )


    return render_template('sales_forecast.html',
                           products=products,
                           selected_product_id=product_id,
                           labels=month_labels,
                           actual_data=actual_data,
                           forecast_data_full_line=forecast_data_full_line,
                           sales_trend_message=sales_trend_message)

@app.route('/performance_comparison')
@login_required
def performance_comparison():

    # Dummy data for performance comparison
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2022', '2023', '2024', '2025']
    return render_template('performance_comparison.html', months=months, years=years)

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

@app.route('/get_year_performance_data')
@login_required
def get_year_performance_data():
    year = request.args.get('year')

    # reuse your product list
    all_products = [
        'Chopao', 'Bottle Water', 'Butter', 'Ice Cream', 'Sanitary Pads',
        'Detergent', 'Notebook', 'Cat Food'
    ]

    # 12 months, deterministic per year
    monthly_totals = []
    import random, calendar
    for month_idx in range(1, 13):             # 1‑12 to ha
        random.seed(hash(f"{year}-{month_idx}"))
        # randomd dummy sum of all product sales that month
        month_sum = sum(random.randint(5, 20) * 100 for _ in all_products)
        monthly_totals.append(month_sum)

    return jsonify({'monthly_totals': monthly_totals})

@app.route('/wastage')
@login_required
def wastage():
    conn = sqlite3.connect(os.path.join('db', 'wastage_db.db'))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT inv_id, inv_desc, quantity, unit, dec_date, remark FROM wastage_record
    """)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows (tuples) into list of dicts
    wastage_record = [
        {
            'inv_id': row[0],
            'inv_desc': row[1],
            'quantity': row[2],
            'unit': row[3],
            'dec_date': row[4],
            'remark': row[5]
        } for row in rows
    ]
    return render_template('wastage.html', wastage_data=wastage_record)

#modal for declaring wastage
@app.route('/declare_wastage', methods=['POST'])
def declare_wastage():
    inv_id   = request.form['inv_id']
    quantity = float(request.form['quantity'])
    dec_date = request.form['dec_date']
    remark   = request.form.get('remark', '')

    # add DB + inventory shit logic here u got dis kim lessgow!
    
    flash('Wastage recorded successfully!', 'success')
    return redirect(url_for('wastage'))

@app.route('/pos')
@login_required
def pos():
    products = [
        {
            "id": 1,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 2,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 3,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 4,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 5,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 6,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 7,
            "name":
              "Red Velvet",
            
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 8,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        },
        {
            "id": 9,
            "name": "Red Velvet",
            "price": 375.00,
            "stock": 12,
            "image": None  # No image fallback
        }
    ]
    
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

def send_recovery_email(to_email, username):
    # Configure your SMTP server settings here
    SMTP_SERVER = 'smtp.example.com'  # e.g., 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = 'your_email@example.com'
    SMTP_PASSWORD = 'your_email_password'

    msg = EmailMessage()
    msg['Subject'] = 'Account Recovery - Economystique'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.set_content(f"Hello {username},\n\nYou requested a password reset for your Economystique account. If this was you, please follow the instructions provided by the administrator to reset your password.\n\nIf you did not request this, you can ignore this email.\n\nBest regards,\nEconomystique Team")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending recovery email: {e}")
        return False

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('recovery_email')
    if not email:
        flash('Please enter your email address.', 'error')
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM user_data WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result:
        username = result['user_name']
        if send_recovery_email(email, username):
            flash('A recovery email has been sent to your address.', 'success')
        else:
            flash('Failed to send recovery email. Please try again later.', 'error')
    else:
        flash('No account found with that email address.', 'error')
    conn.close()
    return redirect(url_for('login'))

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