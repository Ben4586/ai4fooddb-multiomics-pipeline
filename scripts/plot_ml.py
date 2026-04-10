import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("feature_importance.csv")
df = df.sort_values("importance").tail(10)

plt.barh(df["feature"], df["importance"])
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=300)