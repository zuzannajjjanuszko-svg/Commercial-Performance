import pandas as pd

df = pd.read_csv('v_data_quality_flags.csv')

# Keep only the first Negative Revenue row, drop the rest
neg_mask = df['issue_type'] == 'Negative Revenue'
first_neg_index = df[neg_mask].index[0]   # keep first occurrence
drop_indices = df[neg_mask].index.difference([first_neg_index])

df_clean = df.drop(drop_indices)
df_clean.to_csv('v_data_quality_flags.csv', index=False)

print(f"Kept {len(df_clean)} rows (1 Negative Revenue, rest as before).")