import os
import sqlite3
import json
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory, send_file
from functools import wraps
from collections import defaultdict
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import random
import torch
from transformers import pipeline, GPTNeoForCausalLM, GPT2Tokenizer
import smtplib
from email.message import EmailMessage
import webview
import threading
from dateutil.relativedelta import relativedelta
import calendar
import io
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    
    daily_sales = []
    labels = []

    for i in range(9, -1, -1):
        date_check = date.today() - timedelta(days=i)
        year = date_check.year
        month = date_check.strftime('%b').lower()
        day = date_check.day
        table_name = f"d0{day}" if day < 10 else f"d{day}"

        try:
            db_path = os.path.join(f'db/salesdb/daily/sales_d{year}', f'{month}_{year}.db')
            with sqlite3.connect(db_path) as dconn:
                dcursor = dconn.cursor()
                dcursor.execute(f"SELECT SUM(quantity_sold * price) FROM {table_name}")
                total = dcursor.fetchone()[0] or 0
        except Exception:
            total = 0

        labels.append(date_check.strftime('%b %d'))
        daily_sales.append(total)

    return render_template('dashboard.html',
                        labels=labels,
                        quantities=daily_sales,
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

    # Daily Table
    cursor.execute("""
        SELECT inv_id, inv_desc, quantity_sold, price, sales_total
        FROM sales_today
    """)
    rows = cursor.fetchall()
    conn.close()

    sales_data = [
        {
            'inv_id': row[0],
            'inv_desc': row[1],
            'quantity_sold': row[2],
            'price': row[3],
            'sales_total': row[4],
        } for row in rows
    ]
    
    # Line Graph Data
    daily_sales = []
    labels = []

    for i in range(9, -1, -1):
        date_check = date.today() - timedelta(days=i)
        year = date_check.year
        month = date_check.strftime('%b').lower()
        day = date_check.day
        table_name = f"d0{day}" if day < 10 else f"d{day}"

        try:
            db_path = os.path.join(f'db/salesdb/daily/sales_d{year}', f'{month}_{year}.db')
            with sqlite3.connect(db_path) as dconn:
                dcursor = dconn.cursor()
                dcursor.execute(f"SELECT SUM(quantity_sold * price) FROM {table_name}")
                total = dcursor.fetchone()[0] or 0
        except Exception:
            total = 0

        labels.append(date_check.strftime('%b %d'))  # e.g. Jul 02
        daily_sales.append(total)

    return render_template('sales.html', sales_data=sales_data, labels=labels, quantities=daily_sales)

@app.route('/api/sales/<period>')
@login_required
def get_sales_data(period):
    # Map period to actual table names in your database
    table_map = {
        'daily': 'sales_today',
        'monthly': 'sales_this_month',
        'yearly': 'sales_this_year'
    }

    months = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    
    dateTodayFull = date.today()
    thisYear = dateTodayFull.year
    thisMonth = dateTodayFull.month
    thisDay = dateTodayFull.day
    
    month_index = thisMonth - 1
    month_str = months[month_index]
    
    table_name = table_map.get(period)
    if not table_name:
        return jsonify({'error': 'Invalid period'}), 400
    
    # Daily
    if period == "daily":
        # Parse the selected date or default to today
        date_param = request.args.get('date')
        try:
            if date_param:
                base_date = datetime.strptime(date_param, "%Y-%m-%d").date()
            else:
                base_date = date.today()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

        # Line Graph Data: Get sales of 10 days up to selected day
        daily_sales = []
        labels = []

        for i in range(9, -1, -1):
            date_check = base_date - timedelta(days=i)
            year = date_check.year
            month = date_check.strftime('%b').lower()
            day = date_check.day
            table_name = f"d0{day}" if day < 10 else f"d{day}"

            try:
                db_path = os.path.join(f'db/salesdb/daily/sales_d{year}', f'{month}_{year}.db')
                with sqlite3.connect(db_path) as dconn:
                    dcursor = dconn.cursor()
                    dcursor.execute(f"SELECT SUM(quantity_sold * price) FROM {table_name}")
                    total = dcursor.fetchone()[0] or 0
            except Exception:
                total = 0

            labels.append(date_check.strftime('%b %d'))  # e.g. Jun 28
            daily_sales.append(total)

        # Table Data: get only from the selected day (not current)
        target_year = base_date.year
        target_month = base_date.strftime('%b').lower()
        target_day = base_date.day
        table_name = f"d0{target_day}" if target_day < 10 else f"d{target_day}"
        try:
            db_path = os.path.join(f'db/salesdb/daily/sales_d{target_year}', f'{target_month}_{target_year}.db')
            with sqlite3.connect(db_path) as tconn:
                tcursor = tconn.cursor()
                tcursor.execute(f"""
                    SELECT inv_id, inv_desc, quantity_sold, price, (quantity_sold * price) AS sales_total
                    FROM {table_name}
                """)
                rows = tcursor.fetchall()
        except Exception:
            rows = []

        result = [
            {
                'inv_id': row[0],
                'inv_desc': row[1],
                'quantity_sold': row[2],
                'price': row[3],
                'sales_total': row[4],
            } for row in rows
        ]

        return jsonify({
            'labels': labels,
            'quantities': daily_sales,
            'table': result
        })
        
    # Yearly
    elif period == 'yearly':
        # Get year from query string or default to current year
        selected_year = request.args.get('date', str(date.today().year))
        try:
            selected_year = int(selected_year)
        except ValueError:
            return jsonify({'error': 'Invalid year'}), 400

        db_path = os.path.join('db/salesdb', 'sales_yearly.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all available year tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'sales_y%'")
        tables = [row[0] for row in cursor.fetchall()]

        available_years = sorted([int(name.replace('sales_y', '')) for name in tables])

        start_year = selected_year - 9
        years_to_check = [y for y in range(start_year, selected_year + 1) if y in available_years]

        yearly_sales = []
        labels = []

        for y in years_to_check:
            table = f"sales_y{y}"
            try:
                cursor.execute(f"SELECT SUM(quantity_sold * price) FROM {table}")
                total = cursor.fetchone()[0] or 0
            except Exception:
                total = 0

            yearly_sales.append(total)
            labels.append(str(y))

        # Now get detailed sales from the selected year's table
        result = []
        table_name = f"sales_y{selected_year}"
        if table_name in tables:
            cursor.execute(f"""
                SELECT inv_id, inv_desc, quantity_sold, price, sales_total
                FROM {table_name}
            """)
            rows = cursor.fetchall()
            result = [
                {
                    'inv_id': row[0],
                    'inv_desc': row[1],
                    'quantity_sold': row[2],
                    'price': row[3],
                    'sales_total': row[4],
                } for row in rows
            ]

        conn.close()

        return jsonify({
            'labels': labels,
            'quantities': yearly_sales,
            'table': result,
            'available_years': available_years  # To populate dropdown
        })
    # Monthly
    elif period == 'monthly':
        # Get date param or default to current date
        date_param = request.args.get('date')
        if date_param:
            try:
                target_date = datetime.strptime(date_param, "%Y-%m")
                target_year = target_date.year
                target_month = target_date.month
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        else:
            target_date = date.today()
            target_year = target_date.year
            target_month = target_date.month
        dConn = sqlite3.connect(os.path.join(f'db/salesdb/daily/sales_d{thisYear}', f'{month_str}_{thisYear}.db')) 
        dCursor = dConn.cursor()
        conn = sqlite3.connect(os.path.join('db/salesdb', 'sales_now.db'))
        cursor = conn.cursor()

        # Clear old data
        cursor.execute("DELETE FROM sales_this_month")
        sales_aggregate = {}

        # Summate all entries in the current month
        for x in range(1, thisDay + 1):
            table_name = f"d0{x}" if x < 10 else f"d{x}"
            dCursor.execute(f"""
                SELECT inv_id, inv_desc, SUM(quantity_sold), price
                FROM {table_name}
                GROUP BY inv_id
            """)
            temp_rows = dCursor.fetchall()
            
            for inv_id, inv_desc, qty_sold, price in temp_rows:
                if inv_id not in sales_aggregate:
                    sales_aggregate[inv_id] = [inv_desc, qty_sold, price]
                else:
                    sales_aggregate[inv_id][1] += qty_sold
        dConn.close()
        data_to_insert = [
            (inv_id, desc, qty, price)
            for inv_id, (desc, qty, price) in sales_aggregate.items()
        ]

        cursor.executemany("""
            INSERT INTO sales_this_month (inv_id, inv_desc, quantity_sold, price)
            VALUES (?, ?, ?, ?)
        """, data_to_insert)
        
        # Commit Changes to database
        conn.commit()
        
        # Get Monthly
        cursor.execute("""
            SELECT inv_id, inv_desc, quantity_sold, price, sales_total
            FROM sales_this_month
        """)
        rows = cursor.fetchall()

        conn.close()

        result = [
            {
                'inv_id': row[0],
                'inv_desc': row[1],
                'quantity_sold': row[2],
                'price': row[3],
                'sales_total': row[4],
            } for row in rows
        ]
        # Generate sales totals for the last 10 months
        monthly_sales = []
        month_labels = []
        sales_aggregate = defaultdict(lambda: [None, 0, 0])  # inv_desc, qty, price

        for i in range(9, -1, -1):
            date_check = date(target_year, target_month, 1) - relativedelta(months=i)
            y = date_check.year
            m = date_check.month
            m_str = date_check.strftime('%b').lower()
            db_path = os.path.join(f'db/salesdb/daily/sales_d{y}', f'{m_str}_{y}.db')
            label = f"{m_str.capitalize()} {y}"
            total = 0

            if os.path.exists(db_path):
                try:
                    with sqlite3.connect(db_path) as dConn:
                        dCursor = dConn.cursor()
                        days_in_month = calendar.monthrange(y, m)[1]
                        for day in range(1, days_in_month + 1):
                            table_name = f'd0{day}' if day < 10 else f'd{day}'
                            try:
                                dCursor.execute(f"SELECT inv_id, inv_desc, quantity_sold, price FROM {table_name}")
                                for inv_id, inv_desc, qty, price in dCursor.fetchall():
                                    sales_aggregate[inv_id][0] = inv_desc
                                    sales_aggregate[inv_id][1] += qty
                                    sales_aggregate[inv_id][2] = price
                                    total += qty * price
                            except sqlite3.OperationalError:
                                continue
                except Exception as e:
                    print(f"Error reading {db_path}: {e}")

            monthly_sales.append(total)
            month_labels.append(label)

        # prepare table result
        result = [
            {
                'inv_id': inv_id,
                'inv_desc': data[0],
                'quantity_sold': data[1],
                'price': data[2],
                'sales_total': data[1] * data[2]
            } for inv_id, data in sales_aggregate.items()
        ]

        return jsonify({
            'labels': month_labels,
            'quantities': monthly_sales,
            'table': result
        })

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
    current_month = 5 

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

@app.route('/api/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        file_bytes = file.read()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET avatar_blob = ? WHERE user_name = ?", (file_bytes, session['username']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'avatar_url': url_for('avatar_image', username=session['username'])})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/upload_biz_logo', methods=['POST'])
@login_required
def upload_biz_logo():
    if 'biz_logo' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['biz_logo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        file_bytes = file.read()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET biz_logo_blob = ? WHERE user_name = ?", (file_bytes, session['username']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'logo_url': url_for('biz_logo_image', username=session['username'])})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/avatar_image/<username>')
def avatar_image(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT avatar_blob FROM user_data WHERE user_name = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row['avatar_blob']:
        return send_file(io.BytesIO(row['avatar_blob']), mimetype='image/png')
    else:
        return send_file(os.path.join('static', 'img', 'catholder.jpg'), mimetype='image/jpeg')

@app.route('/biz_logo_image/<username>')
def biz_logo_image(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT biz_logo_blob FROM user_data WHERE user_name = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and row['biz_logo_blob']:
        return send_file(io.BytesIO(row['biz_logo_blob']), mimetype='image/png')
    else:
        return send_file(os.path.join('static', 'img', 'dashboardIcon.png'), mimetype='image/png')

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