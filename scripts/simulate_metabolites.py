import pandas as pd
import sys

sample_id = sys.argv[1]

micro = pd.read_csv("/app/data/microbiome_real.csv")
diet = pd.read_csv("/app/data/diet.csv")

df = micro.merge(diet, on="sample_id")
row = df[df["sample_id"] == sample_id].copy()

row["butyrate"] = (
    row["Faecalibacterium"] * 0.6 +
    row["Ruminococcus"] * 0.4
) * row["fiber"] * 0.05

row["acetate"] = row["Bacteroides"] * row["fiber"] * 0.03
row["ammonia"] = row["protein"] * 0.02

row.to_csv(f"{sample_id}_metabo.csv", index=False)