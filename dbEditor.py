import os
import sqlite3
import uuid
import bcrypt
import random
from datetime import date, datetime, timedelta

def edit_database():
    # Connect to the database
    conn = sqlite3.connect(os.path.join("db", "wastage_db.db"))
    cursor = conn.cursor()

    cursor.execute("DROP TABLE wastage_record")
    # # Step 1: Connect to databases
    # inv_conn = sqlite3.connect('db/inventory_db.db')
    # batch_conn = sqlite3.connect('db/batches_db.db')
    # inv_cursor = inv_conn.cursor()
    # batch_cursor = batch_conn.cursor()

    # inv_cursor.execute("""
    #     SELECT inv_id, quantity, unit, exp_date, rec_date
    #     FROM inv_dynamic
    #     ORDER BY rec_date ASC
    # """)
    # rows = inv_cursor.fetchall()

    # # Step 3: Group into 10 batches
    # total = len(rows)
    # batch_size = total // 10 + (total % 10 > 0)  # Evenly distribute with ceiling

    # batches = [rows[i:i + batch_size] for i in range(0, total, batch_size)]

    # # Step 4: Insert each group into Ba00001 to Ba00010
    # for i, batch_data in enumerate(batches):
    #     table_name = f"Ba{str(i+1).zfill(5)}"
    #     for row in batch_data:
    #         inv_id, quantity, unit, exp_date, rec_date = row

    #         # Get inv_desc from inv_static
    #         inv_cursor.execute("SELECT inv_desc FROM inv_static WHERE inv_id = ?", (inv_id,))
    #         result = inv_cursor.fetchone()
    #         inv_desc = result[0] if result else "Unknown"

    #         # Insert into batch table
    #         batch_cursor.execute(f"""
    #             INSERT OR IGNORE INTO {table_name} (inv_id, inv_desc, quantity, unit, exp_date, rec_date)
    #             VALUES (?, ?, ?, ?, ?, ?)
    #         """, (inv_id, inv_desc, quantity, unit, exp_date, rec_date))

    # # Step 5: Commit and close connections
    # batch_conn.commit()
    # inv_conn.close()
    # batch_conn.close()

    # print("Transfer to batch tables completed.")
    
    # Add BLOB in inv_static
    
    # Yearly
    # months = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    # years = ("2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025")

    # yearly_db_path = os.path.join('db/salesdb', 'sales_yearly.db')
    # yearly_conn = sqlite3.connect(yearly_db_path)
    # yearly_cursor = yearly_conn.cursor()

    # for year in years:
    #     print(f"\nProcessing year: {year}")
    #     year_table = f"sales_y{year}"

    #     # Ensure the table exists
    #     yearly_cursor.execute(f"""
    #         CREATE TABLE IF NOT EXISTS {year_table} (
    #             inv_id TEXT PRIMARY KEY,
    #             inv_desc TEXT,
    #             quantity_sold INTEGER,
    #             price REAL,
    #             sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #         )
    #     """)
    #     # Optional: Clear old data
    #     yearly_cursor.execute(f"DELETE FROM {year_table}")

    #     sales_aggregate = {}

    #     # Open the monthly database
    #     monthly_db_path = os.path.join('db/salesdb/monthly', f'sales_m{year}.db')
    #     if not os.path.exists(monthly_db_path):
    #         print(f"Monthly DB not found: {monthly_db_path}")
    #         continue

    #     monthly_conn = sqlite3.connect(monthly_db_path)
    #     monthly_cursor = monthly_conn.cursor()

    #     for month in months:
    #         try:
    #             monthly_cursor.execute(f"SELECT inv_id, inv_desc, quantity_sold, price FROM {month}")
    #             rows = monthly_cursor.fetchall()
    #         except Exception as e:
    #             print(f"Skipping {month} in {year}: {e}")
    #             continue

    #         for inv_id, inv_desc, qty_sold, price in rows:
    #             if inv_id not in sales_aggregate:
    #                 sales_aggregate[inv_id] = [inv_desc, qty_sold, price]
    #             else:
    #                 sales_aggregate[inv_id][1] += qty_sold  # accumulate quantity

    #     monthly_conn.close()

    #     data_to_insert = [
    #         (inv_id, desc, qty, price)
    #         for inv_id, (desc, qty, price) in sales_aggregate.items()
    #     ]

    #     yearly_cursor.executemany(f"""
    #         INSERT INTO {year_table} (inv_id, inv_desc, quantity_sold, price)
    #         VALUES (?, ?, ?, ?)
    #     """, data_to_insert)

    #     yearly_conn.commit()
    #     print(f"✓ Yearly data inserted for {year}")

    # yearly_conn.close()
    # print("\nAll yearly summaries complete.")
    
    # connectionPath = os.path.join("db", "inventory_db.db")
    # connection = sqlite3.connect(connectionPath)
    # cursor = connection.cursor()

    # wholeYear = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    # years = ("2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023")
    
    # for year in years:
    #     year_dir = f"db/salesdb/daily/sales_d{year}"
    #     os.makedirs(year_dir, exist_ok=True)
    #     for month in wholeYear:
    #         toPath = os.path.join(f"{year_dir}",f"{month}_{year}.db")
    #         toConn = sqlite3.connect(toPath)
    #         toCursor = toConn.cursor()
    #         if month == "feb":
    #             # Create tables 1-9
    #             for x in range(1,10):
    #                 toCursor.execute(f"""
    #                     CREATE TABLE IF NOT EXISTS d0{x} (
    #                         inv_id TEXT PRIMARY KEY,
    #                         inv_desc TEXT,
    #                         quantity_sold INTEGER,
    #                         price REAL,
    #                         sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #                     )
    #                 """
    #                 )
    #             # Create tables 10 - 29
    #             for x in range(10,30):
    #                 toCursor.execute(f"""
    #                     CREATE TABLE IF NOT EXISTS d{x} (
    #                         inv_id TEXT PRIMARY KEY,
    #                         inv_desc TEXT,
    #                         quantity_sold INTEGER,
    #                         price REAL,
    #                         sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #                     )
    #                 """
    #                 )
                    
    #             # Insert Mock Data
    #             cursor.execute("""
    #                 SELECT inv_id, inv_desc, cat, sub_cat, unit, rop, barcode, price, cost 
    #                 FROM inv_static
    #             """)
    #             invStatic = cursor.fetchall()
    #             numSales = 25
    #             # 1-95
    #             for x in range(1,10):
    #                 sampled_items = random.sample(invStatic, numSales)
    #                 data_to_insert = []
    #                 for item in sampled_items:
    #                     inv_id = item[0]
    #                     inv_desc = item[1]
    #                     price = item[7]
    #                     quantity_sold = random.randint(1, 13)
    #                     data_to_insert.append((inv_id, inv_desc, quantity_sold, price))
    #                 toCursor.executemany(f"""
    #                     INSERT OR IGNORE INTO d0{x} (inv_id, inv_desc, quantity_sold, price)
    #                     VALUES (?, ?, ?, ?)
    #                     """, data_to_insert)
                    
    #             # 10 and above  
    #             for x in range(10,30):
    #                 sampled_items = random.sample(invStatic, numSales)
    #                 data_to_insert = []
    #                 for item in sampled_items:
    #                     inv_id = item[0]
    #                     inv_desc = item[1]
    #                     price = item[7]
    #                     quantity_sold = random.randint(1, 13)
    #                     data_to_insert.append((inv_id, inv_desc, quantity_sold, price))
    #                 toCursor.executemany(f"""
    #                     INSERT OR IGNORE INTO d{x} (inv_id, inv_desc, quantity_sold, price)
    #                     VALUES (?, ?, ?, ?)
    #                     """, data_to_insert)
            
    #         # For 31-day Months
    #         elif month == "jan" or month == "mar" or month == "may" or month == "jul" or month == "aug" or month == "oct" or month == "dec":
    #             # Create tables 1-9
    #             for x in range(1,10):
    #                 toCursor.execute(f"""
    #                     CREATE TABLE IF NOT EXISTS d0{x} (
    #                         inv_id TEXT PRIMARY KEY,
    #                         inv_desc TEXT,
    #                         quantity_sold INTEGER,
    #                         price REAL,
    #                         sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #                     )
    #                 """
    #                 )
    #             # Create tables 10 ~ 31
    #             for x in range(10,32):
    #                 toCursor.execute(f"""
    #                     CREATE TABLE IF NOT EXISTS d{x} (
    #                         inv_id TEXT PRIMARY KEY,
    #                         inv_desc TEXT,
    #                         quantity_sold INTEGER,
    #                         price REAL,
    #                         sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #                     )
    #                 """
    #                 )
                    
    #             # Insert Mock Data
                
    #             cursor.execute("""
    #                 SELECT inv_id, inv_desc, cat, sub_cat, unit, rop, barcode, price, cost 
    #                 FROM inv_static
    #             """)
    #             invStatic = cursor.fetchall()
    #             numSales = 25
                
    #             # 1-9
    #             for x in range(1,10):
    #                 sampled_items = random.sample(invStatic, numSales)
    #                 data_to_insert = []
    #                 for item in sampled_items:
    #                     inv_id = item[0]
    #                     inv_desc = item[1]
    #                     price = item[7]
    #                     quantity_sold = random.randint(1, 13)
    #                     data_to_insert.append((inv_id, inv_desc, quantity_sold, price))
    #                 toCursor.executemany(f"""
    #                     INSERT OR IGNORE INTO d0{x} (inv_id, inv_desc, quantity_sold, price)
    #                     VALUES (?, ?, ?, ?)
    #                     """, data_to_insert)
                    
    #             # 10 and above  
    #             for x in range(10,32):
    #                 sampled_items = random.sample(invStatic, numSales)
    #                 data_to_insert = []
    #                 for item in sampled_items:
    #                     inv_id = item[0]
    #                     inv_desc = item[1]
    #                     price = item[7]
    #                     quantity_sold = random.randint(1, 13)
    #                     data_to_insert.append((inv_id, inv_desc, quantity_sold, price))
    #                 toCursor.executemany(f"""
    #                     INSERT OR IGNORE INTO d{x} (inv_id, inv_desc, quantity_sold, price)
    #                     VALUES (?, ?, ?, ?)
    #                     """, data_to_insert)
    #         # For 30-day Months
    #         elif month == "apr" or month == "jun" or month == "sep" or month == "nov":
    #             # Create tables 1-9
    #             for x in range(1,10):
    #                 toCursor.execute(f"""
    #                     CREATE TABLE IF NOT EXISTS d0{x} (
    #                         inv_id TEXT PRIMARY KEY,
    #                         inv_desc TEXT,
    #                         quantity_sold INTEGER,
    #                         price REAL,
    #                         sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #                     )
    #                 """
    #                 )
    #             # Create tables 10 - 30
    #             for x in range(10,31):
    #                 toCursor.execute(f"""
    #                     CREATE TABLE IF NOT EXISTS d{x} (
    #                         inv_id TEXT PRIMARY KEY,
    #                         inv_desc TEXT,
    #                         quantity_sold INTEGER,
    #                         price REAL,
    #                         sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
    #                     )
    #                 """
    #                 )
                    
    #             cursor.execute("""
    #                 SELECT inv_id, inv_desc, cat, sub_cat, unit, rop, barcode, price, cost 
    #                 FROM inv_static
    #             """)
    #             invStatic = cursor.fetchall()
    #             numSales = 25
                    
    #             # Insert Mock Data
    #             # 1-9
    #             for x in range(1,10):
    #                 sampled_items = random.sample(invStatic, numSales)
    #                 data_to_insert = []
    #                 for item in sampled_items:
    #                     inv_id = item[0]
    #                     inv_desc = item[1]
    #                     price = item[7]
    #                     quantity_sold = random.randint(1, 13)
    #                     data_to_insert.append((inv_id, inv_desc, quantity_sold, price))
    #                 toCursor.executemany(f"""
    #                     INSERT OR IGNORE INTO d0{x} (inv_id, inv_desc, quantity_sold, price)
    #                     VALUES (?, ?, ?, ?)
    #                     """, data_to_insert)
                    
    #             # 10 and above  
    #             for x in range(10,31):
    #                 sampled_items = random.sample(invStatic, numSales)
    #                 data_to_insert = []
    #                 for item in sampled_items:
    #                     inv_id = item[0]
    #                     inv_desc = item[1]
    #                     price = item[7]
    #                     quantity_sold = random.randint(1, 13)
    #                     data_to_insert.append((inv_id, inv_desc, quantity_sold, price))
    #                 toCursor.executemany(f"""
    #                     INSERT OR IGNORE INTO d{x} (inv_id, inv_desc, quantity_sold, price)
    #                     VALUES (?, ?, ?, ?)
    #                     """, data_to_insert)

    #         toConn.commit()
    #         toConn.close()
    
    # ADD COLUMN
    # cursor.execute("ALTER TABLE inv_static ADD COLUMN cost REAL")
    
    # EDIT ENTRY
    # cursor.execute("UPDATE inv_static SET cost = ? WHERE inv_id = ?;",(expense_data[x-1],f"INVa0000{x}"))
    
    # DELETE ENTRY
    # cursor.execute("DELETE FROM inv_dynamic WHERE actual_id = 'ITa00001'")
    # cursor.execute("DELETE FROM inv_dynamic WHERE actual_id = 'ITa00002'")
    # cursor.execute("DELETE FROM inv_dynamic WHERE actual_id = 'ITa00003'")
    # cursor.execute("DELETE FROM inv_dynamic WHERE actual_id = 'ITa00004'")

    # DELETE COLUMN
    # cursor.execute("ALTER TABLE ingredients DROP COLUMN 'C011'")

    # DELETE TABLE
    # cursor.execute("DROP TABLE IF EXISTS Ba00000")
    # for i in range(6, 10): 
    #     table_name = f"d{i}"
    #     cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # EDIT TABLE NAME
    # cursor.execute("ALTER TABLE BATCHA00001 RENAME TO Ba00001")
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
    
    # wastage
    # data_wastage=[
    #     ("INVa00031","Marby Tasty Bread","7","pack","Expired","2025-06-13"),
    #     ("INVa00048","Chippy BBQ 110 g","5","pack","Deflated, compromised packaging","2025-06-13"),
    #     ("INVa00006","Coca Cola Coke 1.5 L","2","bottle","Leaking bottle","2025-06-13"),
    #     ("INVa00001", "Bimoli Cooking Oil 500 ml", "3", "pack", "Broken seal", "2025-06-12"),
    #     ("INVa00008", "Oreo Cookies 45 g", "4", "pack", "Expired", "2025-06-10"),
    #     ("INVa00030", "Gardenia Classic Bread Loaf", "6", "pack", "Mold growth", "2025-06-09"),
    #     ("INVa00024", "Safeguard Body Wash 400 ml", "2", "bottle", "Cracked bottle", "2025-06-07"),
    #     ("INVa00034", "Nagaraya Garlic Cracker Nuts 160 g", "3", "pack", "Stale product", "2025-06-06"),
    #     ("INVa00044", "Lucky Me! Beef Mami 55 g", "8", "pack", "Improper storage", "2025-06-05"),
    #     ("INVa00005", "Bounty Fresh Eggs L", "12", "piece", "Spoiled", "2025-06-04"),
    #     ("INVa00012", "555 Sardines in Tomato Sauce 155 g", "5", "can", "Rusty can", "2025-06-03"),
    #     ("INVa00038", "Nestlé All Purpose Cream 250 ml", "2", "pack", "Expired", "2025-06-02"),
    #     ("INVa00015", "Bear Brand Powdered Milk 320 g", "1", "pack", "Torn packaging", "2025-06-01"),
    #     ("INVa00027", "Mr. Muscle Glass Cleaner 500 ml", "1", "bottle", "Cracked bottle", "2025-05-31"),
    #     ("INVa00042", "Datu Puti Vinegar 1 L", "2", "bottle", "Leaking cap", "2025-05-30"),
    #     ("INVa00047", "Yakult Probiotic Drink 80 ml", "6", "bottle", "Spoiled due to no refrigeration", "2025-05-28"),
    #     ("INVa00045", "Quickchow Chicken 50 g", "7", "pack", "Expired", "2025-05-26"),
    #     ("INVa00011", "Argentina Corned Beef 150 g", "2", "can", "Dented and bloated", "2025-05-25")
    # ]
    # cursor.executemany("""
    # INSERT OR IGNORE INTO wastage_record (inv_id, inv_desc, quantity, unit, remark, dec_date)
    # VALUES (?, ?, ?, ?, ?, ?)
    # """, data_wastage)
    
    # data__inv_dynamic = [
    #     ("ITa00001", "Ba00001", "INVa00001", 17, "pack", "2025-09-18", "2025-06-01"),
    #     ("ITa00002", "Ba00001", "INVa00005", 24, "piece", "2025-12-11", "2025-06-01"),
    #     ("ITa00003", "Ba00001", "INVa00006", 30, "bottle", "2025-09-01", "2025-06-01"),
    #     ("ITa00004", "Ba00001", "INVa00011", 45, "can", "2025-08-20", "2025-06-01"),
    #     ("ITa00005", "Ba00001", "INVa00017", 22, "jar", "2025-10-14", "2025-06-01"),
    #     ("ITa00006", "Ba00001", "INVa00018", 35, "tetra", "2026-01-01", "2025-06-01"),
    #     ("ITa00007", "Ba00001", "INVa00024", 10, "bottle", "2025-12-31", "2025-06-01"),
    #     ("ITa00008", "Ba00001", "INVa00028", 27, "bottle", "2025-08-15", "2025-06-01"),

    #     ("ITa00009", "Ba00002", "INVa00002", 19, "pack", "2025-10-10", "2025-06-02"),
    #     ("ITa00010", "Ba00002", "INVa00012", 12, "can", "2025-09-25", "2025-06-02"),
    #     ("ITa00011", "Ba00002", "INVa00019", 38, "sachet", "2025-10-01", "2025-06-02"),
    #     ("ITa00012", "Ba00002", "INVa00020", 25, "bar", "2025-11-03", "2025-06-02"),
    #     ("ITa00013", "Ba00002", "INVa00021", 14, "bottle", "2025-07-15", "2025-06-02"),
    #     ("ITa00014", "Ba00002", "INVa00026", 40, "bottle", "2025-08-01", "2025-06-02"),
    #     ("ITa00015", "Ba00002", "INVa00033", 11, "bottle", "2025-10-30", "2025-06-02"),
    #     ("ITa00016", "Ba00002", "INVa00042", 17, "bottle", "2025-12-05", "2025-06-02"),

    #     ("ITa00017", "Ba00003", "INVa00003", 21, "pack", "2025-07-01", "2025-06-03"),
    #     ("ITa00018", "Ba00003", "INVa00007", 23, "pack", "2025-09-17", "2025-06-03"),
    #     ("ITa00019", "Ba00003", "INVa00008", 19, "pack", "2025-11-01", "2025-06-03"),
    #     ("ITa00020", "Ba00003", "INVa00010", 15, "pack", "2025-09-22", "2025-06-03"),
    #     ("ITa00021", "Ba00003", "INVa00022", 26, "tube", "2025-10-10", "2025-06-03"),
    #     ("ITa00022", "Ba00003", "INVa00029", 33, "piece", "2025-08-19", "2025-06-03"),
    #     ("ITa00023", "Ba00003", "INVa00035", 12, "piece", "2025-09-05", "2025-06-03"),
    #     ("ITa00024", "Ba00003", "INVa00037", 28, "tub", "2025-11-17", "2025-06-03"),

    #     ("ITa00025", "Ba00004", "INVa00004", 17, "pack", "2025-09-19", "2025-06-04"),
    #     ("ITa00026", "Ba00004", "INVa00009", 14, "pack", "2025-10-12", "2025-06-04"),
    #     ("ITa00027", "Ba00004", "INVa00013", 18, "pack", "2025-07-07", "2025-06-04"),
    #     ("ITa00028", "Ba00004", "INVa00014", 26, "pack", "2025-11-23", "2025-06-04"),
    #     ("ITa00029", "Ba00004", "INVa00015", 19, "pack", "2025-08-11", "2025-06-04"),
    #     ("ITa00030", "Ba00004", "INVa00016", 16, "pack", "2025-07-29", "2025-06-04"),
    #     ("ITa00031", "Ba00004", "INVa00025", 13, "pack", "2025-10-21", "2025-06-04"),
    #     ("ITa00032", "Ba00004", "INVa00046", 29, "can", "2025-09-30", "2025-06-04"),

    #     ("ITa00033", "Ba00005", "INVa00030", 22, "pack", "2025-08-18", "2025-06-05"),
    #     ("ITa00034", "Ba00005", "INVa00031", 35, "pack", "2025-12-01", "2025-06-05"),
    #     ("ITa00035", "Ba00005", "INVa00032", 14, "pack", "2025-11-11", "2025-06-05"),
    #     ("ITa00036", "Ba00005", "INVa00034", 18, "pack", "2025-10-28", "2025-06-05"),
    #     ("ITa00037", "Ba00005", "INVa00036", 30, "bottle", "2025-07-18", "2025-06-05"),
    #     ("ITa00038", "Ba00005", "INVa00038", 20, "pack", "2025-09-12", "2025-06-05"),
    #     ("ITa00039", "Ba00005", "INVa00039", 10, "pack", "2025-08-02", "2025-06-05"),
    #     ("ITa00040", "Ba00005", "INVa00040", 26, "pack", "2025-12-10", "2025-06-05"),
        
    #     ("ITa00041", "Ba00006", "INVa00041", 15, "pack", "2025-10-20", "2025-06-06"),
    #     ("ITa00042", "Ba00006", "INVa00043", 26, "pack", "2025-12-18", "2025-06-06"),
    #     ("ITa00043", "Ba00006", "INVa00044", 32, "pack", "2025-11-05", "2025-06-06"),
    #     ("ITa00044", "Ba00006", "INVa00045", 28, "pack", "2025-09-30", "2025-06-06"),
    #     ("ITa00045", "Ba00006", "INVa00047", 18, "bottle", "2025-08-28", "2025-06-06"),
    #     ("ITa00046", "Ba00006", "INVa00048", 13, "pack", "2025-11-10", "2025-06-06"),
    #     ("ITa00047", "Ba00006", "INVa00049", 30, "can", "2025-10-14", "2025-06-06"),
    #     ("ITa00048", "Ba00006", "INVa00050", 24, "pack", "2025-12-01", "2025-06-06"),

    #     ("ITa00049", "Ba00007", "INVa00001", 20, "pack", "2025-11-15", "2025-06-07"),
    #     ("ITa00050", "Ba00007", "INVa00003", 16, "pack", "2025-08-27", "2025-06-07"),
    #     ("ITa00051", "Ba00007", "INVa00005", 28, "piece", "2025-09-10", "2025-06-07"),
    #     ("ITa00052", "Ba00007", "INVa00007", 21, "pack", "2025-10-02", "2025-06-07"),
    #     ("ITa00053", "Ba00007", "INVa00010", 12, "pack", "2025-11-30", "2025-06-07"),
    #     ("ITa00054", "Ba00007", "INVa00013", 30, "pack", "2025-09-04", "2025-06-07"),
    #     ("ITa00055", "Ba00007", "INVa00016", 22, "pack", "2025-10-18", "2025-06-07"),
    #     ("ITa00056", "Ba00007", "INVa00019", 15, "sachet", "2025-08-09", "2025-06-07"),

    #     ("ITa00057", "Ba00008", "INVa00002", 19, "pack", "2025-08-11", "2025-06-08"),
    #     ("ITa00058", "Ba00008", "INVa00004", 17, "pack", "2025-10-01", "2025-06-08"),
    #     ("ITa00059", "Ba00008", "INVa00006", 24, "bottle", "2025-11-12", "2025-06-08"),
    #     ("ITa00060", "Ba00008", "INVa00008", 34, "pack", "2025-12-19", "2025-06-08"),
    #     ("ITa00061", "Ba00008", "INVa00011", 23, "can", "2025-09-08", "2025-06-08"),
    #     ("ITa00062", "Ba00008", "INVa00014", 29, "pack", "2025-08-25", "2025-06-08"),
    #     ("ITa00063", "Ba00008", "INVa00018", 20, "tetra", "2025-11-07", "2025-06-08"),
    #     ("ITa00064", "Ba00008", "INVa00020", 26, "bar", "2025-09-19", "2025-06-08"),

    #     ("ITa00065", "Ba00009", "INVa00009", 13, "pack", "2025-08-13", "2025-06-09"),
    #     ("ITa00066", "Ba00009", "INVa00012", 22, "can", "2025-11-14", "2025-06-09"),
    #     ("ITa00067", "Ba00009", "INVa00015", 35, "pack", "2025-10-23", "2025-06-09"),
    #     ("ITa00068", "Ba00009", "INVa00017", 18, "jar", "2025-09-06", "2025-06-09"),
    #     ("ITa00069", "Ba00009", "INVa00021", 27, "bottle", "2025-12-09", "2025-06-09"),
    #     ("ITa00070", "Ba00009", "INVa00022", 31, "tube", "2025-08-19", "2025-06-09"),
    #     ("ITa00071", "Ba00009", "INVa00023", 16, "pack", "2025-09-26", "2025-06-09"),
    #     ("ITa00072", "Ba00009", "INVa00025", 29, "pack", "2025-10-30", "2025-06-09"),

    #     ("ITa00073", "Ba00010", "INVa00027", 23, "bottle", "2025-11-01", "2025-06-10"),
    #     ("ITa00074", "Ba00010", "INVa00030", 19, "pack", "2025-12-11", "2025-06-10"),
    #     ("ITa00075", "Ba00010", "INVa00032", 21, "pack", "2025-09-02", "2025-06-10"),
    #     ("ITa00076", "Ba00010", "INVa00034", 25, "pack", "2025-10-12", "2025-06-10"),
    #     ("ITa00077", "Ba00010", "INVa00036", 14, "bottle", "2025-08-20", "2025-06-10"),
    #     ("ITa00078", "Ba00010", "INVa00038", 30, "pack", "2025-09-30", "2025-06-10"),
    #     ("ITa00079", "Ba00010", "INVa00039", 28, "pack", "2025-07-28", "2025-06-10"),
    #     ("ITa00080", "Ba00010", "INVa00044", 22, "pack", "2025-12-22", "2025-06-10")
    # ]
    
    # cursor.executemany("""
    # INSERT OR IGNORE INTO inv_dynamic (actual_id, batch_id, inv_id, quantity, unit, exp_date, rec_date)
    # VALUES (?, ?, ?, ?, ?, ?, ?)
    # """, data__inv_dynamic)
    
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
    #     CREATE TABLE IF NOT EXISTS Ba00010 (
    #         inv_id TEXT PRIMARY KEY,
    #         inv_desc TEXT,
    #         quantity INTEGER,
    #         unit TEXT,
    #         exp_date DATE,
    #         rec_date DATE
    #     )
    #     """)
    
    # for x in range(9):
    #     cursor.execute(f"""
    #     CREATE TABLE IF NOT EXISTS Ba0000{x} (
    #         inv_id TEXT PRIMARY KEY,
    #         inv_desc TEXT,
    #         quantity INTEGER,
    #         unit TEXT,
    #         exp_date DATE,
    #         rec_date DATE
    #     )
    #     """)
    
    # ADD DATA
    # data = [
    #     ("INVa00001", "Bimoli Cooking Oil 500 ml", "Cooking", "Cooking Oil", "pack", 30),
    #     ("INVa00002", "Silver Swan Soy Souce 500 ml","Cooking", "Soy Sauce", "pack", 30),
    #     ("INVa00003", "Lucky Me! Pancit Canton Chili Mansi 50 g", "Easy Prep", "Instant Noodles", "pack", 30),
    #     ("INVa00004", "Lucky Me! Pancit Canton Extra Hot 50 g", "Easy Prep", "Instant Noodles", "pack", 30),
    #     ("INVa00005", "Bounty Fresh Eggs L", "Eggs & Dairy", "Egg", "piece", 36),
    #     ("INVa00006", "Coca Cola Coke 1.5 L", "Beverages", "Soft Drinks", "bottle", 20),
    #     ("INVa00007", "Rebisco Crackers 30 g", "Snacks", "Instant Noodles", "pack", 50),
    #     ("INVa00008", "Oreo Cookies 45 g", "Snacks", "Biscuits", "pack", 50),
    #     ("INVa00009", "Piattos Sour Cream Onion 90g", "Snacks", "Chips", "pack", 30),
    #     ("INVa00010", "Surf Powder Lavender 150 g", "Cleaning", "Laundry", "pack", 15),
    #     ("INVa00011", "Argentina Corned Beef 150 g", "Cooking", "Canned Goods", "can", 20),
    #     ("INVa00012", "555 Sardines in Tomato Sauce 155 g", "Cooking", "Canned Goods", "can", 20),
    #     ("INVa00013", "Purefoods Hotdog Regular 1 kg", "Easy Prep", "Frozen Goods", "pack", 10),
    #     ("INVa00014", "Magnolia Cheezee 165 g", "Eggs & Dairy", "Cheese", "pack", 10),
    #     ("INVa00015", "Bear Brand Powdered Milk 320 g", "Eggs & Dairy", "Milk", "pack", 15),
    #     ("INVa00016", "Milo Chocolate Drink 220 g", "Beverages", "Powdered Drinks", "pack", 10),
    #     ("INVa00017", "Nescafe Classic 100 g", "Beverages", "Coffee", "jar", 8),
    #     ("INVa00018", "Zesto Orange Juice 250 ml", "Beverages", "Juice", "tetra", 40),
    #     ("INVa00019", "Tang Pineapple Powder Drink 25 g", "Beverages", "Powdered Drinks", "sachet", 50),
    #     ("INVa00020", "Lifebuoy Antibacterial Soap 90 g", "Personal Care", "Soap", "bar", 30),
    #     ("INVa00021", "Head & Shoulders Shampoo 170 ml", "Personal Care", "Shampoo", "bottle", 15),
    #     ("INVa00022", "Colgate Toothpaste 150 ml", "Personal Care", "Toothpaste", "tube", 25),
    #     ("INVa00023", "Modess Regular Pads 8s", "Personal Care", "Sanitary", "pack", 20),
    #     ("INVa00024", "Safeguard Body Wash 400 ml", "Personal Care", "Soap", "bottle", 10),
    #     ("INVa00025", "Tide Powder Detergent 500 g", "Cleaning", "Laundry", "pack", 20),
    #     ("INVa00026", "Domex Toilet Cleaner 500 ml", "Cleaning", "Bathroom", "bottle", 10),
    #     ("INVa00027", "Mr. Muscle Glass Cleaner 500 ml", "Cleaning", "Surface Cleaner", "bottle", 12),
    #     ("INVa00028", "Joy Dishwashing Liquid 495 ml", "Cleaning", "Kitchen", "bottle", 15),
    #     ("INVa00029", "Scotch Brite Sponge", "Cleaning", "Kitchen", "piece", 20),
    #     ("INVa00030", "Gardenia Classic Bread Loaf", "Bakery", "Bread", "pack", 25),
    #     ("INVa00031", "Marby Tasty Bread", "Bakery", "Bread", "pack", 25),
    #     ("INVa00032", "Fita Biscuits 33 g", "Snacks", "Biscuits", "pack", 40),
    #     ("INVa00033", "Nova Multigrain Snacks 78 g", "Snacks", "Chips", "pack", 30),
    #     ("INVa00034", "Nagaraya Garlic Cracker Nuts 160 g", "Snacks", "Nuts", "pack", 20),
    #     ("INVa00035", "Cloud 9 Classic Chocolate Bar", "Snacks", "Chocolates", "piece", 35),
    #     ("INVa00036", "C2 Apple 500 ml", "Beverages", "Tea Drinks", "bottle", 30),
    #     ("INVa00037", "Selecta Super Thick Vanilla 1.5L", "Easy Prep", "Frozen Goods", "tub", 8),
    #     ("INVa00038", "Nestlé All Purpose Cream 250 ml", "Cooking", "Baking", "pack", 20),
    #     ("INVa00039", "Maya All Purpose Flour 1 kg", "Cooking", "Baking", "pack", 10),
    #     ("INVa00040", "Brown Sugar 1 kg", "Cooking", "Baking", "pack", 15),
    #     ("INVa00041", "Ajinomoto Vetsin 250 g", "Cooking", "Seasoning", "pack", 25),
    #     ("INVa00042", "Datu Puti Vinegar 1 L", "Cooking", "Condiments", "bottle", 25),
    #     ("INVa00043", "Datu Puti Soy Sauce 1 L", "Cooking", "Condiments", "bottle", 25),
    #     ("INVa00044", "Lucky Me! Beef Mami 55 g", "Easy Prep", "Instant Noodles", "pack", 40),
    #     ("INVa00045", "Quickchow Chicken 50 g", "Easy Prep", "Instant Noodles", "pack", 40),
    #     ("INVa00046", "Alaska Evaporated Milk 370 ml", "Eggs & Dairy", "Milk", "can", 25),
    #     ("INVa00047", "Yakult Probiotic Drink 80 ml", "Beverages", "Probiotic", "bottle", 50),
    #     ("INVa00048", "Chippy BBQ 110 g", "Snacks", "Chips", "pack", 30),
    #     ("INVa00049", "Ligo Sardines Green 155 g", "Cooking", "Canned Goods", "can", 20),
    #     ("INVa00050", "Energizer AA Battery 2s", "Personal Care", "Essentials", "pack", 10)
    # ]
    
    # ADD TO TABLE
    # cursor.executemany("""
    # INSERT OR IGNORE INTO inv_static (inv_id, inv_desc, cat, sub_cat, unit, rop)
    # VALUES (?, ?, ?, ?, ?, ?)
    # """, data)
    
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
    
    # connection.commit()
    # connection.close()
edit_database()