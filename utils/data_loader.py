import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

def load_sample_data():
    """
    Load sample MRSA data with biofilm formation measurements.
    
    Returns:
        pandas.DataFrame: Dataframe with sample MRSA data
    """
    # Generate sample data
    np.random.seed(42)
    
    # Create sample data for 200 MRSA isolates
    n_samples = 200
    
    # Generate random biofilm OD590 values with a bimodal distribution
    biofilm_od590 = np.concatenate([
        np.random.normal(0.15, 0.08, n_samples // 2),  # Low biofilm formers
        np.random.normal(0.45, 0.12, n_samples // 2)   # High biofilm formers
    ])
    
    # Ensure values are positive
    biofilm_od590 = np.maximum(0.01, biofilm_od590)
    
    # Create DataFrame
    data = pd.DataFrame({
        "isolate_id": [f"MRSA_{i:04d}" for i in range(1, n_samples + 1)],
        "lineage": np.random.choice(["ST5", "ST8", "ST22", "ST36", "ST45", "ST239", "ST398"], n_samples),
        "biofilm_od590": biofilm_od590,
        "is_high_biofilm": biofilm_od590 > 0.3
    })
    
    return data

def load_sample_gwas_results():
    """
    Load sample GWAS results for MRSA biofilm formation.
    
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

def load_sample_ml_models():
    """
    Load sample machine learning model results.
    
    Returns:
        dict: Dictionary with sample ML model results
    """
    # Generate sample ML model results
    models = {
        "XGBoost": {
            "auroc": 0.93,
            "accuracy": 0.88,
            "precision": 0.86,
            "recall": 0.85,
            "f1": 0.855
        },
        "RandomForest": {
            "auroc": 0.91,
            "accuracy": 0.87,
            "precision": 0.84,
            "recall": 0.82,
            "f1": 0.83
        },
        "GraphNeuralNetwork": {
            "auroc": 0.94,
            "accuracy": 0.89,
            "precision": 0.87,
            "recall": 0.86,
            "f1": 0.865
        }
    }
    
    return models

def load_sample_regulatory_data():
    """
    Load sample regulatory network data.
    
    Returns:
        dict: Dictionary with sample regulatory network data
    """
    # Generate sample regulatory network data
    regulatory_data = {
        "nodes": [
            {"id": "sarA", "type": "regulator", "biofilm_effect": "positive"},
            {"id": "agr", "type": "regulator", "biofilm_effect": "negative"},
            {"id": "icaA", "type": "target", "biofilm_effect": "positive"},
            {"id": "icaD", "type": "target", "biofilm_effect": "positive"},
            {"id": "fnbA", "type": "target", "biofilm_effect": "positive"},
            {"id": "clfA", "type": "target", "biofilm_effect": "positive"},
            {"id": "sigB", "type": "regulator", "biofilm_effect": "positive"},
            {"id": "saeRS", "type": "regulator", "biofilm_effect": "variable"},
            {"id": "rot", "type": "regulator", "biofilm_effect": "positive"},
            {"id": "spa", "type": "target", "biofilm_effect": "positive"},
            {"id": "hla", "type": "target", "biofilm_effect": "negative"},
            {"id": "ACME", "type": "MGE", "biofilm_effect": "positive"},
            {"id": "SCCmec_II", "type": "MGE", "biofilm_effect": "positive"},
            {"id": "phiSa3", "type": "MGE", "biofilm_effect": "variable"}
        ],
        "edges": [
            {"source": "sarA", "target": "icaA", "type": "activation", "weight": 2.0},
            {"source": "sarA", "target": "fnbA", "type": "activation", "weight": 1.5},
            {"source": "sarA", "target": "clfA", "type": "activation", "weight": 1.5},
            {"source": "agr", "target": "sarA", "type": "repression", "weight": 1.0},
            {"source": "agr", "target": "rot", "type": "repression", "weight": 2.0},
            {"source": "agr", "target": "hla", "type": "activation", "weight": 2.5},
            {"source": "rot", "target": "spa", "type": "activation", "weight": 1.5},
            {"source": "sigB", "target": "sarA", "type": "activation", "weight": 1.0},
            {"source": "sigB", "target": "icaA", "type": "activation", "weight": 0.5},
            {"source": "saeRS", "target": "fnbA", "type": "activation", "weight": 1.0},
            {"source": "phiSa3", "target": "agr", "type": "modulation", "weight": 1.0},
            {"source": "SCCmec_II", "target": "sarA", "type": "modulation", "weight": 0.8},
            {"source": "ACME", "target": "biofilm", "type": "activation", "weight": 1.2}
        ]
    }
    
    return regulatory_data

def load_sample_surveillance_data():
    """
    Load sample MRSA surveillance data.
    
    Returns:
        pandas.DataFrame: Dataframe with sample surveillance data
    """
    # Generate sample surveillance data
    np.random.seed(42)
    
    # Define countries and their coordinates
    countries = {
        "United States": (37.0902, -95.7129),
        "United Kingdom": (55.3781, -3.4360),
        "Germany": (51.1657, 10.4515),
        "France": (46.2276, 2.2137),
        "Italy": (41.8719, 12.5674),
        "Spain": (40.4637, -3.7492),
        "Japan": (36.2048, 138.2529),
        "China": (35.8617, 104.1954),
        "Australia": (-25.2744, 133.7751),
        "Brazil": (-14.2350, -51.9253),
        "India": (20.5937, 78.9629),
        "South Africa": (-30.5595, 22.9375),
        "Canada": (56.1304, -106.3468),
        "Russia": (61.5240, 105.3188),
        "Hungary": (47.1625, 19.5033)
    }
    
    # Define MRSA lineages
    lineages = ["ST5", "ST8", "ST22", "ST36", "ST45", "ST239", "ST398", "ST15", "ST80", "ST97"]
    
    # Define SCCmec types
    sccmec_types = ["I", "II", "III", "IV", "V", "NT"]
    
    # Generate random dates over the last 2 years
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=730)  # 2 years
    days_range = (end_date - start_date).days
    
    # Create sample data for 1000 MRSA isolates
    n_samples = 1000
    
    # Generate dates
    dates = [start_date + timedelta(days=np.random.randint(0, days_range)) for _ in range(n_samples)]
    
    # Generate country data with weighted distribution
    country_weights = {
        "United States": 0.2,
        "United Kingdom": 0.15,
        "Germany": 0.1,
        "France": 0.08,
        "Italy": 0.07,
        "Spain": 0.06,
        "Japan": 0.05,
        "China": 0.07,
        "Australia": 0.04,
        "Brazil": 0.04,
        "India": 0.05,
        "South Africa": 0.03,
        "Canada": 0.03,
        "Russia": 0.02,
        "Hungary": 0.01
    }
    
    country_list = list(country_weights.keys())
    country_probabilities = list(country_weights.values())
    
    # Generate countries
    selected_countries = np.random.choice(country_list, n_samples, p=country_probabilities)
    
    # Generate coordinates based on countries
    latitudes = []
    longitudes = []
    
    for country in selected_countries:
        base_lat, base_lon = countries[country]
        # Add some random noise to coordinates
        lat = base_lat + np.random.normal(0, 1.0)
        lon = base_lon + np.random.normal(0, 1.0)
        latitudes.append(lat)
        longitudes.append(lon)
    
    # Generate lineages with weighted distribution
    lineage_weights = [0.25, 0.2, 0.15, 0.1, 0.08, 0.08, 0.05, 0.04, 0.03, 0.02]
    selected_lineages = np.random.choice(lineages, n_samples, p=lineage_weights)
    
    # Generate SCCmec types with weighted distribution
    sccmec_weights = [0.05, 0.25, 0.1, 0.4, 0.15, 0.05]
    selected_sccmec = np.random.choice(sccmec_types, n_samples, p=sccmec_weights)
    
    # Generate biofilm risk scores - make them correlated with lineage
    lineage_risk_base = {
        "ST5": 0.7,
        "ST8": 0.85,
        "ST22": 0.6,
        "ST36": 0.75,
        "ST45": 0.65,
        "ST239": 0.9,
        "ST398": 0.8,
        "ST15": 0.5,
        "ST80": 0.7,
        "ST97": 0.6
    }
    
    biofilm_risk_scores = []
    for lineage in selected_lineages:
        base_risk = lineage_risk_base[lineage]
        # Add some random noise
        risk = base_risk + np.random.normal(0, 0.1)
        # Ensure risk is between 0 and 1
        risk = max(0.1, min(1.0, risk))
        biofilm_risk_scores.append(risk)
    
    # Create DataFrame
    data = pd.DataFrame({
        "isolate_id": [f"MRSA_{i:04d}" for i in range(1, n_samples + 1)],
        "date": dates,
        "country": selected_countries,
        "latitude": latitudes,
        "longitude": longitudes,
        "lineage": selected_lineages,
        "sccmec_type": selected_sccmec,
        "biofilm_risk_score": biofilm_risk_scores,
        "mge_profile": [f"profile_{np.random.randint(1, 20)}" for _ in range(n_samples)]
    })
    
    return data

def load_sample_phage_data():
    """
    Load sample phage and antibiofilm peptide data.
    
    Returns:
        dict: Dictionary with sample phage and peptide data
    """
    # Generate sample phage data
    phage_data = {
        "phages": [
            {
                "id": "vB_SauM-C1",
                "name": "vB_SauM-C1",
                "target": "Cell Wall",
                "coverage": {
                    "ST5": 0.89,
                    "ST8": 0.76,
                    "ST22": 0.45,
                    "ST36": 0.67,
                    "ST45": 0.32,
                    "ST239": 0.91,
                    "ST398": 0.85
                }
            },
            {
                "id": "vB_SauP-S24",
                "name": "vB_SauP-S24",
                "target": "Biofilm EPS",
                "coverage": {
                    "ST5": 0.76,
                    "ST8": 0.82,
                    "ST22": 0.79,
                    "ST36": 0.45,
                    "ST45": 0.67,
                    "ST239": 0.58,
                    "ST398": 0.71
                }
            },
            {
                "id": "vB_SauM-K2",
                "name": "vB_SauM-K2",
                "target": "Surface Proteins",
                "coverage": {
                    "ST5": 0.92,
                    "ST8": 0.88,
                    "ST22": 0.65,
                    "ST36": 0.72,
                    "ST45": 0.81,
                    "ST239": 0.77,
                    "ST398": 0.69
                }
            },
            {
                "id": "vB_SauM-T4",
                "name": "vB_SauM-T4",
                "target": "Cell Membrane",
                "coverage": {
                    "ST5": 0.67,
                    "ST8": 0.91,
                    "ST22": 0.58,
                    "ST36": 0.83,
                    "ST45": 0.75,
                    "ST239": 0.62,
                    "ST398": 0.59
                }
            },
            {
                "id": "vB_SauP-P17",
                "name": "vB_SauP-P17",
                "target": "ica Operon",
                "coverage": {
                    "ST5": 0.78,
                    "ST8": 0.65,
                    "ST22": 0.81,
                    "ST36": 0.59,
                    "ST45": 0.88,
                    "ST239": 0.72,
                    "ST398": 0.68
                }
            }
        ],
        "peptides": [
            {
                "id": "ABP-01",
                "name": "LL-37 Derivative",
                "target": "Cell Membrane",
                "coverage": {
                    "ST5": 0.85,
                    "ST8": 0.79,
                    "ST22": 0.82,
                    "ST36": 0.76,
                    "ST45": 0.81,
                    "ST239": 0.78,
                    "ST398": 0.83
                }
            },
            {
                "id": "ABP-02",
                "name": "1018-Derivative",
                "target": "Biofilm Matrix",
                "coverage": {
                    "ST5": 0.92,
                    "ST8": 0.87,
                    "ST22": 0.78,
                    "ST36": 0.85,
                    "ST45": 0.79,
                    "ST239": 0.91,
                    "ST398": 0.88
                }
            },
            {
                "id": "ABP-03",
                "name": "DJK-5",
                "target": "Stringent Response",
                "coverage": {
                    "ST5": 0.76,
                    "ST8": 0.91,
                    "ST22": 0.85,
                    "ST36": 0.79,
                    "ST45": 0.88,
                    "ST239": 0.82,
                    "ST398": 0.77
                }
            },
            {
                "id": "ABP-04",
                "name": "Polycationic Peptide",
                "target": "EPS",
                "coverage": {
                    "ST5": 0.88,
                    "ST8": 0.83,
                    "ST22": 0.76,
                    "ST36": 0.91,
                    "ST45": 0.72,
                    "ST239": 0.84,
                    "ST398": 0.79
                }
            }
        ]
    }
    
    return phage_data
