import pandas as pd
import numpy as np

def generate_sample_gwas_results():
    """
    Generate sample GWAS results for MRSA biofilm formation.
    
    Returns:
        pandas.DataFrame: Dataframe with sample GWAS results
    """
    # Generate sample GWAS results
    np.random.seed(42)
    
    # Define feature types
    feature_types = ["MGE", "SCCmec", "Core Genome", "Plasmid", "Phage"]
    
    # Create sample data for 100 genetic features
    n_features = 100
    
    # Generate random p-values with some significant hits
    p_values = np.concatenate([
        np.random.uniform(1e-20, 1e-8, 10),     # Very significant
        np.random.uniform(1e-8, 1e-5, 20),      # Moderately significant
        np.random.uniform(1e-5, 0.05, 30),      # Marginally significant
        np.random.uniform(0.05, 1.0, n_features - 60)  # Not significant
    ])
    
    # Generate random genome positions
    positions = np.random.randint(1, 3000000, n_features)
    
    # Generate random odds ratios
    odds_ratios = np.random.normal(1.5, 0.8, n_features)
    odds_ratios = np.abs(odds_ratios)  # Ensure positive
    
    # Feature types
    feature_type_weights = {
        "MGE": 0.2,
        "SCCmec": 0.15,
        "Core Genome": 0.3,
        "Plasmid": 0.15,
        "Phage": 0.2
    }
    feature_probs = [feature_type_weights[ft] for ft in feature_types]
    feature_types_list = np.random.choice(feature_types, n_features, p=feature_probs)
    
    # Create feature names based on type
    features = []
    feature_descriptions = []
    
    for i in range(n_features):
        ft = feature_types_list[i]
        if ft == "MGE":
            features.append(f"MGE_{np.random.randint(1, 50)}")
            feature_descriptions.append(f"Mobile genetic element affecting biofilm regulation")
        elif ft == "SCCmec":
            scc_type = np.random.choice(["I", "II", "III", "IV", "V"])
            features.append(f"SCCmec_type_{scc_type}")
            feature_descriptions.append(f"SCCmec type {scc_type} cassette")
        elif ft == "Core Genome":
            gene = np.random.choice(["sarA", "agr", "icaA", "icaD", "fnbA", "clfA", "sigB", "hla", "spa", "other"])
            if gene == "other":
                gene = f"core_gene_{np.random.randint(1, 100)}"
            features.append(gene)
            feature_descriptions.append(f"Core genome gene involved in biofilm formation")
        elif ft == "Plasmid":
            features.append(f"plasmid_{np.random.randint(1, 20)}")
            feature_descriptions.append(f"Plasmid-encoded factor")
        elif ft == "Phage":
            features.append(f"phage_{np.random.randint(1, 15)}")
            feature_descriptions.append(f"Phage-encoded factor affecting biofilm")
    
    # Create DataFrame
    data = pd.DataFrame({
        "feature": features,
        "feature_type": feature_types_list,
        "feature_description": feature_descriptions,
        "position": positions,
        "p_value": p_values,
        "-log10_pvalue": -np.log10(p_values),
        "odds_ratio": odds_ratios
    })
    
    return data

# Generate sample GWAS results
sample_gwas_results = generate_sample_gwas_results()
