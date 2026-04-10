import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("metabolites.csv")
plt.scatter(df["fiber"], df["butyrate"])
plt.xlabel("Fiber")
plt.ylabel("Butyrate")
plt.tight_layout()
plt.savefig("butyrate_vs_fiber.png", dpi=300)