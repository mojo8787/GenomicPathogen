import pandas as pd
import numpy as np

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

def get_feature_importance():
    """
    Get sample feature importance data.
    
    Returns:
        pandas.DataFrame: Dataframe with feature importance data
    """
    # Generate sample feature importance data
    np.random.seed(42)
    
    # Define feature categories
    categories = ["MGE", "SCCmec", "Core Regulator", "Adhesin", "Surface Protein", "Metabolic"]
    
    # Define features
    features = [
        # MGEs
        {"feature": "SCCmec_type_II", "category": "SCCmec", "importance": 0.152},
        {"feature": "SCCmec_type_IV", "category": "SCCmec", "importance": 0.098},
        {"feature": "ACME_presence", "category": "MGE", "importance": 0.142},
        {"feature": "phiSa3_integration", "category": "MGE", "importance": 0.127},
        {"feature": "pSK41_presence", "category": "MGE", "importance": 0.062},
        
        # Core regulators
        {"feature": "sarA_allele1", "category": "Core Regulator", "importance": 0.085},
        {"feature": "sarA_allele2", "category": "Core Regulator", "importance": 0.074},
        {"feature": "agr_group_I", "category": "Core Regulator", "importance": 0.065},
        {"feature": "agr_group_II", "category": "Core Regulator", "importance": 0.043},
        {"feature": "sigB_mutation", "category": "Core Regulator", "importance": 0.079},
        {"feature": "rot_mutation", "category": "Core Regulator", "importance": 0.038},
        {"feature": "saeRS_variant", "category": "Core Regulator", "importance": 0.045},
        
        # Adhesins
        {"feature": "ica_operon_complete", "category": "Adhesin", "importance": 0.112},
        {"feature": "ica_deletion", "category": "Adhesin", "importance": 0.076},
        {"feature": "fnbA_allele1", "category": "Adhesin", "importance": 0.058},
        {"feature": "fnbB_presence", "category": "Adhesin", "importance": 0.042},
        {"feature": "clfA_variant", "category": "Adhesin", "importance": 0.047},
        {"feature": "clfB_variant", "category": "Adhesin", "importance": 0.035},
        
        # Surface proteins
        {"feature": "spa_deletion", "category": "Surface Protein", "importance": 0.032},
        {"feature": "spa_repeat_number", "category": "Surface Protein", "importance": 0.025},
        {"feature": "protein_A_variant", "category": "Surface Protein", "importance": 0.031},
        
        # Metabolic
        {"feature": "arcA_presence", "category": "Metabolic", "importance": 0.046},
        {"feature": "speG_presence", "category": "Metabolic", "importance": 0.037},
        {"feature": "arginine_deiminase", "category": "Metabolic", "importance": 0.028},
        {"feature": "urease_operon_variant", "category": "Metabolic", "importance": 0.023}
    ]
    
    # Create DataFrame
    feature_df = pd.DataFrame(features)
    
    # Add some random noise to importances
    feature_df["importance"] = feature_df["importance"] + np.random.normal(0, 0.005, len(feature_df))
    
    # Ensure importance values are positive
    feature_df["importance"] = np.maximum(0.01, feature_df["importance"])
    
    return feature_df
