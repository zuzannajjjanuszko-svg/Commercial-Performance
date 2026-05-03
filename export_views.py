import psycopg2
import csv

# Your working pooler URI
DB_URI = "postgresql://postgres.jjgnpqvxwettoxtemdtm:Kevinmiradouro29122021*@aws-0-eu-west-1.pooler.supabase.com:6543/postgres"

views = [
    "v_revenue_attainment",
    "v_pricing_adherence",
    "v_net_revenue_retention",
    "v_renewal_pipeline",
    "v_data_quality_flags"
]

conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

for view in views:
    cur.execute(f"SELECT * FROM {view}")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    with open(f"{view}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(rows)
    print(f"Exported {view}.csv — {len(rows)} rows")

cur.close()
conn.close()
print("All views exported to CSV.")