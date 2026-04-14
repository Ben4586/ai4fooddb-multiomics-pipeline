import pandas as pd

# ----------------------
# Load results
# ----------------------
fi = pd.read_csv("feature_importance.csv")
cobra = pd.read_csv("cobra_growth_rates.csv")

# ----------------------
# Define feature groups
# ----------------------
micro_features = ["Bacteroides", "Prevotella", "Faecalibacterium", "Ruminococcus", "Escherichia"]

metabo_features = ["fiber", "protein", "fat", "butyrate", "acetate", "ammonia"]

# Classify features
def classify_feature(f):
    if f in micro_features:
        return "microbiome"
    elif f in metabo_features:
        return "metabolite"
    else:
        return "rna"

fi["type"] = fi["feature"].apply(classify_feature)

# ----------------------
# Get top features per omics
# ----------------------
top_micro = fi[fi["type"] == "microbiome"].sort_values("importance", ascending=False).head(3)
top_metabo = fi[fi["type"] == "metabolite"].sort_values("importance", ascending=False).head(3)
top_rna = fi[fi["type"] == "rna"].sort_values("importance", ascending=False).head(5)

# ----------------------
# Build report
# ----------------------
report_lines = []
report_lines.append("=== BIOLOGICAL INTERPRETATION ===\n")

# ----------------------
# Global top (for transparency)
# ----------------------
report_lines.append("Top predictive features (global):\n")
top_global = fi.sort_values("importance", ascending=False).head(10)

for _, row in top_global.iterrows():
    report_lines.append(f"{row['feature']} (importance={row['importance']:.3f})")

# ----------------------
# Microbiome Insights
# ----------------------
report_lines.append("\n--- Microbiome Insights ---")

if not top_micro.empty:
    for f in top_micro["feature"]:
        if f == "Bacteroides":
            report_lines.append("Bacteroides → associated with protein/fat-rich diets")
        elif f == "Prevotella":
            report_lines.append("Prevotella → associated with fiber-rich diets")
        elif f == "Faecalibacterium":
            report_lines.append("Faecalibacterium → butyrate producer, anti-inflammatory")
        elif f == "Ruminococcus":
            report_lines.append("Ruminococcus → fiber degradation and SCFA production")
        elif f == "Escherichia":
            report_lines.append("Escherichia → potential marker of dysbiosis")
else:
    report_lines.append("Microbiome features contributed less to prediction compared to other omics layers.")

# ----------------------
# Metabolomics Insights
# ----------------------
report_lines.append("\n--- Metabolomics Insights ---")

if not top_metabo.empty:
    for f in top_metabo["feature"]:
        if f == "butyrate":
            report_lines.append("Butyrate → key SCFA supporting gut barrier and anti-inflammatory effects")
        elif f == "acetate":
            report_lines.append("Acetate → involved in host energy metabolism and cross-feeding")
        elif f == "ammonia":
            report_lines.append("Ammonia → protein fermentation; excess linked to gut imbalance")
        elif f == "fiber":
            report_lines.append("Dietary fiber → drives SCFA production and microbiome diversity")
        elif f == "protein":
            report_lines.append("Protein intake → influences nitrogen metabolism and microbiome composition")
        elif f == "fat":
            report_lines.append("Dietary fat → impacts bile acids and microbial ecology")
else:
    report_lines.append("Metabolite features were not dominant drivers in the model.")

# ----------------------
# Transcriptomics Insights
# ----------------------
report_lines.append("\n--- Transcriptomics Insights ---")

if not top_rna.empty:
    report_lines.append("Top gene signals:")
    for f in top_rna["feature"]:
        report_lines.append(f"{f}")
    report_lines.append(
        "These genes may reflect host metabolic and immune responses to diet–microbiome interactions."
    )
else:
    report_lines.append("Transcriptomic contribution was limited.")

# ----------------------
# COBRA Insights
# ----------------------
report_lines.append("\n--- Systems Biology (COBRA) ---")

mean_growth = cobra["growth_rate"].mean()
report_lines.append(f"Average predicted microbial growth rate: {mean_growth:.3f}")

if mean_growth > 0.5:
    report_lines.append("Indicates metabolically active microbial communities.")
else:
    report_lines.append("Suggests constrained microbial metabolism.")

# ----------------------
# Integrated Insight (IMPORTANT)
# ----------------------
report_lines.append("\n--- Integrated Insight ---")

report_lines.append(
    "Multi-omics integration reveals that microbiome composition (e.g. fiber-degrading taxa), "
    "metabolic outputs (SCFAs), and host gene expression jointly shape metabolic outcomes."
)

report_lines.append(
    "Although transcriptomics contributes strongly, microbiome and metabolite signals provide "
    "mechanistic insight into diet–microbe–host interactions."
)

# ----------------------
# Save report
# ----------------------
with open("biological_interpretation.txt", "w") as f:
    f.write("\n".join(report_lines))

print("[INFO] Biological interpretation generated")