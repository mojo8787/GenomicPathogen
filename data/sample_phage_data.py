import pandas as pd
import numpy as np

def generate_sample_phage_data():
    """
    Generate sample phage and antibiofilm peptide data.
    
    Returns:
        dict: Dictionary with sample phage and peptide data
    """
    # Generate sample phage data
    np.random.seed(42)
    
    # Define MRSA lineages
    lineages = ["ST5", "ST8", "ST22", "ST36", "ST45", "ST239", "ST398"]
    
    # Define phages
    phages = [
        {
            "id": "vB_SauM-C1",
            "name": "vB_SauM-C1",
            "target": "Cell Wall",
            "coverage": {}
        },
        {
            "id": "vB_SauP-S24",
            "name": "vB_SauP-S24",
            "target": "Biofilm EPS",
            "coverage": {}
        },
        {
            "id": "vB_SauM-K2",
            "name": "vB_SauM-K2",
            "target": "Surface Proteins",
            "coverage": {}
        },
        {
            "id": "vB_SauM-T4",
            "name": "vB_SauM-T4",
            "target": "Cell Membrane",
            "coverage": {}
        },
        {
            "id": "vB_SauP-P17",
            "name": "vB_SauP-P17",
            "target": "ica Operon",
            "coverage": {}
        }
    ]
    
    # Define antibiofilm peptides
    peptides = [
        {
            "id": "ABP-01",
            "name": "LL-37 Derivative",
            "target": "Cell Membrane",
            "coverage": {}
        },
        {
            "id": "ABP-02",
            "name": "1018-Derivative",
            "target": "Biofilm Matrix",
            "coverage": {}
        },
        {
            "id": "ABP-03",
            "name": "DJK-5",
            "target": "Stringent Response",
            "coverage": {}
        },
        {
            "id": "ABP-04",
            "name": "Polycationic Peptide",
            "target": "EPS",
            "coverage": {}
        }
    ]
    
    # Generate random coverage values for phages
    for phage in phages:
        for lineage in lineages:
            # Generate a random coverage value between 0.3 and 0.95
            coverage = np.random.uniform(0.3, 0.95)
            phage["coverage"][lineage] = coverage
    
    # Generate random coverage values for peptides
    for peptide in peptides:
        for lineage in lineages:
            # Generate a random coverage value between 0.5 and 0.95
            # Peptides generally have broader spectrum
            coverage = np.random.uniform(0.5, 0.95)
            peptide["coverage"][lineage] = coverage
    
    # Create a dictionary with phage and peptide data
    phage_data = {
        "phages": phages,
        "peptides": peptides
    }
    
    return phage_data

# Generate sample phage data
sample_phage_data = generate_sample_phage_data()
