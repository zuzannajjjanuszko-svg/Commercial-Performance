import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

base = 24000          # realistic base
regions = ['DACH', 'UK', 'Iberia', 'Nordics', 'France', 'Italy']

targets = []
target_id = 1
for year in [2021, 2022, 2023, 2024, 2025, 2026]:
    for month in range(1, 13):
        for region in regions:
            for product_id in [1, 2, 3]:
                growth = (year - 2021) * 0.05
                rev_target = base * (1 + growth) * 1.0   # no regional multiplier
                targets.append({
                    'target_id': target_id,
                    'product_id': product_id,
                    'region': region,
                    'month_date': datetime(year, month, 1).strftime('%Y-%m-%d'),
                    'revenue_target': round(rev_target + np.random.uniform(-5000, 5000), 2),
                    'retention_target': 0.92
                })
                target_id += 1

df = pd.DataFrame(targets)
df.to_csv('fact_targets.csv', index=False)
print(f"New fact_targets.csv written. Columns: {list(df.columns)}, Rows: {len(df)}")