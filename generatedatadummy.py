import pandas as pd
import numpy as np

# Daftar produk fiktif
products = [
    'Pastaria Classic', 'Pastaria Carbonara', 'Pastaria Pesto', 
    "Sei'Tan Original", "Sei'Tan Spicy", "Sei'Tan Teriyaki",
    'Sek Fan Chicken', 'Sek Fan Beef', 'Sek Fan Vegetarian',
    'Ryujin Sushi', 'Ryujin Ramen', 'Ryujin Bento',
    'Snack Box A', 'Snack Box B', 'Snack Box C',
    'Dessert Box 1', 'Dessert Box 2', 'Dessert Box 3',
    'Drink A', 'Drink B', 'Drink C', 'Drink D',
    'Special Promo 1', 'Special Promo 2', 'Special Promo 3'
]

# Fungsi buat harga random per produk
def random_price(product):
    if 'Pastaria' in product:
        return np.random.randint(50000, 100001)
    elif "Sei'Tan" in product:
        return np.random.randint(60000, 120001)
    elif 'Sek Fan' in product:
        return np.random.randint(30000, 70001)
    elif 'Ryujin' in product:
        return np.random.randint(70000, 150001)
    elif 'Snack' in product or 'Dessert' in product or 'Drink' in product:
        return np.random.randint(10000, 50001)
    elif 'Promo' in product:
        return np.random.randint(20000, 80001)
    else:
        return np.random.randint(20000, 100001)

# Fungsi stok awal random
def random_initial_stock(product):
    if 'Pastaria' in product:
        return np.random.randint(50, 100)
    elif "Sei'Tan" in product:
        return np.random.randint(40, 90)
    elif 'Sek Fan' in product:
        return np.random.randint(30, 80)
    elif 'Ryujin' in product:
        return np.random.randint(20, 70)
    else:
        return np.random.randint(20, 60)

# Atur tanggal
start_date = '2025-08-01'
days = 30
date_range = pd.date_range(start=start_date, periods=days, freq='D')

# DataFrame kosong
sales_data = pd.DataFrame(columns=['Date', 'Product', 'Initial Stock', 'Units Sold', 'Price', 'Revenue'])

# Isi data
for product in products:
    initial_stock = random_initial_stock(product)
    units_sold_raw = np.random.poisson(lam=np.random.randint(20, 100), size=days)
    units_sold = np.minimum(units_sold_raw, initial_stock)  # batasi tidak lebih dari initial stock
    price = random_price(product)
    
    product_sales = pd.DataFrame({
        'Date': date_range,
        'Product': product,
        'Initial Stock': initial_stock,
        'Units Sold': units_sold,
        'Price': price,
    })
    product_sales['Revenue'] = product_sales['Units Sold'] * product_sales['Price']
    
    sales_data = pd.concat([sales_data, product_sales], ignore_index=True)

# Preview data
print(sales_data.head(20))

# Simpan CSV
sales_data.to_csv('sales_data_dummy.csv', index=False)