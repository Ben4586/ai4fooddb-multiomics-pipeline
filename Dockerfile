FROM continuumio/miniconda3:latest

WORKDIR /app

# Copy environment and install dependencies
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate environment
ENV PATH /opt/conda/envs/ai4fooddb/bin:$PATH

# Copy project files
COPY scripts/ ./scripts
COPY data/ ./data

# Make scripts executable (if needed)
RUN chmod +x scripts/*.py || true