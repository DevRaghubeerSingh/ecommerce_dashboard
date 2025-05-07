from flask import Flask, render_template, jsonify, request
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ecommerce.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sales_trend')
def sales_trend():
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', '2024-12-31')
    
    conn = get_db_connection()
    query = '''
        SELECT strftime('%Y-%m', order_date) as month, SUM(total_amount) as total_sales
        FROM orders
        WHERE order_date BETWEEN ? AND ?
        GROUP BY month
        ORDER BY month
    '''
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    
    return jsonify({
        'labels': df['month'].tolist(),
        'data': df['total_sales'].tolist()
    })

@app.route('/api/top_products')
def top_products():
    category = request.args.get('category', '')
    
    conn = get_db_connection()
    query = '''
        SELECT p.product_name, SUM(od.quantity) as total_quantity
        FROM order_details od
        JOIN products p ON od.product_id = p.product_id
        WHERE 1=1
    '''
    params = []
    if category:
        query += ' AND p.category = ?'
        params.append(category)
    
    query += ' GROUP BY p.product_name ORDER BY total_quantity DESC LIMIT 5'
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return jsonify({
        'labels': df['product_name'].tolist(),
        'data': df['total_quantity'].tolist()
    })

@app.route('/api/customer_distribution')
def customer_distribution():
    country = request.args.get('country', '')
    
    conn = get_db_connection()
    query = '''
        SELECT country, COUNT(DISTINCT customer_id) as customer_count
        FROM customers
        WHERE 1=1
    '''
    params = []
    if country:
        query += ' AND country = ?'
        params.append(country)
    
    query += ' GROUP BY country'
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return jsonify({
        'labels': df['country'].tolist(),
        'data': df['customer_count'].tolist()
    })

@app.route('/api/average_order_value')
def average_order_value():
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT AVG(total_amount) as aov FROM orders', conn)
    conn.close()
    return jsonify({
        'aov': round(df['aov'][0], 2)
    })

if __name__ == '__main__':
    app.run(debug=True)