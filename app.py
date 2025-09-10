from flask import Flask, render_template, jsonify
import data
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk departemen Manajemen
@app.route('/management')
def management():
    sales_data = data.generate_sales_data()
    forecasting = data.calculate_forecasting(sales_data)
    sales_trend = data.calculate_sales_trend(sales_data)
    statistics = data.calculate_statistics(sales_data)
    
    return render_template('management.html', 
                          sales_data=sales_data,
                          forecasting=forecasting,
                          sales_trend=sales_trend,
                          statistics=statistics)

# Route untuk departemen PPIC
@app.route('/ppic')
def ppic():
    inventory_data = data.generate_inventory_data()
    stock_analysis = data.calculate_stock_analysis(inventory_data)
    demand_forecast = data.calculate_demand_forecast()
    
    return render_template('ppic.html',
                         inventory_data=inventory_data,
                         stock_analysis=stock_analysis,
                         demand_forecast=demand_forecast)

# Route untuk departemen Inventory
@app.route('/inventory')
def inventory():
    inventory_data = data.generate_inventory_data()
    stock_alerts = data.generate_stock_alerts(inventory_data)
    movement_data = data.generate_movement_data()
    
    return render_template('inventory.html',
                         inventory_data=inventory_data,
                         stock_alerts=stock_alerts,
                         movement_data=movement_data)

# API untuk data chart
@app.route('/api/sales-chart-data')
def sales_chart_data():
    sales_data = data.generate_sales_data()
    return jsonify(sales_data)

@app.route('/api/inventory-chart-data')
def inventory_chart_data():
    inventory_data = data.generate_inventory_data()
    return jsonify(inventory_data)

if __name__ == '__main__':
    app.run(debug=True)