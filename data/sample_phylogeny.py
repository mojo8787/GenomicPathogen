import pandas as pd
import numpy as np
import json

def generate_sample_phylogeny():
    """
    Generate sample phylogenetic data for MRSA strains.
    
    Returns:
        dict: Dictionary with sample phylogenetic data
    """
    # Generate sample phylogenetic data
    np.random.seed(42)
    
    # Define lineages
    lineages = ["ST5", "ST8", "ST22", "ST36", "ST45", "ST239", "ST398"]
    
    # Create nodes
    nodes = []
    for lineage in lineages:
        # Add lineage as main node
        nodes.append({
            "id": lineage,
            "name": lineage,
            "level": 0,
            "parent": None,
            "biofilm_risk": np.random.uniform(0.6, 0.9)
        })
        
        # Add 3-5 strains per lineage
        n_strains = np.random.randint(3, 6)
        for i in range(n_strains):
            strain_id = f"{lineage}-{i+1}"
            biofilm_risk = np.random.normal(nodes[-1]["biofilm_risk"], 0.1)
            biofilm_risk = max(0.1, min(1.0, biofilm_risk))
            
            nodes.append({
                "id": strain_id,
                "name": strain_id,
                "parent": lineage,
                "level": 1,
                "biofilm_risk": biofilm_risk
            })
    
    # Create phylogenetic tree structure
    tree = {
        "nodes": nodes,
        "lineages": lineages
    }
    
    return tree

# Generate sample phylogeny
sample_phylogeny = generate_sample_phylogeny()
