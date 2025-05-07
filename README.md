# E-Commerce Data Analysis Dashboard

A web-based dashboard built with Flask, SQLite, and Chart.js to analyze e-commerce data. Features include sales trends, top products, customer distribution, and average order value, with interactive filters for date ranges, product categories, and countries.

## Features

- Sales Trend: Line chart with date range filtering.
- Top Products: Bar chart with category filtering.
- Customer Distribution: Pie chart (or stat card for single data points) with country filtering.
- Average Order Value: Stat card showing the average order value.

## Setup

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Install dependencies: `pip install flask pandas`
5. Run the database setup: `python database.py`
6. Start the Flask app: `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.

## Technologies Used

- Flask (Python)
- SQLite
- Chart.js
- HTML/CSS/JavaScript
