import random
from datetime import datetime, timedelta

# Generate data penjualan
def generate_sales_data():
    categories = ['Makanan', 'Minuman', 'Produk Rumah Tangga', 'Kesehatan & Kecantikan', 'Elektronik']
    data = []
    
    for i in range(30):
        date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        for category in categories:
            data.append({
                'date': date,
                'category': category,
                'sales': random.randint(100, 1000),
                'revenue': random.randint(500, 5000)
            })
    
    return data

# Generate data inventory
def generate_inventory_data():
    products = [
        'Indomie Goreng', 'Aqua Gelas', 'Pocari Sweat', 'Sunlight', 
        'Rinso', 'Lifebuoy', 'Chiki Ball', 'Teh Botol', 'Tissue Paseo',
        'Baterai ABC', 'Minyak Goreng', 'Gula Pasir'
    ]
    
    data = []
    for product in products:
        data.append({
            'product': product,
            'stock': random.randint(0, 200),
            'min_stock': 20,
            'price': random.randint(5000, 30000),
            'category': random.choice(['Makanan', 'Minuman', 'Produk Rumah Tangga', 'Kesehatan & Kecantikan', 'Elektronik'])
        })
    
    return data

# Generate peringatan stok
def generate_stock_alerts(inventory_data):
    alerts = []
    for item in inventory_data:
        if item['stock'] < item['min_stock']:
            alerts.append({
                'product': item['product'],
                'current_stock': item['stock'],
                'min_stock': item['min_stock'],
                'status': 'Kritis' if item['stock'] < 5 else 'Warning'
            })
    return alerts

# Generate data pergerakan barang
def generate_movement_data():
    movements = []
    types = ['Masuk', 'Keluar']
    products = ['Indomie Goreng', 'Aqua Gelas', 'Pocari Sweat', 'Sunlight', 'Rinso']
    
    for i in range(50):
        movements.append({
            'date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'product': random.choice(products),
            'type': random.choice(types),
            'quantity': random.randint(10, 100),
            'reference': f'REF{random.randint(1000, 9999)}'
        })
    
    return movements

# Forecasting penjualan
def calculate_forecasting(sales_data):
    # Sederhana: rata-rata penjualan 7 hari terakhir
    recent_sales = [item['sales'] for item in sales_data if item['date'] >= (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')]
    avg_sales = sum(recent_sales) / len(recent_sales) if recent_sales else 0
    
    # Forecast untuk 7 hari ke depan dengan variasi acak
    forecast = []
    for i in range(7):
        forecast.append({
            'date': (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d'),
            'sales': max(100, avg_sales * random.uniform(0.8, 1.2))
        })
    
    return forecast

# Tren penjualan
def calculate_sales_trend(sales_data):
    # Kelompokkan berdasarkan kategori
    categories = {}
    for item in sales_data:
        if item['category'] not in categories:
            categories[item['category']] = []
        categories[item['category']].append(item['sales'])
    
    # Hitung rata-rata per kategori
    trends = {}
    for category, sales in categories.items():
        trends[category] = sum(sales) / len(sales)
    
    return trends

# Statistik penjualan
def calculate_statistics(sales_data):
    total_sales = sum(item['sales'] for item in sales_data)
    total_revenue = sum(item['revenue'] for item in sales_data)
    avg_daily_sales = total_sales / 30  # Asumsi 30 hari
    
    return {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'avg_daily_sales': avg_daily_sales
    }

# Analisis stok
def calculate_stock_analysis(inventory_data):
    total_value = sum(item['stock'] * item['price'] for item in inventory_data)
    low_stock_items = sum(1 for item in inventory_data if item['stock'] < item['min_stock'])
    
    return {
        'total_value': total_value,
        'total_items': len(inventory_data),
        'low_stock_items': low_stock_items
    }

# Peramalan permintaan
def calculate_demand_forecast():
    products = ['Indomie Goreng', 'Aqua Gelas', 'Pocari Sweat', 'Sunlight', 'Rinso']
    forecast = {}
    
    for product in products:
        forecast[product] = random.randint(50, 200)
    
    return forecast