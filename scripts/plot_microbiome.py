import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("micro.csv")
df.set_index("sample_id").plot(kind="bar", stacked=True)
plt.tight_layout()
plt.savefig("microbiome_composition.png", dpi=300)