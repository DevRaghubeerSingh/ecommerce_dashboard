import sqlite3 
import pandas as pd 
from datetime import datetime, timedelta 
import random

def create_database(): 
    conn = sqlite3.connect('ecommerce.db') 
    cursor = conn.cursor()

# Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            total_amount REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_details (
            detail_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT,
            country TEXT
        )
    ''')

    # Generate sample data
    start_date = datetime(2024, 1, 1)
    products = [
        (1, 'Laptop', 'Electronics'),
        (2, 'Smartphone', 'Electronics'),
        (3, 'T-Shirt', 'Clothing'),
        (4, 'Jeans', 'Clothing'),
        (5, 'Headphones', 'Electronics')
    ]
    customers = [
        (1, 'John Doe', 'USA'),
        (2, 'Jane Smith', 'UK'),
        (3, 'Alice Brown', 'Canada'),
        (4, 'Bob Wilson', 'Australia'),
        (5, 'Emma Davis', 'USA')
    ]

    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?, ?, ?)', products)
    cursor.executemany('INSERT OR REPLACE INTO customers VALUES (?, ?, ?)', customers)

    orders = []
    order_details = []
    for order_id in range(1, 101):
        customer_id = random.randint(1, 5)
        order_date = (start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        total_amount = 0
        orders.append((order_id, customer_id, order_date, 0))  # Temporary total_amount

        for _ in range(random.randint(1, 3)):
            detail_id = len(order_details) + 1
            product_id = random.randint(1, 5)
            quantity = random.randint(1, 5)
            unit_price = random.uniform(10, 500)
            total_amount += quantity * unit_price
            order_details.append((detail_id, order_id, product_id, quantity, unit_price))

        orders[-1] = (order_id, customer_id, order_date, total_amount)

    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', orders)
    cursor.executemany('INSERT INTO order_details VALUES (?, ?, ?, ?, ?)', order_details)

    conn.commit()
    conn.close()

 
create_database()