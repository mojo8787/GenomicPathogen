import pandas as pd
import numpy as np

def calculate_phage_coverage(phage_data, region="Global", target_lineages=None, therapy_type="Phage", coverage_threshold=0.9):
    """
    Calculate phage and antibiofilm peptide coverage for MRSA lineages.
    
    Args:
        phage_data (dict): Dictionary with phage and peptide data
        region (str): Geographic region to filter by
        target_lineages (list): List of target MRSA lineages
        therapy_type (str): Type of therapy to consider (Phage, Antibiofilm Peptide, or Combination)
        coverage_threshold (float): Minimum coverage threshold (0-1)
    
    Returns:
        tuple: Coverage matrix and recommended cocktail components
    """
    # If no target lineages are provided, use all available lineages
    if target_lineages is None or len(target_lineages) == 0:
        # Get all lineages from the first phage's coverage
        if len(phage_data["phages"]) > 0:
            target_lineages = list(phage_data["phages"][0]["coverage"].keys())
        else:
            target_lineages = []
    
    # Create coverage matrix
    coverage_matrix = {}
    
    # Include phages if requested
    if therapy_type in ["Phage", "Combination"]:
        for phage in phage_data["phages"]:
            coverage_dict = {}
            for lineage in target_lineages:
                if lineage in phage["coverage"]:
                    coverage_dict[lineage] = phage["coverage"][lineage]
                else:
                    coverage_dict[lineage] = 0.0
            
            coverage_matrix[phage["name"]] = coverage_dict
    
    # Include peptides if requested
    if therapy_type in ["Antibiofilm Peptide", "Combination"]:
        for peptide in phage_data["peptides"]:
            coverage_dict = {}
            for lineage in target_lineages:
                if lineage in peptide["coverage"]:
                    coverage_dict[lineage] = peptide["coverage"][lineage]
                else:
                    coverage_dict[lineage] = 0.0
            
            coverage_matrix[peptide["name"]] = coverage_dict
    
    # Use a greedy algorithm to find minimal cocktail
    recommended_cocktail = recommend_phage_cocktail(
        coverage_matrix, 
        target_lineages, 
        coverage_threshold,
        therapy_type
    )
    
    return coverage_matrix, recommended_cocktail

def recommend_phage_cocktail(coverage_matrix, target_lineages, coverage_threshold=0.9, therapy_type="Phage"):
    """
    Recommend optimal phage or peptide cocktail to cover target lineages.
    
    Args:
        coverage_matrix (dict): Coverage matrix of therapeutic agents and lineages
        target_lineages (list): List of target MRSA lineages
        coverage_threshold (float): Minimum coverage threshold (0-1)
        therapy_type (str): Type of therapy (for naming and description)
    
    Returns:
        list: Recommended cocktail components
    """
    # Create a copy of the coverage matrix
    remaining_coverage = {}
    for agent, coverage in coverage_matrix.items():
        remaining_coverage[agent] = {}
        for lineage, value in coverage.items():
            remaining_coverage[agent][lineage] = value
    
    # Initialize selected components
    selected_components = []
    covered_lineages = set()
    
    # If no target lineages are provided, return empty list
    if not target_lineages:
        return []
    
    # Greedy algorithm - select components until we reach the coverage threshold
    # Ensure we don't enter an infinite loop if coverage cannot be improved
    max_iterations = len(coverage_matrix) + 1  # Set a maximum number of iterations
    iteration_count = 0
    
    while len(covered_lineages) < len(target_lineages) * coverage_threshold and iteration_count < max_iterations:
        iteration_count += 1
        # Find the component with the highest coverage of remaining lineages
        best_component = None
        best_coverage = 0
        best_coverage_lineages = []
        
        for agent, coverage in remaining_coverage.items():
            # Skip already selected components
            if any(comp["name"] == agent for comp in selected_components):
                continue
            
            # Calculate coverage for uncovered lineages
            uncovered_lineages = [lin for lin in target_lineages if lin not in covered_lineages]
            coverage_count = sum([1 for lin in uncovered_lineages if coverage.get(lin, 0) >= 0.7])
            
            if coverage_count > best_coverage:
                best_component = agent
                best_coverage = coverage_count
                best_coverage_lineages = [lin for lin in uncovered_lineages if coverage.get(lin, 0) >= 0.7]
        
        # If we can't improve coverage further, break
        if best_component is None or best_coverage == 0:
            break
        
        # Add the best component to the selected list
        if therapy_type == "Phage":
            # Find the phage in the original data
            for phage in phage_data["phages"]:
                if phage["name"] == best_component:
                    selected_components.append({
                        "name": best_component,
                        "target": phage["target"],
                        "coverage": sum([coverage_matrix[best_component].get(lin, 0) for lin in target_lineages]) / len(target_lineages),
                        "lineages": best_coverage_lineages
                    })
                    break
        elif therapy_type == "Antibiofilm Peptide":
            # Find the peptide in the original data
            for peptide in phage_data["peptides"]:
                if peptide["name"] == best_component:
                    selected_components.append({
                        "name": best_component,
                        "target": peptide["target"],
                        "coverage": sum([coverage_matrix[best_component].get(lin, 0) for lin in target_lineages]) / len(target_lineages),
                        "lineages": best_coverage_lineages
                    })
                    break
        else:  # Combination
            # Find in either phages or peptides
            component_found = False
            for phage in phage_data["phages"]:
                if phage["name"] == best_component:
                    selected_components.append({
                        "name": best_component,
                        "target": phage["target"],
                        "coverage": sum([coverage_matrix[best_component].get(lin, 0) for lin in target_lineages]) / len(target_lineages),
                        "lineages": best_coverage_lineages
                    })
                    component_found = True
                    break
            
            if not component_found:
                for peptide in phage_data["peptides"]:
                    if peptide["name"] == best_component:
                        selected_components.append({
                            "name": best_component,
                            "target": peptide["target"],
                            "coverage": sum([coverage_matrix[best_component].get(lin, 0) for lin in target_lineages]) / len(target_lineages),
                            "lineages": best_coverage_lineages
                        })
                        break
        
        # Update covered lineages
        covered_lineages.update(best_coverage_lineages)
    
    return selected_components

# Sample phage data for testing
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
        }
    ]
}
