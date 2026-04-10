#!/usr/bin/env nextflow
nextflow.enable.dsl=2

// ---------------- CHANNEL ----------------
Channel
    .fromPath("data/microbiome_real.csv")
    .splitCsv(header:true)
    .map { row -> tuple(row.sample_id, row) }
    .set { samples_ch }

// ---------------- WORKFLOW ----------------
workflow {

    // Channels
    Channel.fromPath("data/microbiome_real.csv").set { micro_file }
    Channel.fromPath("data/metabolites_placeholder.csv").set { metabo_file }
    Channel.fromPath("data/GSE10072_family.soft.gz").set { geo_file }

    // Parallel steps
    micro_ch  = process_micro(samples_ch)
    metabo_ch = simulate_metabolites(samples_ch)

    // Merge results
    micro  = merge_micro(micro_ch.collect())
    metabo = merge_metabo(metabo_ch.collect())

    // RNA-seq (sequential)
    rna = process_geo(geo_file)

    // Integration
    integrated = integrate_all(micro, metabo, rna)

    // Modeling
    ml  = model_ml(integrated)
    cob = model_cobra(integrated)

    // Visualization
    plot_results(micro, metabo, ml)

    // Report
    report(ml, cob)
}

// ---------------- PROCESSES ----------------

// 🦠 Microbiome (parallel)
process process_micro {

    tag "$sample_id"
    publishDir "results/micro/", mode: 'copy'

    input:
    tuple val(sample_id), val(row)
    
    output:
    path "${sample_id}_micro.csv"

    script:
    """
    set -e
    python /app/scripts/process_microbiome.py ${sample_id}
    """
}

// 🧪 Metabolites (parallel)
process simulate_metabolites {

    tag "$sample_id"
    publishDir "results/metabolites/", mode: 'copy'

    input:
    tuple val(sample_id), val(row)
  
    output:
    path "${sample_id}_metabo.csv"

    script:
    """
    set -e
    python /app/scripts/simulate_metabolites.py ${sample_id}
    """
}

// 🔗 Merge microbiome
process merge_micro {

    input:
    path micro_files

    output:
    path "micro.csv"

    script:
    """
    set -e
    ls *_micro.csv | head -n 1 | xargs head -n 1 > micro.csv
    tail -n +2 -q *_micro.csv >> micro.csv
    """
}

// 🔗 Merge metabolites
process merge_metabo {

    input:
    path metabo_files

    output:
    path "metabolites.csv"

    script:
    """
    set -e
    ls *_metabo.csv | head -n 1 | xargs head -n 1 > metabolites.csv
    tail -n +2 -q *_metabo.csv >> metabolites.csv
    """
}

// 🧬 RNA-seq (GEO)
process process_geo {

    publishDir "results/rna/", mode: 'copy'

    input:
    path geo_file

    output:
    path "rna.csv"

    script:
    """
    set -e
    python /app/scripts/process_rnaseq.py ${geo_file}
    """
}

// 🔗 Integration
process integrate_all {

    publishDir "results/integrated/", mode: 'copy'

    input:
    path micro
    path metabo
    path rna

    output:
    path "integrated.csv"

    script:
    """
    set -e
    python /app/scripts/integrate.py
    """
}

// 🤖 Machine Learning
process model_ml {

    publishDir "results/ml/", mode: 'copy'

    input:
    path integrated

    output:
    path "feature_importance.csv"

    script:
    """
    set -e
    python /app/scripts/model_ml.py
    """
}

// ⚙️ COBRA modeling
process model_cobra {

    publishDir "results/cobra/", mode: 'copy'

    input:
    path integrated

    output:
    path "cobra_growth_rates.csv"

    script:
    """
    set -e
    python /app/scripts/model_cobra.py  
    """
}

// 📊 Plotting
process plot_results {

    publishDir "results/plots/", mode: 'copy'

    input:
    path micro
    path metabo
    path ml

    output:
    path "*.png"

    script:
    """
    set -e
    python /app/scripts/plot_microbiome.py
    python /app/scripts/plot_metabolites.py
    python /app/scripts/plot_ml.py
    """
}

// 📄 Report
process report {

    publishDir "results/", mode: 'copy'

    input:
    path ml
    path cob

    output:
    path "report.txt"

    script:
    """
    set -e
    python /app/scripts/report.py
    """
}