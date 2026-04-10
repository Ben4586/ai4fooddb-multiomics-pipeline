# 🧬 AI4FoodDB Multi-Omics Pipeline

An end-to-end **multi-omics data integration pipeline** built with **Nextflow + Docker + Python**, designed to analyze microbiome, metabolomics, and RNA-seq data for nutritional and health insights.

---

## 🚀 Overview

This project simulates a real-world **precision nutrition / microbiome analysis workflow**, inspired by industrial applications in food science.

### 🔬 Data Modalities

* 🦠 Microbiome (relative abundance)
* 🧪 Metabolomics
* 🧬 RNA-seq (GEO datasets)

---

## ⚙️ Pipeline Architecture

```
Microbiome ─┐
            ├── Merge ─┐
Metabolites ─┘         │
                      ├── Integration ─── ML Model ─── Feature Importance
RNA-seq ──────────────┘
                              │
                              ├── COBRA Metabolic Modeling
                              └── Visualization
```

---

## 🛠️ Technologies Used

* **Nextflow (DSL2)** – workflow orchestration
* **Docker** – reproducible environment
* **Python**:

  * pandas
  * scikit-learn
  * cobra (metabolic modeling)
  * matplotlib / seaborn

---

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/Ben4586/ai4fooddb-multiomics-pipeline.git
cd ai4fooddb-multiomics-pipeline
```

### 2. Build Docker container

```bash
docker build -t ai4fooddb .
```

### 3. Run pipeline

```bash
nextflow run main.nf -with-docker
```

---

## 📊 Outputs

* `integrated.csv` → merged multi-omics dataset
* `feature_importance.csv` → key biological drivers
* metabolic flux predictions (COBRA)
* plots & visualizations

---

## 🧠 Key Features

✔ Multi-omics integration
✔ Automated workflow with Nextflow
✔ Containerized reproducibility
✔ Machine learning modeling
✔ Systems biology (COBRA) integration

## 🎯 Future Improvements

* Add real clinical datasets
* Deep learning models
* Microbiome-host interaction analysis
* Deploy as web app

---

## 👤 Author

**Beng Soon Teh**
Computational Biology / Bioinformatics

---


