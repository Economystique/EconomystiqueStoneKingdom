import os
import sqlite3
import bcrypt

def init_db():
    # Create db directory if it doesn't exist
    if not os.path.exists('db'):
        os.makedirs('db')

    # Connect to database
    conn = sqlite3.connect('db/users_db.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        pw_hash TEXT NOT NULL,
        owner_name TEXT,
        contact TEXT,
        biz_name TEXT,
        industry TEXT,
        biz_type TEXT,
        address TEXT,
        avatar_blob BLOB,
        biz_logo_blob BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Add new columns to existing table if they don't exist
    def add_column_if_not_exists(table, column, column_type):
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
            print(f"Added column {column} to {table}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {column} already exists in {table}")
            else:
                print(f"Error adding column {column}: {e}")

    # Add profile columns to existing user_data table
    add_column_if_not_exists('user_data', 'title', 'TEXT')
    add_column_if_not_exists('user_data', 'owner_name', 'TEXT')
    add_column_if_not_exists('user_data', 'contact', 'TEXT')
    add_column_if_not_exists('user_data', 'biz_name', 'TEXT')
    add_column_if_not_exists('user_data', 'industry', 'TEXT')
    add_column_if_not_exists('user_data', 'biz_type', 'TEXT')
    add_column_if_not_exists('user_data', 'address', 'TEXT')
    add_column_if_not_exists('user_data', 'avatar_blob', 'BLOB')
    add_column_if_not_exists('user_data', 'biz_logo_blob', 'BLOB')

    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        image TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create inventory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity REAL NOT NULL DEFAULT 0,
        unit TEXT NOT NULL,
        expiry_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    # Create user activity table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        description TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user_data (id)
    )
    ''')

    # Create default admin user if it doesn't exist
    cursor.execute("SELECT * FROM user_data WHERE user_name = 'admin'")
    if not cursor.fetchone():
        password = "admin123"  # Default password
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO user_data (user_name, email, pw_hash) VALUES (?, ?, ?)",
            ('admin', 'admin@economystique.com', pw_hash.decode('utf-8'))
        )

    # Create sample products
    sample_products = [
        ('Coffee', 'Fresh brewed coffee', 120.00, 100, None),
        ('Tea', 'Assorted tea flavors', 80.00, 150, None),
        ('Sandwich', 'Classic sandwich', 150.00, 50, None),
        ('Cake', 'Fresh baked cake', 200.00, 30, None),
        ('Cookie', 'Homemade cookies', 50.00, 200, None)
    ]

    cursor.execute("SELECT * FROM products LIMIT 1")
    if not cursor.fetchone():
        cursor.executemany(
            "INSERT INTO products (name, description, price, stock, image) VALUES (?, ?, ?, ?, ?)",
            sample_products
        )

    # Create sample inventory items
    sample_inventory = [
        ('Coffee Beans', 10.0, 'kg', '2024-12-31'),
        ('Tea Bags', 500.0, 'pcs', '2024-12-31'),
        ('Bread', 50.0, 'pcs', '2024-03-01'),
        ('Flour', 25.0, 'kg', '2024-12-31'),
        ('Sugar', 20.0, 'kg', '2024-12-31')
    ]

    cursor.execute("SELECT * FROM inventory LIMIT 1")
    if not cursor.fetchone():
        cursor.executemany(
            "INSERT INTO inventory (name, quantity, unit, expiry_date) VALUES (?, ?, ?, ?)",
            sample_inventory
        )

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Database initialized successfully!")
    print("Default admin credentials:")
    print("Username: admin")
    print("Password: admin123")

if __name__ == '__main__':
    init_db() 