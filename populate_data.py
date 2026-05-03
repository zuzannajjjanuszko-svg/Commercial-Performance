import psycopg2
from psycopg2 import extras
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# Your working transaction pooler URI
DB_URI = "postgresql://postgres.jjgnpqvxwettoxtemdtm:Kevinmiradouro29122021*@aws-0-eu-west-1.pooler.supabase.com:6543/postgres"

def connect():
    return psycopg2.connect(DB_URI)

# ---------- 1. dim_clients ----------
regions = ['DACH', 'UK', 'Iberia', 'Nordics', 'France', 'Italy']
segments = ['Asset Manager', 'Bank', 'Corporate', 'Hedge Fund']

clients = pd.DataFrame({
    'client_name': [f'Client_{i}' for i in range(1, 61)],
    'region': np.random.choice(regions, 60),
    'industry_segment': np.random.choice(segments, 60),
    'onboarded_date': [datetime(2021,1,1) + timedelta(days=random.randint(0, 1095)) for _ in range(60)]
})

# ---------- 2. dim_products ----------
products = pd.DataFrame({
    'product_name': ['Market Data Terminal', 'Reference Data Feed', 'Index Benchmarks'],
    'product_tier': ['Professional', 'Enterprise', 'Enterprise'],
    'list_price_monthly': [1500, 3000, 5000]
})

# ---------- 3. fact_contracts ----------
n_contracts = 200
contracts = []
for cid in range(1, n_contracts + 1):
    client_id = random.randint(1, 60)
    client_row = clients.iloc[client_id - 1]
    product_id = random.choices([1,2,3], weights=[0.4, 0.35, 0.25])[0]
    list_price = products.loc[product_id - 1, 'list_price_monthly']
    start_date = client_row['onboarded_date'] + timedelta(days=random.randint(0, 365))
    if random.random() < 0.7:
        end_date = None
    else:
        end_date = start_date + timedelta(days=random.randint(365, 1000))
    discount = random.choices([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
                              weights=[0.2, 0.2, 0.2, 0.15, 0.1, 0.1, 0.05])[0]
    # introduce missing discounts
    if random.random() < 0.01:
        discount = None
    contracted_rev = round(list_price * (1 - (discount or 0)), 2)
    sales_rep = random.choice(['MJ', 'AK', 'LP', 'ST'])
    contracts.append({
        'contract_id': cid,
        'client_id': client_id,
        'product_id': product_id,
        'start_date': start_date,
        'end_date': end_date.date() if end_date else None,
        'contracted_monthly_revenue': contracted_rev,
        'discount_pct': discount * 100 if discount is not None else None,
        'sales_rep': sales_rep
    })

contracts = pd.DataFrame(contracts)

# ---------- 4. fact_revenue_actuals ----------
revenue = []
for _, contract in contracts.iterrows():
    if contract['end_date']:
        end = pd.Timestamp(contract['end_date'])
    else:
        end = pd.Timestamp('2026-04-01')
    month = pd.Timestamp(contract['start_date']).replace(day=1)
    while month <= end:
        rev = contract['contracted_monthly_revenue']
        if random.random() < 0.05:
            rev = round(rev * random.uniform(0.9, 0.98), 2)
        if random.random() < 0.005:
            rev = -round(abs(rev), 2)
        status = random.choices(['Paid', 'Pending', 'Disputed'], weights=[90, 5, 5])[0]
        revenue.append({
            'contract_id': contract['contract_id'],
            'month_date': month.strftime('%Y-%m-%d'),
            'recognized_revenue': rev,
            'invoice_status': status
        })
        month = (month + pd.DateOffset(months=1)).replace(day=1)

# intentional duplicate
if revenue:
    dup = revenue[-1].copy()
    revenue.append(dup)

revenue = pd.DataFrame(revenue)

# ---------- 5. fact_targets ----------
targets = []
for year in [2021, 2022, 2023, 2024, 2025, 2026]:
    for month in range(1, 13):
        for region in regions:
            for product_id in [1,2,3]:
                base = 20000
                growth = (year - 2021) * 0.05
                rev_target = base * (1 + growth) * (1.0 if region == 'DACH' else 1)
                targets.append({
                    'product_id': product_id,
                    'region': region,
                    'month_date': datetime(year, month, 1),
                    'revenue_target': round(rev_target + random.uniform(-5000, 5000), 2),
                    'retention_target': 0.92
                })

targets = pd.DataFrame(targets)

# ---------- 6. ref_fx_rates ----------
fx = []
currencies = ['USD', 'CHF', 'GBP']
for year in [2021,2022,2023,2024,2025,2026]:
    for month in range(1,13):
        for cur in currencies:
            rate = {'USD': 0.92, 'CHF': 1.02, 'GBP': 0.86}[cur] + np.random.normal(0, 0.02)
            fx.append({
                'date': datetime(year, month, 1),
                'currency': cur,
                'rate_to_eur': round(rate, 4)
            })

fx = pd.DataFrame(fx)

# ---------- BULK INSERT USING execute_values (fast & safe) ----------
print("Inserting data into Supabase...")
conn = connect()
cur = conn.cursor()

for table_name, df in [
    ('dim_clients', clients),
    ('dim_products', products),
    ('fact_contracts', contracts),
    ('fact_revenue_actuals', revenue),
    ('fact_targets', targets),
    ('ref_fx_rates', fx)
]:
    cols = list(df.columns)
    # Convert DataFrame to list of tuples with plain Python types
    data = []
    for row in df.itertuples(index=False, name=None):
        clean_row = []
        for val in row:
            if isinstance(val, (np.integer,)):
                clean_row.append(int(val))
            elif isinstance(val, (np.floating,)):
                clean_row.append(float(val))
            elif isinstance(val, (np.bool_,)):
                clean_row.append(bool(val))
            elif pd.isna(val):
                clean_row.append(None)
            else:
                clean_row.append(val)
        data.append(tuple(clean_row))
    
    # Construct the insert with execute_values
    insert_sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s"
    print(f"  Inserting {len(data)} rows into {table_name}...")
    extras.execute_values(cur, insert_sql, data)
    conn.commit()
    print(f"  {table_name} done.")

cur.close()
conn.close()
print("All tables populated successfully.")
