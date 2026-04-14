import sys
import GEOparse
import pandas as pd

geo_file = sys.argv[1]

# ----------------------
# Load GEO
# ----------------------
gse = GEOparse.get_GEO(filepath=geo_file, silent=True)

# ----------------------
# Pivot
# ----------------------
df = gse.pivot_samples('VALUE')

# ----------------------
# Transpose (samples = rows)
# ----------------------
df = df.T

# ----------------------
# Create sample_id safely
# ----------------------
df.reset_index(inplace=True)

# ALWAYS rename first column to sample_id
df.rename(columns={df.columns[0]: "sample_id"}, inplace=True)

# ----------------------
# Remove control probes
# ----------------------
df = df.loc[:, ~df.columns.str.contains("AFFX", case=False)]
df = df.loc[:, ~df.columns.str.contains("control", case=False)]

# ----------------------
# Ensure sample_id is preserved
# ----------------------
if "sample_id" not in df.columns:
    df.insert(0, "sample_id", ["S" + str(i+1) for i in range(len(df))])

# ----------------------
# Convert numeric (IMPORTANT)
# ----------------------
for col in df.columns:
    if col != "sample_id":
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ----------------------
# Fill missing
# ----------------------
df.fillna(0, inplace=True)

# ----------------------
# Reduce RNA dimensionality (SAFE)
# ----------------------
numeric_df = df.drop(columns=["sample_id"], errors="ignore")

top_n = 20

variance = numeric_df.var()
top_genes = variance.sort_values(ascending=False).head(top_n).index

df = pd.concat([df[["sample_id"]], numeric_df[top_genes]], axis=1)

# ----------------------
# Save
# ----------------------
df.to_csv("rna.csv", index=False)

print("[INFO] RNA processing complete")
print(df.head())