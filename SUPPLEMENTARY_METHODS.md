# Supplementary Methods: Mechanistic AI for MRSA Biofilm Analysis

## Contents
1. [Computational Infrastructure](#computational-infrastructure)
2. [Data Processing Pipeline](#data-processing-pipeline)
3. [Machine Learning Model Specifications](#machine-learning-model-specifications)
4. [Multi-omics Integration Methodology](#multi-omics-integration-methodology)
5. [Hyperparameter Optimization](#hyperparameter-optimization)
6. [Statistical Analysis Framework](#statistical-analysis-framework)
7. [Deployment Architecture](#deployment-architecture)

## Computational Infrastructure

### Hardware Specifications
- **HPC Cluster**: HUN-REN BRC HPC cluster with 128 compute nodes
- **GPU Resources**: 4× NVIDIA A100 40GB GPUs for deep learning models
- **Storage**: 100TB high-performance storage array for genomic datasets
- **Memory**: 512GB RAM per node for large-scale genomic analyses

### Software Environment
- **OS**: CentOS 8.4 with SLURM job scheduler
- **Container System**: Singularity 3.8.0 and Docker 20.10.12
- **Workflow Management**: Nextflow 22.04.0
- **Version Control**: Git 2.35.1 with GitHub for code repositories
- **Data Management**: DVC 2.10.0 for versioning large datasets

## Data Processing Pipeline

### Genome Assembly and QC
- **Assembly**: SPAdes v3.15.4 (parameters: --careful, -k 21,33,55,77)
- **Quality Assessment**: QUAST v5.0.2, CheckM v1.1.3
- **Filtering Criteria**: >90% completeness, <5% contamination, N50 >100kb
- **Annotation**: Prokka v1.14.6 with --genus Staphylococcus --species aureus

### Accessory Genome Analysis
- **Pangenome Construction**: Panaroo v1.2.9 (--clean-mode strict)
- **MGE Detection**: MobileElementFinder v1.0.3, phiSpy v4.2.21
- **SCCmec Typing**: SCCmecFinder v1.3
- **ACME Detection**: Custom BLASTn search against reference database (E-value <1e-30)

### Phenotype Harmonization
- **Biofilm Quantification**: Crystal violet OD570 values standardized to Z-scores
- **MIC Data**: Log2-transformed and normalized within antibiotic classes
- **Metadata Schema**: JSON format following AMR-specific extensions to MIxS v5.0

## Machine Learning Model Specifications

### XGBoost Classifier
- **Implementation**: XGBoost v1.6.1
- **Feature Set**: k-mer profiles (k=31), gene presence/absence, MGE profiles
- **Hyperparameters**: max_depth=6, learning_rate=0.1, n_estimators=500, subsample=0.8
- **Regularization**: L1=0.01, L2=1.0
- **Feature Selection**: Recursive feature elimination with 5-fold CV

### Random Forest
- **Implementation**: scikit-learn 1.1.0
- **Feature Set**: Same as XGBoost
- **Hyperparameters**: n_estimators=1000, max_features='sqrt', min_samples_leaf=4
- **Class Weighting**: 'balanced_subsample'
- **Performance Metrics**: AUROC, AUPRC, F1-score, accuracy, MCC

### Graph Neural Network
- **Framework**: PyTorch 1.12.0 with PyTorch Geometric 2.0.4
- **Architecture**: Graph Attention Network (GAT) with 3 graph convolutional layers
- **Node Features**: Gene embeddings from pre-trained protein language model (ESM-2, 33M parameters)
- **Edge Features**: Functional interactions from STRING database (confidence score >0.7)
- **Embedding Dimension**: 128
- **Attention Heads**: 8
- **Dropout**: 0.2
- **Training Protocol**: Adam optimizer (lr=3e-4), batch size=32, early stopping patience=25 epochs

## Multi-omics Integration Methodology

### Batch Correction
- **Method**: ComBat-seq for RNA-seq, Protein-Combat for proteomics
- **Covariates**: Growth phase, media composition, sequencing platform
- **Evaluation**: Silhouette coefficient for cluster preservation after batch correction
- **Implementation**: scanpy v1.9.1, sva v3.42.0 (R package)

### Multimodal Transformer Architecture
- **Framework**: PyTorch Lightning 1.7.1
- **Transformer Configuration**: 6-layer encoder, 8 attention heads, embedding dim=512
- **Tokenization**: K-mer tokenization for genomics, expression binning for transcriptomics
- **Cross-attention**: Between modality-specific encoders with learnable modality weights
- **Training**: 4×A100 GPUs, mixed precision, gradient accumulation (steps=4)
- **Regularization**: Dropout=0.1, weight decay=1e-4, label smoothing=0.1

### Variational Autoencoder Alternative
- **Architecture**: Multimodal β-VAE with modality-specific encoders
- **Latent Space**: 64-dimensional with KL-divergence annealing
- **Reconstruction Loss**: MSE for continuous features, BCE for binary features
- **Disentanglement**: β=4.0 with cyclical annealing schedule
- **Training**: Alternating optimization with modality dropout (p=0.2)

## Hyperparameter Optimization

### Search Strategy
- **Method**: Bayesian optimization with Optuna v2.10.1
- **Trials**: 100 trials per model with 5-fold cross-validation
- **Objective Function**: Maximize balanced accuracy
- **Pruning**: Asynchronous successive halving with early stopping

### Compute Resources
- **Parallelization**: 16 concurrent trials across 4 nodes
- **Time Budget**: 72 hours per optimization run
- **Checkpointing**: Every 10 trials with state recovery capability

### Hyperparameter Ranges
- **Learning Rates**: Log-uniform between 1e-5 and 1e-2
- **Regularization**: Log-uniform between 1e-6 and 1e-1
- **Network Width**: Categorical [64, 128, 256, 512, 1024]
- **Network Depth**: Integer between 2 and 8

## Statistical Analysis Framework

### GWAS Implementation
- **Software**: DBGWAS v0.5.4, PySEER v1.3.0
- **Population Structure Correction**: Linear mixed model with kinship matrix
- **Multiple Testing**: Benjamini-Hochberg FDR with threshold q<0.05
- **Genetic Relatedness**: PopPUNK v2.4.0 for population structure
- **Effect Size Estimation**: Odds ratios with 95% confidence intervals

### Explainable AI Methods
- **Feature Attribution**: SHAP v0.40.0 with KernelExplainer for black-box models
- **Interaction Detection**: H-statistic for pairwise feature interactions
- **Visualization**: SHAP summary and dependency plots, partial dependence plots
- **Counterfactual Analysis**: DiCE v0.6 for examining causal relationships

## Deployment Architecture

### Dashboard Implementation
- **Framework**: Streamlit v1.14.0
- **Interactive Elements**: Plotly v5.10.0, NetworkX v2.8.6
- **Containerization**: Multi-stage Docker build with slim Python 3.10 base
- **Authentication**: OAuth2 with hospital SSO integration capability

### Real-time Surveillance Pipeline
- **Update Frequency**: Weekly automated runs triggered by cron
- **Data Sources**: NCBI Pathogen Detection API, PATRIC, BioProject
- **ETL Pipeline**: Prefect v2.3.1 workflows with failure handling
- **Phylogeny Updates**: TreeTime v0.8.6 with incremental addition to existing tree

### API Layer
- **Implementation**: FastAPI v0.85.0 with Pydantic v1.10.2 models
- **Documentation**: OpenAPI 3.0 with Swagger UI
- **Rate Limiting**: 100 requests per minute per IP
- **Caching**: Redis v6.2.7 with 12-hour TTL for computationally intensive endpoints

### Hospital Deployment Options
- **Air-gapped**: Singularity container with embedded datasets, monthly updates via secure transfer
- **Connected**: Kubernetes deployment with automated weekly updates
- **Minimum Requirements**: 4 CPU cores, 16GB RAM, 100GB storage for standalone operation 