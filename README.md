# MRSA Biofilm Surveillance Dashboard

![MRSA Biofilm Dashboard](generated-icon.png)

## Overview

This Streamlit dashboard demonstrates a proof-of-concept implementation for the research proposal: "AI-Driven Genomic Surveillance and Mechanistic Inference of High-Biofilm MRSA Lineages for Precision Antibiofilm Therapeutics." The dashboard showcases key components from the proposal, focusing on genomic surveillance, predictive modeling, and therapeutic recommendations for high-biofilm MRSA strains.

The project is designed as a technical demonstration of the methodologies and approaches outlined in the research proposal, with specific alignment to Prof. Papp's work in genomic surveillance and antimicrobial resistance.

## Features

### 1. Genomic Determinants Analysis
- **GWAS Results**: Interactive visualization of genomic variants associated with biofilm formation
- **Machine Learning Models**: Comparison of XGBoost, Random Forest, and Graph Neural Network models for biofilm prediction
- **Feature Importance Analysis**: Identification and visualization of key genomic determinants
- **Demo Genome Analysis**: Simulated analysis of MRSA genomes with biofilm prediction

### 2. Regulatory Circuit Analysis
- **Network Visualization**: Interactive network graph showing biofilm formation regulatory mechanisms
- **Circuit Perturbation Analysis**: Simulation of genetic knockouts and their effects on biofilm formation
- **Expression Module Analysis**: Identification of co-regulated gene modules involved in biofilm pathways

### 3. Surveillance Dashboard
- **Geographic Distribution**: Real-time tracking of high-biofilm MRSA lineages across geographic regions
- **Lineage Tracking**: Temporal analysis of emerging high-biofilm MRSA lineages
- **Therapeutic Coverage Calculator**: Recommendation tool for optimal phage and antibiofilm peptide combinations

## Installation and Setup

### Prerequisites
- Python 3.9+
- Streamlit
- Pandas, NumPy
- Plotly
- NetworkX
- Folium

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mrsa-biofilm-dashboard.git
cd mrsa-biofilm-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The application will be available at http://localhost:5000

## Project Structure

```
mrsa-biofilm-dashboard/
├── app.py                 # Main application file
├── data/                  # Data generation modules
│   ├── sample_gwas_results.py
│   ├── sample_mrsa_data.py
│   ├── sample_phage_data.py
│   └── sample_phylogeny.py
├── pages/                 # Streamlit multi-page components
│   ├── 1_Genomic_Determinants.py
│   ├── 2_Regulatory_Circuits.py
│   └── 3_Surveillance_Dashboard.py
├── utils/                 # Utility functions
│   ├── data_loader.py
│   ├── ml_models.py
│   ├── phage_calculator.py
│   └── visualization.py
├── .streamlit/            # Streamlit configuration
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

## Implementation Details

### Data Sources
This demonstration uses synthetic data that represents realistic MRSA genomic profiles, biofilm measurements, and therapeutic coverage matrices. In a real deployment, this would connect to:

1. **Genomic Data**: NCBI Pathogen Detection, BioProject, and ENA repositories
2. **AMR Data**: PATRIC, CARD, and ResFinder databases
3. **Biofilm Measurements**: Laboratory experimental data from participating hospitals and research labs
4. **Geographic Metadata**: Submissions linked to regional hospitals and surveillance networks

### ML Pipeline Integration
The machine learning pipeline is designed to integrate with high-performance computing infrastructure, using:

1. **Feature Extraction**: k-mer based genomic features, pangenome gene presence/absence, SNPs, and structural variants
2. **Model Training**: XGBoost, Random Forest, and Graph Neural Network approaches
3. **Model Evaluation**: Nested cross-validation (10 × 5-fold)
4. **Deployment**: Models optimized for CPU/GPU execution in hospital settings

### Therapeutic Recommender System
The system uses a greedy optimization algorithm to identify the minimal set of therapeutic agents needed to target a specific set of MRSA lineages, considering:

1. **Agent Coverage**: The spectrum of MRSA lineages each therapeutic component can target
2. **Resistance Probability**: Estimated likelihood of resistance development
3. **Synergistic Effects**: Combinations that produce enhanced biofilm disruption
4. **Regional Availability**: Considering geographic distribution of therapy access

## Integration with Host Lab Infrastructure

This project is designed to integrate with Prof. Papp's lab infrastructure:

1. **Phylogenetic Pipeline**: Uses the same TreeTime workflow from recent Cell publications
2. **Hospital Deployment**: Can be packaged as a Docker container for air-gapped deployment
3. **Computational Resources**: Optimized for HPC cluster and GPU nodes
4. **Data Pipeline**: Integrates with existing genomic data processing workflows

For a detailed mapping of how this project aligns with EMBO Fellowship criteria and Prof. Papp's research focus, see [EMBO_CRITERIA.md](EMBO_CRITERIA.md).

## Future Directions

### Development Roadmap

| Component | Status | Action Item |
|-----------|--------|-------------|
| Real Data | ❌ | Add 100 NCBI genomes + PATRIC phenotypes |
| Lab Tool Integration | ❌ | Fork/PR Prof. Papp's repos (e.g., TreeTime) |
| Performance Metrics | ❌ | Add HPC benchmarks |
| Validation | ❌ | Simulate CRISPRi results |
| EMBO Mapping | ✅ | Add criteria table to README (see EMBO_CRITERIA.md) |

### Planned Enhancements

1. **Real-time Data Integration**: Connection to live genomic surveillance data feeds
2. **Enhanced ML Models**: Integration of transformer-based genomic language models
3. **Mobile Interface**: Development of mobile-optimized views for field epidemiologists
4. **Experimental Validation**: Connection to laboratory biofilm assay data for model refinement

## Acknowledgments

This dashboard is a proof-of-concept implementation based on the research proposal developed for application to Prof. Papp's lab. It builds upon approaches from genomic surveillance, machine learning for bacterial genomics, and precision antimicrobial development.

## Author

This dashboard was developed by:

**Dr. Almotasem Bellah Younis, PhD**  
Website: [https://almotasem-younis.netlify.app](https://almotasem-younis.netlify.app)

## Citation

This is a proof-of-concept implementation for demonstration purposes. No formal citation is required at this time.

## License

This project is licensed under the MIT License - see the LICENSE file for details.