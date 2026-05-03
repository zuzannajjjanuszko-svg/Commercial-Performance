import pandas as pd
df = pd.read_csv('fact_revenue_actuals.csv')
df.drop_duplicates(inplace=True)
df.to_csv('fact_revenue_actuals.csv', index=False)
print("Duplicates removed. Rows:", len(df))