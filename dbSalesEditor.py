import os
import sqlite3
import uuid
import bcrypt
import random
import calendar

def edit_database():
    wholeYear = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    years = ("2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023","2024", "2025")

    for year in years:
        year_int = int(year)

        # Create/open the database for the whole year
        conn = sqlite3.connect(os.path.join('db/salesdb/monthly', f'sales_m{year}.db'))
        cursor = conn.cursor()

        for month_index, month in enumerate(wholeYear, start=1):
            db_path = os.path.join(f'db/salesdb/daily/sales_d{year}', f'{month}_{year}.db')
            if not os.path.exists(db_path):
                print(f"Skipping missing database: {db_path}")
                continue

            try:
                dConn = sqlite3.connect(db_path)
                dCursor = dConn.cursor()
            except:
                print(f"Error opening {db_path}")
                continue

            sales_aggregate = {}
            days_in_month = calendar.monthrange(year_int, month_index)[1]

            for day in range(1, days_in_month + 1):
                table_name = f"d0{day}" if day < 10 else f"d{day}"
                try:
                    dCursor.execute(f"""
                        SELECT inv_id, inv_desc, SUM(quantity_sold), price
                        FROM {table_name}
                        GROUP BY inv_id
                    """)
                    temp_rows = dCursor.fetchall()
                except Exception as e:
                    print(f"Error reading table {table_name} in {month}_{year}: {e}")
                    continue

                for inv_id, inv_desc, qty_sold, price in temp_rows:
                    if inv_id not in sales_aggregate:
                        sales_aggregate[inv_id] = [inv_desc, qty_sold, price]
                    else:
                        sales_aggregate[inv_id][1] += qty_sold

            dConn.close()

            # Insert into corresponding month table (e.g., jan, feb...)
            data_to_insert = [
                (inv_id, desc, qty, price)
                for inv_id, (desc, qty, price) in sales_aggregate.items()
            ]
            
            cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {month} (
                            inv_id TEXT PRIMARY KEY,
                            inv_desc TEXT,
                            quantity_sold INTEGER,
                            price REAL,
                            sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
                        )
                    """)
            # Optional: clear old data from the table
            cursor.execute(f"DELETE FROM {month}")
            
            cursor.executemany(f"""
                INSERT INTO {month} (inv_id, inv_desc, quantity_sold, price)
                VALUES (?, ?, ?, ?)
            """, data_to_insert)

            conn.commit()
            print(f"Inserted data for {month}_{year}")

        conn.close()
        print(f"Finished year {year}")  
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
                # inv_id TEXT PRIMARY KEY,
                # inv_desc TEXT,
                # quantity_sold INTEGER,
                # price REAL,
                # sales_total REAL GENERATED ALWAYS AS (quantity_sold * price) STORED
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
    #     ("INVa00001", "Bimoli Cooking Oil 500 ml", 2, 125),
    #     ("INVa00003", "Lucky Me! Pancit Canton Chili Mansi 50 g", 5, 15),
    #     ("INVa00005", "Bounty Fresh Eggs L", 6, 9),
    #     ("INVa00006", "Coca Cola Coke 1.5 L", 3, 60),
    #     ("INVa00008", "Oreo Cookies 45 g", 4, 18),
    #     ("INVa00009", "Piattos Sour Cream Onion 90g", 3, 25),
    #     ("INVa00011", "Argentina Corned Beef 150 g", 2, 45),
    #     ("INVa00013", "Purefoods Hotdog Regular 1 kg", 1, 170),
    #     ("INVa00015", "Bear Brand Powdered Milk 320 g", 2, 95),
    #     ("INVa00016", "Milo Chocolate Drink 220 g", 1, 80),
    #     ("INVa00018", "Zesto Orange Juice 250 ml", 6, 12),
    #     ("INVa00019", "Tang Pineapple Powder Drink 25 g", 5, 10),
    #     ("INVa00020", "Lifebuoy Antibacterial Soap 90 g", 3, 35),
    #     ("INVa00022", "Colgate Toothpaste 150 ml", 2, 50),
    #     ("INVa00025", "Tide Powder Detergent 500 g", 1, 65),
    #     ("INVa00028", "Joy Dishwashing Liquid 495 ml", 2, 70),
    #     ("INVa00030", "Gardenia Classic Bread Loaf", 3, 55),
    #     ("INVa00032", "Fita Biscuits 33 g", 4, 12),
    #     ("INVa00034", "Nagaraya Garlic Cracker Nuts 160 g", 2, 45),
    #     ("INVa00035", "Cloud 9 Classic Chocolate Bar", 5, 10),
    #     ("INVa00036", "C2 Apple 500 ml", 4, 28),
    #     ("INVa00037", "Selecta Super Thick Vanilla 1.5L", 1, 210),
    #     ("INVa00040", "Brown Sugar 1 kg", 2, 45),
    #     ("INVa00042", "Datu Puti Vinegar 1 L", 3, 22),
    #     ("INVa00047", "Yakult Probiotic Drink 80 ml", 6, 12)
    # ]
    
    # cursor.executemany("""
    #     INSERT OR IGNORE INTO sales_today (inv_id, inv_desc, quantity_sold, price)
    #     VALUES (?, ?, ?, ?)              
    # """, data_sales_now)
    
    # connection.commit()
    # connection.close()
edit_database()