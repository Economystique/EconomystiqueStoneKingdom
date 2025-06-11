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
    # for i in range(6, 10): 
    #     table_name = f"d{i}"
    #     cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # EDIT TABLE NAME
    #cursor.execute("ALTER TABLE this_month RENAME TO apr")
    # for i in range(1, 10):  # d1 to d9
    #     old_name = f"d{i}"
    #     new_name = f"d{str(i).zfill(2)}"  # zero-pads single digits to 2 digits
    #     cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")

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
    data = [
        ("INVa00001", "Bimoli Cooking Oil 500 ml", "Cooking", "Cooking Oil", "pack", 30),
        ("INVa00002", "Silver Swan Soy Souce 500 ml","Cooking", "Soy Sauce", "pack", 30),
        ("INVa00003", "Lucky Me! Pancit Canton Chili Mansi 50 g", "Easy Prep", "Instant Noodles", "pack", 30),
        ("INVa00004", "Lucky Me! Pancit Canton Extra Hot 50 g", "Easy Prep", "Instant Noodles", "pack", 30),
        ("INVa00005", "Bounty Fresh Eggs L", "Eggs & Dairy", "Egg", "piece", 36),
        ("INVa00006", "Coca Cola Coke 1.5 L", "Beverages", "Soft Drinks", "bottle", 20),
        ("INVa00007", "Rebisco Crackers 30 g", "Snacks", "Instant Noodles", "pack", 50),
        ("INVa00008", "Oreo Cookies 45 g", "Snacks", "Biscuits", "pack", 50),
        ("INVa00009", "Piattos Sour Cream Onion 90g", "Snacks", "Chips", "pack", 30),
        ("INVa00010", "Surf Powder Lavender 150 g", "Cleaning", "Laundry", "pack", 15),
        ("INVa00011", "Argentina Corned Beef 150 g", "Cooking", "Canned Goods", "can", 20),
        ("INVa00012", "555 Sardines in Tomato Sauce 155 g", "Cooking", "Canned Goods", "can", 20),
        ("INVa00013", "Purefoods Hotdog Regular 1 kg", "Easy Prep", "Frozen Goods", "pack", 10),
        ("INVa00014", "Magnolia Cheezee 165 g", "Eggs & Dairy", "Cheese", "pack", 10),
        ("INVa00015", "Bear Brand Powdered Milk 320 g", "Eggs & Dairy", "Milk", "pack", 15),
        ("INVa00016", "Milo Chocolate Drink 220 g", "Beverages", "Powdered Drinks", "pack", 10),
        ("INVa00017", "Nescafe Classic 100 g", "Beverages", "Coffee", "jar", 8),
        ("INVa00018", "Zesto Orange Juice 250 ml", "Beverages", "Juice", "tetra", 40),
        ("INVa00019", "Tang Pineapple Powder Drink 25 g", "Beverages", "Powdered Drinks", "sachet", 50),
        ("INVa00020", "Lifebuoy Antibacterial Soap 90 g", "Personal Care", "Soap", "bar", 30),
        ("INVa00021", "Head & Shoulders Shampoo 170 ml", "Personal Care", "Shampoo", "bottle", 15),
        ("INVa00022", "Colgate Toothpaste 150 ml", "Personal Care", "Toothpaste", "tube", 25),
        ("INVa00023", "Modess Regular Pads 8s", "Personal Care", "Sanitary", "pack", 20),
        ("INVa00024", "Safeguard Body Wash 400 ml", "Personal Care", "Soap", "bottle", 10),
        ("INVa00025", "Tide Powder Detergent 500 g", "Cleaning", "Laundry", "pack", 20),
        ("INVa00026", "Domex Toilet Cleaner 500 ml", "Cleaning", "Bathroom", "bottle", 10),
        ("INVa00027", "Mr. Muscle Glass Cleaner 500 ml", "Cleaning", "Surface Cleaner", "bottle", 12),
        ("INVa00028", "Joy Dishwashing Liquid 495 ml", "Cleaning", "Kitchen", "bottle", 15),
        ("INVa00029", "Scotch Brite Sponge", "Cleaning", "Kitchen", "piece", 20),
        ("INVa00030", "Gardenia Classic Bread Loaf", "Bakery", "Bread", "pack", 25),
        ("INVa00031", "Marby Tasty Bread", "Bakery", "Bread", "pack", 25),
        ("INVa00032", "Fita Biscuits 33 g", "Snacks", "Biscuits", "pack", 40),
        ("INVa00033", "Nova Multigrain Snacks 78 g", "Snacks", "Chips", "pack", 30),
        ("INVa00034", "Nagaraya Garlic Cracker Nuts 160 g", "Snacks", "Nuts", "pack", 20),
        ("INVa00035", "Cloud 9 Classic Chocolate Bar", "Snacks", "Chocolates", "piece", 35),
        ("INVa00036", "C2 Apple 500 ml", "Beverages", "Tea Drinks", "bottle", 30),
        ("INVa00037", "Selecta Super Thick Vanilla 1.5L", "Easy Prep", "Frozen Goods", "tub", 8),
        ("INVa00038", "Nestlé All Purpose Cream 250 ml", "Cooking", "Baking", "pack", 20),
        ("INVa00039", "Maya All Purpose Flour 1 kg", "Cooking", "Baking", "pack", 10),
        ("INVa00040", "Brown Sugar 1 kg", "Cooking", "Baking", "pack", 15),
        ("INVa00041", "Ajinomoto Vetsin 250 g", "Cooking", "Seasoning", "pack", 25),
        ("INVa00042", "Datu Puti Vinegar 1 L", "Cooking", "Condiments", "bottle", 25),
        ("INVa00043", "Datu Puti Soy Sauce 1 L", "Cooking", "Condiments", "bottle", 25),
        ("INVa00044", "Lucky Me! Beef Mami 55 g", "Easy Prep", "Instant Noodles", "pack", 40),
        ("INVa00045", "Quickchow Chicken 50 g", "Easy Prep", "Instant Noodles", "pack", 40),
        ("INVa00046", "Alaska Evaporated Milk 370 ml", "Eggs & Dairy", "Milk", "can", 25),
        ("INVa00047", "Yakult Probiotic Drink 80 ml", "Beverages", "Probiotic", "bottle", 50),
        ("INVa00048", "Chippy BBQ 110 g", "Snacks", "Chips", "pack", 30),
        ("INVa00049", "Ligo Sardines Green 155 g", "Cooking", "Canned Goods", "can", 20),
        ("INVa00050", "Energizer AA Battery 2s", "Personal Care", "Essentials", "pack", 10)
    ]
    
    # ADD TO TABLE
    cursor.executemany("""
    INSERT OR IGNORE INTO inv_static (inv_id, inv_desc, cat, sub_cat, unit, rop)
    VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    
    # UUID Generation
    # user_name = "admin"
    # uid1 =str(uuid.uuid5(uuid.NAMESPACE_DNS, user_name))
    
    # # PW Acquisition & Byte Conversion
    # pw = "admin123"
    # pw_byte = pw.encode('UTF-8')
    # salt = bcrypt.gensalt()
    # pw_hash = bcrypt.hashpw(pw_byte, salt).decode('utf-8')
    
    # data = [uid1,"admin","economystique@gmail.com",pw_hash,"2025-06-05"]
    
    

    # ADD BLOB IN COLUMN
    # product_id = "C010"
    # image_path = "img/C010.png"
    
    # def convert_to_binary(filename):
    #     with open(filename, 'rb') as file:
    #         return file.read()
    
    # try:
    #     image_data = convert_to_binary(image_path)
    #     cursor.execute("UPDATE products_on_hand SET image = ? WHERE product_id = ?", (image_data, product_id))
    #     connection.commit()
    #     print(f"Image added successfully to product_id: {product_id}")
    # except Exception as e:
    #     print(f"Failed to update image: {e}")
    # finally:
    #     connection.close()
    
    connection.commit()
    connection.close()
edit_database()