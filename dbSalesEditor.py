import os
import sqlite3
import uuid
import bcrypt

def edit_database():
    connectionPath = os.path.join("db/salesdb", "sales_now.db")
    connection = sqlite3.connect(connectionPath)
    cursor = connection.cursor()

    # ADD COLUMN
    
    # Barcode
    # cursor.execute("ALTER TABLE inv_static ADD COLUMN barcode TEXT")
    # cursor.execute("CREATE UNIQUE INDEX idx_inv_static_barcode ON inv_static(barcode)")

    # EDIT CELL
    # cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",("13-05-25","C004"))  
    # DELETE ENTRY
    #cursor.execute("DELETE FROM ingredients WHERE inventory_id = 'IN014'")

    # DELETE COLUMN
    #cursor.execute("ALTER TABLE ingredients DROP COLUMN 'C011'")

    # DELETE TABLE
    # cursor.execute("DROP TABLE IF EXISTS sales_now")
    # for i in range(6, 10): 
    #     table_name = f"d{i}"
    #     cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # EDIT TABLE NAME
    #cursor.execute("ALTER TABLE this_month RENAME TO apr")
    # for i in range(1, 10):  # d1 to d9
    #     old_name = f"d{i}"
    #     new_name = f"d{str(i).zfill(2)}"  # zero-pads single digits to 2 digits
    #     cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")

    # Sales Yearly
    # cursor.execute(f"""
    #         CREATE TABLE IF NOT EXISTS sales_y2025 (
    #             inv_id TEXT PRIMARY KEY,
    #             inv_desc TEXT,
    #             quantity_sold INTEGER,
    #             price REAL,
    #             sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #         )
    # """)

    # for i in range(1, 10):  # d01-d09
    #     table_name = f"d0{i}"
    #     cursor.execute(f"""
    #         CREATE TABLE IF NOT EXISTS {table_name} (
    #             inv_id TEXT PRIMARY KEY,
    #             inv_desc TEXT,
    #             quantity_sold INTEGER,
    #             price REAL,
    #             sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #         )
    # """)

    # for i in range(10, 31):  # d10-d30
    #     table_name = f"d{i}"
    #     cursor.execute(f"""
    #         CREATE TABLE IF NOT EXISTS {table_name} (
    #             inv_id TEXT PRIMARY KEY,
    #             inv_desc TEXT,
    #             quantity_sold INTEGER,
    #             price REAL,
    #             sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #         )
    #     """)
    
    # months = ("jan","feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    # for i in range(12):  # d01-d09
    #     cursor.execute(f"""
    #         CREATE TABLE IF NOT EXISTS {months[i]} (
    #             inv_id TEXT PRIMARY KEY,
    #             inv_desc TEXT,
    #             quantity_sold INTEGER,
    #             price REAL,
    #             sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #         )
    # """)
    
    # Sales Now
    
    # data_sales_now = [
    #         (),
    #     ]
    
    # cursor.executemany("""
    #     INSERT OR IGNORE INTO sales_today (inv_id, inv_desc, quantity_sold, price, sales_total)
    #     VALUES (?, ?, ?, ?, ?)              
    # """, data_sales_now)
    
    connection.commit()
    connection.close()
edit_database()