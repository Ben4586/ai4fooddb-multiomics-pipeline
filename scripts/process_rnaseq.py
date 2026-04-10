import sys
import GEOparse
import pandas as pd

geo_file = sys.argv[1]

gse = GEOparse.get_GEO(filepath=geo_file, silent=True)

# Step 1: pivot
df = gse.pivot_samples('VALUE')

# Step 2: transpose (CRITICAL)
df = df.T

# Step 3: create sample_id
df.reset_index(inplace=True)
df.rename(columns={"index": "sample_id"}, inplace=True)

# Step 4: OPTIONAL (match your S1, S2 format)
df["sample_id"] = ["S" + str(i+1) for i in range(len(df))]

# Step 5: clean
df.fillna(0, inplace=True)

# Step 6: save
df.to_csv("rna.csv", index=False)

print(df.head())