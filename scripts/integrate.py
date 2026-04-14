import pandas as pd

# Load data
micro = pd.read_csv("micro.csv")
metabo = pd.read_csv("metabolites.csv")
rna = pd.read_csv("rna.csv")

print("[DEBUG] Micro columns:", micro.columns)
print("[DEBUG] Metabo columns:", metabo.columns)
print("[DEBUG] RNA columns:", rna.columns[:10])

# Ensure sample_id exists
assert "sample_id" in micro.columns
assert "sample_id" in metabo.columns
assert "sample_id" in rna.columns

# Merge step-by-step (LEFT JOIN to preserve microbiome)
df = micro.merge(metabo, on="sample_id", how="left")
df = df.merge(rna, on="sample_id", how="left")

# Fill missing
df.fillna(0, inplace=True)

# Save
df.to_csv("integrated.csv", index=False)

print("[INFO] Integration complete")
print(df.head())