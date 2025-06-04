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
    '''cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",("13-05-25","C004"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(760,"C002"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(820,"C003"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(750,"C004"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(850,"C005"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(760,"C006"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(780,"C007"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(900,"C008"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(370,"C009"))
    cursor.execute("UPDATE apr SET quantity_sold = ? WHERE product_id = ?;",(40,"C010"))'''

    # DELETE ENTRY
    #cursor.execute("DELETE FROM ingredients WHERE inventory_id = 'IN014'")
    
    # DELETE COLUMN
    #cursor.execute("ALTER TABLE ingredients DROP COLUMN 'C011'")
    
    # DELETE TABLE
    # cursor.execute(f"DROP TABLE IF EXISTS inv_static")
    
    # EDIT TABLE NAME
    #cursor.execute("ALTER TABLE this_month RENAME TO apr")
    
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
    
    # CREATE TABLE
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS inv_static (
    #     inv_id TEXT PRIMARY KEY,
    #     inv_desc TEXT,
    #     cat TEXT,
    #     sub_cat TEXT,
    #     unit TEXT,
    #     rop INTEGER
    # )
    # """)
  

    # ADD DATA
    data = [("Ba00001","INVa00005",36,"piece","2025-06-20","2025-06-04"),
            ("Ba00002","INVa00006",20,"bottle","2025-10-15","2025-06-04"),
            ("Ba00003","INVa00008",20,"pack","2025-12-10","2025-06-04"),
            ("Ba00004","INVa00010",15,"pack","2026-06-20","2025-06-04"),\
    ]
    
    # UUID Generation
    # uid1 =str(uuid.uuid4())
    
    # PW Acquisition & Byte Conversion
    # pw = "123"
    # pw_byte = pw.encode('UTF-8')
    # salt = bcrypt.gensalt()
    # pw_hash = bcrypt.hashpw(pw_byte, salt).decode('utf-8')
    
    # data = [uid1,"kate","katelascota@gmail.com",pw_hash]
    cursor.executemany("""
    INSERT OR IGNORE INTO inv_dynamic (batch_id, inv_id, quantity, unit, exp_date, rec_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, data)

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