from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import math
import random
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = 'alfamart_secret_key_2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alfamart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)
    price = db.Column(db.Float, default=0.0)
    supplier = db.Column(db.String(100))

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    store_location = db.Column(db.String(100))

class InventoryMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    movement_type = db.Column(db.String(20))  # 'in' or 'out'
    quantity = db.Column(db.Integer, nullable=False)
    movement_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['department'] = user.department
            session['fullname'] = user.fullname
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    department = session['department']
    
    if department == 'management':
        return render_template('management.html')
    elif department == 'ppic':
        return render_template('ppic.html')
    elif department == 'inventory':
        return render_template('inventory.html')
    
    return redirect(url_for('login'))

@app.route('/forecasting')
def forecasting():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('forecasting.html')

@app.route('/sales_trends')
def sales_trends():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('sales_trends.html')

@app.route('/inventory_report')
def inventory_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('inventory_report.html')

@app.route('/production_plan')
def production_plan():
    if 'user_id' not in session or session['department'] != 'ppic':
        flash('Akses ditolak! Hanya untuk departemen PPIC.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('production_plan.html')

# API Routes
@app.route('/api/sales_data')
def sales_data():
    # Generate sample sales data for the last 30 days
    days = 30
    sales_data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
        # Weekly pattern with some randomness
        day_of_week = (base_date + timedelta(days=i)).weekday()
        if day_of_week in [5, 6]:  # Weekend
            sales = random.randint(4000, 6000)
        else:
            sales = random.randint(2000, 4000)
        
        # Add some upward trend
        sales += i * 20
        
        sales_data.append({
            'date': date,
            'sales': sales
        })
    
    return jsonify(sales_data)

@app.route('/api/forecast')
def forecast_data():
    # Get historical data
    days = 30
    historical_data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
        day_of_week = (base_date + timedelta(days=i)).weekday()
        if day_of_week in [5, 6]:  # Weekend
            sales = random.randint(4000, 6000)
        else:
            sales = random.randint(2000, 4000)
        sales += i * 20
        historical_data.append(sales)
    
    # Simple linear regression for forecasting
    X = np.array(range(days)).reshape(-1, 1)
    y = np.array(historical_data)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast next 14 days
    forecast_days = 14
    future_X = np.array(range(days, days + forecast_days)).reshape(-1, 1)
    future_y = model.predict(future_X)
    
    forecast_data = []
    for i in range(forecast_days):
        date = (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')
        # Add some randomness to the forecast
        forecast_value = max(1000, future_y[i] + random.randint(-300, 300))
        forecast_data.append({
            'date': date,
            'forecast': int(forecast_value)
        })
    
    return jsonify(forecast_data)

@app.route('/api/inventory_status')
def inventory_status():
    # Get inventory status from database
    products = Product.query.all()
    low_stock = [p for p in products if p.stock < p.min_stock]
    sufficient_stock = [p for p in products if p.stock >= p.min_stock]
    
    return jsonify({
        'low_stock': len(low_stock),
        'sufficient_stock': len(sufficient_stock),
        'total_products': len(products),
        'low_stock_items': [{'name': p.name, 'stock': p.stock, 'min_stock': p.min_stock} for p in low_stock]
    })

@app.route('/api/top_products')
def top_products():
    # Get top selling products (simulated data)
    top_products = [
        {'name': 'Rokok Surya 12', 'sales': 1250, 'revenue': 18750000},
        {'name': 'Indomie Goreng', 'sales': 980, 'revenue': 6860000},
        {'name': 'Aqua Gelas', 'sales': 875, 'revenue': 2625000},
        {'name': 'Telur 1kg', 'sales': 652, 'revenue': 12388000},
        {'name': 'Minyak Goreng', 'sales': 521, 'revenue': 10420000}
    ]
    
    return jsonify(top_products)

@app.route('/api/category_sales')
def category_sales():
    # Sales by category (simulated data)
    categories = [
        {'name': 'Rokok', 'sales': 2850, 'percentage': 35},
        {'name': 'Makanan Instan', 'sales': 1950, 'percentage': 24},
        {'name': 'Minuman', 'sales': 1450, 'percentage': 18},
        {'name': 'Sembako', 'sales': 1150, 'percentage': 14},
        {'name': 'Lainnya', 'sales': 700, 'percentage': 9}
    ]
    
    return jsonify(categories)

@app.route('/api/store_performance')
def store_performance():
    # Store performance data (simulated)
    stores = [
        {'name': 'Cabang Utama', 'sales': 3250, 'target': 3000, 'progress': 108},
        {'name': 'Cabang Mall', 'sales': 2850, 'target': 3200, 'progress': 89},
        {'name': 'Cabang Pusat Kota', 'sales': 2450, 'target': 2500, 'progress': 98},
        {'name': 'Cabang Pinggir Kota', 'sales': 1950, 'target': 1800, 'progress': 108}
    ]
    
    return jsonify(stores)

@app.route('/api/inventory_movements')
def inventory_movements():
    # Recent inventory movements (simulated)
    movements = [
        {'product': 'Indomie Goreng', 'type': 'in', 'quantity': 100, 'date': '2023-10-15', 'notes': 'Restok dari supplier'},
        {'product': 'Rokok Surya 12', 'type': 'out', 'quantity': 50, 'date': '2023-10-15', 'notes': 'Penjualan'},
        {'product': 'Aqua Gelas', 'type': 'in', 'quantity': 200, 'date': '2023-10-14', 'notes': 'Restok dari supplier'},
        {'product': 'Minyak Goreng', 'type': 'out', 'quantity': 30, 'date': '2023-10-14', 'notes': 'Penjualan'},
        {'product': 'Telur 1kg', 'type': 'in', 'quantity': 40, 'date': '2023-10-13', 'notes': 'Restok dari supplier'}
    ]
    
    return jsonify(movements)

@app.route('/api/production_plan')
def production_plan_data():
    # Production plan data (simulated)
    plans = [
        {'product': 'Indomie Goreng', 'planned_qty': 5000, 'actual_qty': 4800, 'status': 'completed', 'due_date': '2023-10-20'},
        {'product': 'Rokok Surya 12', 'planned_qty': 3000, 'actual_qty': 3000, 'status': 'completed', 'due_date': '2023-10-18'},
        {'product': 'Aqua Gelas', 'planned_qty': 2000, 'actual_qty': 1500, 'status': 'in_progress', 'due_date': '2023-10-25'},
        {'product': 'Minyak Goreng', 'planned_qty': 1500, 'actual_qty': 0, 'status': 'planned', 'due_date': '2023-11-01'},
        {'product': 'Telur 1kg', 'planned_qty': 1000, 'actual_qty': 0, 'status': 'planned', 'due_date': '2023-11-05'}
    ]
    
    return jsonify(plans)

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

# Initialize database with sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create sample users if they don't exist
        if not User.query.filter_by(username='management').first():
            db.session.add(User(
                username='management', 
                password='management123', 
                department='management',
                fullname='Manager Utama'
            ))
        
        if not User.query.filter_by(username='ppic').first():
            db.session.add(User(
                username='ppic', 
                password='ppic123', 
                department='ppic',
                fullname='Supervisor PPIC'
            ))
        
        if not User.query.filter_by(username='inventory').first():
            db.session.add(User(
                username='inventory', 
                password='inventory123', 
                department='inventory',
                fullname='Supervisor Gudang'
            ))
        
        # Create sample products if they don't exist
        if not Product.query.first():
            products = [
                Product(name='Rokok Surya 12', category='Rokok', stock=150, min_stock=50, price=15000, supplier='Gudang Garam'),
                Product(name='Indomie Goreng', category='Makanan Instan', stock=200, min_stock=100, price=7000, supplier='Indofood'),
                Product(name='Aqua Gelas', category='Minuman', stock=300, min_stock=150, price=3000, supplier='Danone'),
                Product(name='Telur 1kg', category='Sembako', stock=40, min_stock=20, price=19000, supplier='Peternakan Setia'),
                Product(name='Minyak Goreng', category='Sembako', stock=60, min_stock=30, price=20000, supplier='Sawit Indo')
            ]
            
            for product in products:
                db.session.add(product)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)