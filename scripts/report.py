import pandas as pd

imp = pd.read_csv("feature_importance.csv")

top = imp.sort_values("importance", ascending=False).head(5)

with open("report.txt", "w") as f:
    f.write("Top drivers of butyrate production:\\n")
    f.write(str(top))