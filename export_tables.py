import psycopg2
import csv

DB_URI = "postgresql://postgres.jjgnpqvxwettoxtemdtm:Kevinmiradouro29122021*@aws-0-eu-west-1.pooler.supabase.com:6543/postgres"

tables = [
    "dim_clients",
    "dim_products",
    "fact_contracts",
    "fact_revenue_actuals",
    "fact_targets",
    "ref_fx_rates"
]

conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

for tbl in tables:
    cur.execute(f"SELECT * FROM {tbl}")
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    with open(f"{tbl}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
    print(f"Exported {tbl}.csv — {len(rows)} rows")

cur.close()
conn.close()
print("All base tables exported.")