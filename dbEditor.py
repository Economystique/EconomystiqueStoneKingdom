import os
import sqlite3
import uuid
import bcrypt

def edit_database():
    connectionPath = os.path.join("db", "inventory_db.db")
    connection = sqlite3.connect(connectionPath)
    cursor = connection.cursor()

    # ADD COLUMN
    #cursor.execute("ALTER TABLE products_on_hand ADD COLUMN image BLOB")
    
    # EDIT CELL
    # cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",("13-05-25","C004"))  

    # DELETE ENTRY
    #cursor.execute("DELETE FROM ingredients WHERE inventory_id = 'IN014'")
    
    # DELETE COLUMN
    #cursor.execute("ALTER TABLE ingredients DROP COLUMN 'C011'")
    
    # DELETE TABLE
    # cursor.execute("DROP TABLE IF EXISTS sales_now")
    
    # EDIT TABLE NAME
    #cursor.execute("ALTER TABLE this_month RENAME TO apr")
    
    # Wastage
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS wastage_record (
    #     inv_id TEXT PRIMARY KEY,
    #     inv_desc TEXT,
    #     quantity REAL,
    #     unit TEXT,
    #     remark TEXT,
    #     dec_date DATE
    # )
    # """)
    
    # sales
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS sales_this_year (
    #     inv_id TEXT PRIMARY KEY,
    #     inv_desc TEXT,
    #     quantity_sold INTEGER,
    #     price REAL,
    #     sales_total REAL ALWAYS GENERATED AS (quantity_sold * price)STORED
    # )
    # """)
    
    # inv_dynamic
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS inv_dynamic (
    #     actual_id TEXT PRIMARY KEY,
    #     batch_id TEXT,
    #     inv_id TEXT,
    #     quantity INTEGER,
    #     unit TEXT,
    #     exp_date DATE,
    #     rec_date DATE
    # )
    # """)
    
    # restock_cart
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS restock_cart (
    #     inv_id TEXT PRIMARY KEY,
    #     inv_name TEXT,
    #     quantity INTEGER,
    #     unit TEXT,
    #     rop INTEGER,
    #     exp_date DATE,
    #     rec_date DATE
    # )
    # """)
    
    # batch_record
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS batch_record (
    #     batch_id TEXT PRIMARY KEY,
    #     rec_date DATE
    # )
    # """)

    # batches
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS BATCHA00001 (
    #     inv_id TEXT PRIMARY KEY,
    #     inv_desc TEXT,
    #     quantity INTEGER,
    #     unit TEXT,
    #     rop INTEGER,
    #     exp_date DATE,
    #     rec_date DATE
    # )
    # """)

    # ADD DATA
    # data1 = [("ITa00001","Ba00001","INVa00005",36,"piece","2025-06-20","2025-06-04"),
    #         ("ITa00002","Ba00002","INVa00006",20,"bottle","2025-10-15","2025-06-04"),
    #         ("ITa00003","Ba00003","INVa00008",20,"pack","2025-12-10","2025-06-04"),
    #         ("ITa00004","Ba00004","INVa00010",15,"pack","2026-06-20","2025-06-04")
    # ]
    
    # UUID Generation
    # user_name = "admin"
    # uid1 =str(uuid.uuid5(uuid.NAMESPACE_DNS, user_name))
    
    # # PW Acquisition & Byte Conversion
    # pw = "admin123"
    # pw_byte = pw.encode('UTF-8')
    # salt = bcrypt.gensalt()
    # pw_hash = bcrypt.hashpw(pw_byte, salt).decode('utf-8')
    
    # data = [uid1,"admin","economystique@gmail.com",pw_hash,"2025-06-05"]
    
    # ADD TO TABLE
    # cursor.executemany("""
    # INSERT OR IGNORE INTO inv_dynamic (actual_id, batch_id, inv_id, quantity, unit, exp_date, rec_date)
    # VALUES (?, ?, ?, ?, ?, ?, ?)
    # """, data1)

    # ADD BLOB IN COLUMN
    """product_id = "C010"
    image_path = "img/C010.png"
    
    def convert_to_binary(filename):
        with open(filename, 'rb') as file:
            return file.read()
    
    try:
        image_data = convert_to_binary(image_path)
        cursor.execute("UPDATE products_on_hand SET image = ? WHERE product_id = ?", (image_data, product_id))
        connection.commit()
        print(f"Image added successfully to product_id: {product_id}")
    except Exception as e:
        print(f"Failed to update image: {e}")
    finally:
        connection.close()"""
    
    # GET TOTAL PER YEAR
    '''cursor.execute("""
        INSERT INTO year_total (product_id, product_name, price, quantity_sold)
        SELECT 
            product_id, 
            product_name, 
            price, 
            SUM(quantity_sold)
        FROM (
            SELECT * FROM jan
            UNION ALL
            SELECT * FROM feb
            UNION ALL
            SELECT * FROM mar
            UNION ALL
            SELECT * FROM may
            UNION ALL
            SELECT * FROM jun
            UNION ALL
            SELECT * FROM jul
            UNION ALL
            SELECT * FROM aug
            UNION ALL
            SELECT * FROM sep
            UNION ALL
            SELECT * FROM oct
            UNION ALL
            SELECT * FROM nov
            UNION ALL
            SELECT * FROM dec
        ) 
        GROUP BY product_id
        ON CONFLICT(product_id) DO UPDATE SET quantity_sold=excluded.quantity_sold;
        """)'''
    
    connection.commit()
    connection.close()
edit_database()