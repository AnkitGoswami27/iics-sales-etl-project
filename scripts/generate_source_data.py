"""
=============================================================================
SOURCE DATA GENERATOR for Sales ETL Data Engineering (Campus Use Case)
=============================================================================
Generates 4 CSV files:
  1. sales_transactions.csv      - 50 records (Clean)
  2. product_master.csv           - 10 records (Clean)
  3. customer_master.csv          - 20 records (Clean)
  4. sales_transactions_dirty.csv - 40 records (Requires Cleansing)
=============================================================================
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)  # For reproducibility

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── 1. PRODUCT MASTER (10 products, 5 categories) ───────────────────────────
products = [
    (101, "Laptop",         "Electronics",  "TechCorp",     45000.00),
    (102, "Smartphone",     "Electronics",  "MobileInc",    25000.00),
    (103, "Headphones",     "Electronics",  "AudioPro",      2000.00),
    (104, "Running Shoes",  "Footwear",     "SportMax",      3500.00),
    (105, "Formal Shoes",   "Footwear",     "ClassicWear",   4200.00),
    (106, "T-Shirt",        "Clothing",     "FashionHub",     800.00),
    (107, "Jeans",          "Clothing",     "DenimWorld",    1500.00),
    (108, "Office Chair",   "Furniture",    "ComfortPlus",   8500.00),
    (109, "Study Table",    "Furniture",    "WoodCraft",     6200.00),
    (110, "Novel Book",     "Books",        "ReadMore",       350.00),
]

with open(os.path.join(OUTPUT_DIR, "product_master.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["PRODUCT_ID", "PRODUCT_NAME", "CATEGORY", "SUPPLIER", "COST_PRICE"])
    for p in products:
        w.writerow(p)

print("✓ product_master.csv created (10 records)")

# ─── 2. CUSTOMER MASTER (20 customers, ~12 states) ───────────────────────────
states_cities = [
    ("Maharashtra",    "Mumbai"),
    ("Maharashtra",    "Pune"),
    ("Karnataka",      "Bangalore"),
    ("Karnataka",      "Mysore"),
    ("Tamil Nadu",     "Chennai"),
    ("Tamil Nadu",     "Coimbatore"),
    ("Delhi",          "New Delhi"),
    ("Uttar Pradesh",  "Lucknow"),
    ("Uttar Pradesh",  "Noida"),
    ("Gujarat",        "Ahmedabad"),
    ("Rajasthan",      "Jaipur"),
    ("West Bengal",    "Kolkata"),
    ("Telangana",      "Hyderabad"),
    ("Kerala",         "Kochi"),
    ("Madhya Pradesh", "Bhopal"),
    ("Punjab",         "Chandigarh"),
    ("Bihar",          "Patna"),
    ("Odisha",         "Bhubaneswar"),
    ("Assam",          "Guwahati"),
    ("Haryana",        "Gurugram"),
]

first_names = ["Amit", "Priya", "Rahul", "Sneha", "Vikram",
               "Anjali", "Rohit", "Neha", "Suresh", "Kavita",
               "Arjun", "Pooja", "Deepak", "Swati", "Manoj",
               "Ritu", "Sanjay", "Divya", "Kiran", "Meera"]
last_names  = ["Sharma", "Patel", "Gupta", "Singh", "Kumar",
               "Reddy", "Nair", "Joshi", "Verma", "Das",
               "Mehta", "Rao", "Mishra", "Iyer", "Chopra",
               "Bose", "Pandey", "Thakur", "Agarwal", "Sethi"]

customers = []
base_date = datetime(2024, 1, 1)
for i in range(20):
    cid = 201 + i
    name = f"{first_names[i]} {last_names[i]}"
    email = f"{first_names[i].lower()}.{last_names[i].lower()}@email.com"
    state, city = states_cities[i]
    reg_date = (base_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    customers.append((cid, name, email, city, state, reg_date))

with open(os.path.join(OUTPUT_DIR, "customer_master.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["CUSTOMER_ID", "CUSTOMER_NAME", "EMAIL", "CITY", "STATE", "REGISTRATION_DATE"])
    for c in customers:
        w.writerow(c)

print("✓ customer_master.csv created (20 records)")

# ─── 3. SALES TRANSACTIONS - CLEAN (50 records) ─────────────────────────────
product_ids   = [p[0] for p in products]
customer_ids  = [c[0] for c in customers]
product_prices = {p[0]: p[4] for p in products}

# Generate unit prices with some markup over cost price
def get_unit_price(pid):
    cost = product_prices[pid]
    markup = random.uniform(1.1, 1.5)  # 10%-50% markup
    return round(cost * markup, 2)

clean_txns = []
txn_start = datetime(2025, 1, 1)
for i in range(50):
    tid = 1001 + i
    tdate = (txn_start + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d")
    cid = random.choice(customer_ids)
    pid = random.choice(product_ids)
    qty = random.randint(1, 5)
    unit_price = get_unit_price(pid)
    discount = round(random.uniform(0, 30), 2)  # 0-30% discount (valid)
    clean_txns.append((tid, tdate, cid, pid, qty, unit_price, discount))

with open(os.path.join(OUTPUT_DIR, "sales_transactions.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["TRANSACTION_ID", "TRANSACTION_DATE", "CUSTOMER_ID", "PRODUCT_ID",
                 "QUANTITY", "UNIT_PRICE", "DISCOUNT_PERCENT"])
    for t in clean_txns:
        w.writerow(t)

print("✓ sales_transactions.csv created (50 records)")

# ─── 4. SALES TRANSACTIONS - DIRTY (40 records with bad data) ────────────────
#
# Bad data rules injected:
#   a. Negative quantity (rows ~5)     → Should be made positive
#   b. Mixed date formats (rows ~5)    → Should be standardized to YYYY-MM-DD
#   c. Null CUSTOMER_ID (rows ~3)      → Reject
#   d. Null UNIT_PRICE (rows ~3)       → Reject
#   e. Discount > 100% (rows ~3)       → Reject
#   f. Null CUSTOMER_ID (same as c)    → Reject
#   g. Zero quantity (rows ~3)         → Reject
#   h. Negative discount (rows ~3)     → Change to positive
#   Some rows are perfectly clean      → Should pass through

dirty_txns = []
dirty_date_formats = ["%d-%m-%Y", "%m/%d/%Y", "%d %b %Y", "%Y/%m/%d"]

for i in range(40):
    tid = 2001 + i
    tdate_obj = txn_start + timedelta(days=random.randint(0, 300))
    cid = random.choice(customer_ids)
    pid = random.choice(product_ids)
    qty = random.randint(1, 5)
    unit_price = get_unit_price(pid)
    discount = round(random.uniform(0, 25), 2)

    # Inject specific bad data at known positions
    if i in [0, 7, 14, 21, 28]:
        # a. Negative quantity
        qty = -abs(qty)
        tdate = tdate_obj.strftime("%Y-%m-%d")
    elif i in [1, 8, 15, 22, 29]:
        # b. Mixed date formats
        fmt = dirty_date_formats[i % len(dirty_date_formats)]
        tdate = tdate_obj.strftime(fmt)
    elif i in [2, 9, 16]:
        # c/f. Null CUSTOMER_ID
        cid = ""
        tdate = tdate_obj.strftime("%Y-%m-%d")
    elif i in [3, 10, 17]:
        # d. Null UNIT_PRICE
        unit_price = ""
        tdate = tdate_obj.strftime("%Y-%m-%d")
    elif i in [4, 11, 18]:
        # e. Discount > 100%
        discount = round(random.uniform(110, 200), 2)
        tdate = tdate_obj.strftime("%Y-%m-%d")
    elif i in [5, 12, 19]:
        # g. Zero quantity
        qty = 0
        tdate = tdate_obj.strftime("%Y-%m-%d")
    elif i in [6, 13, 20]:
        # h. Negative discount
        discount = -abs(round(random.uniform(5, 25), 2))
        tdate = tdate_obj.strftime("%Y-%m-%d")
    else:
        # Clean rows
        tdate = tdate_obj.strftime("%Y-%m-%d")

    dirty_txns.append((tid, tdate, cid, pid, qty, unit_price, discount))

with open(os.path.join(OUTPUT_DIR, "sales_transactions_dirty.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["TRANSACTION_ID", "TRANSACTION_DATE", "CUSTOMER_ID", "PRODUCT_ID",
                 "QUANTITY", "UNIT_PRICE", "DISCOUNT_PERCENT"])
    for t in dirty_txns:
        w.writerow(t)

print("✓ sales_transactions_dirty.csv created (40 records)")
print("\n✅ All 4 source files generated successfully in:", OUTPUT_DIR)
