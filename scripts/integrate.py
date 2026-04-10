#!/usr/bin/env python
import pandas as pd

# Load files from working directory (Nextflow staged inputs)
micro = pd.read_csv("micro.csv")
metabo = pd.read_csv("metabolites.csv")
rna = pd.read_csv("rna.csv")

print("Micro columns:", micro.columns)
print("Metabo columns:", metabo.columns)
print("RNA columns:", rna.columns)

# Ensure sample_id exists
assert "sample_id" in micro.columns
assert "sample_id" in metabo.columns
assert "sample_id" in rna.columns

# Merge
df = micro.merge(metabo, on="sample_id", how="outer")
df = df.merge(rna, on="sample_id", how="outer")

df.fillna(0, inplace=True)

# Save output
df.to_csv("integrated.csv", index=False)

print("[INFO] Integration complete")