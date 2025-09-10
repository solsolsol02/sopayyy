// Fungsi untuk memuat data sales chart
async function loadSalesChart() {
    const response = await fetch('/api/sales_data');
    const data = await response.json();
    
    const dates = data.map(item => item.date);
    const sales = data.map(item => item.sales);
    
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Penjualan Harian',
                data: sales,
                backgroundColor: 'rgba(52, 152, 219, 0.2)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Tren Penjualan 30 Hari Terakhir'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Jumlah Penjualan'
                    }
                }
            }
        }
    });
}

// Fungsi untuk memuat data forecast chart
async function loadForecastChart() {
    const response = await fetch('/api/forecast');
    const data = await response.json();
    
    const dates = data.map(item => item.date);
    const forecasts = data.map(item => item.forecast);
    
    const ctx = document.getElementById('forecastChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Peramalan Penjualan',
                data: forecasts,
                backgroundColor: 'rgba(46, 204, 113, 0.2)',
                borderColor: 'rgba(46, 204, 113, 1)',
                borderWidth: 2,
                tension: 0.3,
                borderDash: [5, 5]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Peramalan Penjualan 30 Hari Ke Depan'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Perkiraan Penjualan'
                    }
                }
            }
        }
    });
}

// Fungsi untuk memuat data inventory chart
async function loadInventoryChart() {
    const response = await fetch('/api/inventory_status');
    const data = await response.json();
    
    const ctx = document.getElementById('inventoryChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Stok Rendah', 'Stok Cukup'],
            datasets: [{
                data: [data.low_stock, data.sufficient_stock],
                backgroundColor: [
                    'rgba(231, 76, 60, 0.8)',
                    'rgba(46, 204, 113, 0.8)'
                ],
                borderColor: [
                    'rgba(231, 76, 60, 1)',
                    'rgba(46, 204, 113, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Status Inventory'
                }
            }
        }
    });
}

// Fungsi untuk memuat data top products chart
async function loadTopProductsChart() {
    const response = await fetch('/api/top_products');
    const data = await response.json();
    
    const productNames = data.map(item => item.name);
    const productSales = data.map(item => item.sales);
    
    const ctx = document.getElementById('topProductsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: productNames,
            datasets: [{
                label: 'Jumlah Penjualan',
                data: productSales,
                backgroundColor: 'rgba(155, 89, 182, 0.6)',
                borderColor: 'rgba(155, 89, 182, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Top 5 Produk Terlaris'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Jumlah Terjual'
                    }
                }
            }
        }
    });
}