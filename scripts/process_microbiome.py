import pandas as pd
import numpy as np
import sys

sample_id = sys.argv[1]

df = pd.read_csv("/app/data/microbiome_real.csv")
row = df[df["sample_id"] == sample_id]

row.iloc[:, 1:] = np.log(row.iloc[:, 1:] + 1e-6)

row.to_csv(f"{sample_id}_micro.csv", index=False)