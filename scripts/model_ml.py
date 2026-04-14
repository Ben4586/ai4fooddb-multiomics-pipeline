import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# ----------------------
# Load data
# ----------------------
df = pd.read_csv("integrated.csv", low_memory=False)

# Keep sample_id separately
sample_ids = df["sample_id"]

# ----------------------
# Define feature groups
# ----------------------
micro_cols = ["Bacteroides", "Prevotella", "Faecalibacterium", "Ruminococcus", "Escherichia"]

metabo_cols = ["fiber", "protein", "fat", "butyrate", "acetate", "ammonia"]

# RNA = everything else numeric
rna_cols = [c for c in df.columns if c not in micro_cols + metabo_cols + ["sample_id"]]

# ----------------------
# Select numeric only
# ----------------------
# Keep only columns that actually exist
available_micro = [c for c in micro_cols if c in df.columns]
available_metabo = [c for c in metabo_cols if c in df.columns]

rna_cols = [c for c in df.columns if c not in available_micro + available_metabo + ["sample_id"]]

df = df[available_micro + available_metabo + rna_cols]

print("[DEBUG] Microbiome columns found:", available_micro)
print("[DEBUG] Metabolite columns found:", available_metabo)
print("[DEBUG] RNA columns count:", len(rna_cols))

df.fillna(0, inplace=True)

# ----------------------
# Reduce RNA dimensionality (CRITICAL)
# ----------------------
top_n = 20

rna_var = df[rna_cols].var()
top_rna = rna_var.sort_values(ascending=False).head(top_n).index

# Keep only selected RNA
df = pd.concat([
    df[available_micro],
    df[available_metabo],
    df[top_rna]
], axis=1)

# ----------------------
# Normalize each omics block
# ----------------------
scaler = StandardScaler()

if available_micro:
    df[available_micro] = scaler.fit_transform(df[available_micro])

if available_metabo:
    df[available_metabo] = scaler.fit_transform(df[available_metabo])

df[top_rna] = scaler.fit_transform(df[top_rna])

# ----------------------
# OPTIONAL: reduce RNA dominance
# ----------------------
df[top_rna] *= 0.5

# ----------------------
# Define target (biologically meaningful)
# ----------------------
# Example: predict butyrate (gut health marker)
y = df["butyrate"]

# Remove target from features
X = df.drop(columns=["butyrate"])

# ----------------------
# Train model
# ----------------------
model = RandomForestRegressor(random_state=42)
model.fit(X, y)

# ----------------------
# Feature importance
# ----------------------
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

importance.to_csv("feature_importance.csv", index=False)

print("[INFO] ML completed")
print(importance.head(10))