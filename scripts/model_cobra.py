import cobra
import pandas as pd

diet = pd.read_csv("/app/data/diet.csv")
model = cobra.io.load_model("textbook")

results = []

for _, row in diet.iterrows():
    m = model.copy()
    m.reactions.get_by_id("EX_glc__D_e").lower_bound = -row["fiber"]

    sol = m.optimize()

    results.append({
        "sample_id": row["sample_id"],
        "growth_rate": sol.objective_value
    })

pd.DataFrame(results).to_csv("cobra_growth_rates.csv", index=False)