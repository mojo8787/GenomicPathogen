import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_mrsa_data():
    """
    Generate sample MRSA data with biofilm formation measurements.
    
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
    
    # Generate sample dates over the last year
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)  # 1 year
    days_range = (end_date - start_date).days
    dates = [start_date + timedelta(days=np.random.randint(0, days_range)) for _ in range(n_samples)]
    
    # Generate sample countries
    countries = ["United States", "United Kingdom", "Germany", "France", "Italy", 
                "Spain", "Japan", "China", "Australia", "Brazil", "Hungary"]
    
    # Create DataFrame
    data = pd.DataFrame({
        "isolate_id": [f"MRSA_{i:04d}" for i in range(1, n_samples + 1)],
        "date": dates,
        "country": np.random.choice(countries, n_samples),
        "lineage": np.random.choice(["ST5", "ST8", "ST22", "ST36", "ST45", "ST239", "ST398"], n_samples),
        "sccmec_type": np.random.choice(["I", "II", "III", "IV", "V"], n_samples),
        "biofilm_od590": biofilm_od590,
        "is_high_biofilm": biofilm_od590 > 0.3
    })
    
    # Add some correlations between lineage and biofilm formation
    # ST239 and ST8 lineages have higher biofilm formation
    for i, row in data.iterrows():
        if row["lineage"] in ["ST239", "ST8"]:
            data.at[i, "biofilm_od590"] = row["biofilm_od590"] * 1.2 + 0.1
        
        # Update high biofilm flag
        data.at[i, "is_high_biofilm"] = data.at[i, "biofilm_od590"] > 0.3
    
    return data

# Generate and save sample MRSA data
sample_mrsa_data = generate_sample_mrsa_data()
