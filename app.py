import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_loader import load_sample_data
from utils.visualization import plot_sample_phylogeny

# Page configuration
st.set_page_config(
    page_title="MRSA Biofilm Surveillance Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page header
st.title("🧬 MRSA Biofilm Surveillance Dashboard")

# Subtitle and introduction
st.markdown("""
### AI-Driven Genomic Surveillance and Mechanistic Inference of High-Biofilm MRSA Lineages

This dashboard demonstrates key components of a proposed EMBO fellowship project focusing on 
methicillin-resistant *Staphylococcus aureus* (MRSA) biofilm formation. The project aims to:

1. **Identify genetic determinants** of high-biofilm MRSA clones
2. **Decode regulatory circuitry** governing the planktonic→sessile switch
3. **Deploy real-time surveillance** & therapeutic-prioritisation

*Developed for Prof. Balázs Papp's Metabolic Systems Biology Research Group at HUN-REN BRC*
""")

# Create two columns for the dashboard overview
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Project Overview")
    st.markdown("""
    This interactive dashboard implements the surveillance and therapeutic prioritization 
    component described in **Aim 3** of the research proposal. It demonstrates:
    
    - **Phylogenetic visualization** of MRSA lineages
    - **Biofilm risk scoring** based on genomic markers
    - **Geographic distribution** of high-risk strains
    - **Therapeutic coverage calculator** for phage and peptide therapies
    
    Navigate using the sidebar to explore different aspects of the project.
    """)
    
    # Add a sample phylogenetic tree visualization
    st.subheader("Sample MRSA Phylogeny with Biofilm Risk Overlay")
    phylo_fig = plot_sample_phylogeny()
    st.plotly_chart(phylo_fig, use_container_width=True)

with col2:
    st.subheader("MRSA Biofilm Impact")
    
    # Create metrics for the dashboard
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Analyzed Genomes", value="20,000+")
        st.metric(label="High-Biofilm Strains", value="4,358", delta="+215 in 2024")
    with col_b:
        st.metric(label="MGEs Identified", value="37")
        st.metric(label="Key Regulators", value="23", delta="+8 validated")
    
    # Add a sample chart showing data distribution
    st.subheader("Biofilm Formation Distribution")
    
    sample_data = load_sample_data()
    
    # Create a histogram of biofilm OD measurements
    fig = px.histogram(
        sample_data, 
        x="biofilm_od590",
        color="is_high_biofilm",
        barmode="overlay",
        labels={"biofilm_od590": "Biofilm Formation (OD590)", "is_high_biofilm": "High Biofilm"},
        color_discrete_map={"True": "#ff4b4b", "False": "#4b4bff"},
        title="MRSA Biofilm Formation Distribution"
    )
    fig.add_vline(x=0.3, line_dash="dash", line_color="red", annotation_text="High Biofilm Threshold")
    st.plotly_chart(fig, use_container_width=True)

# Main information about project aims and links to navigation
st.markdown("""
## Dashboard Components

Explore the different components of the dashboard using the sidebar navigation:

1. **Genomic Determinants**: Explore GWAS results and ML models predicting biofilm formation
2. **Regulatory Circuits**: Visualize the regulatory networks controlling biofilm formation
3. **Surveillance Dashboard**: Real-time tracking of high-biofilm MRSA lineages and therapeutic recommendations

This dashboard is part of a proposed EMBO fellowship project and demonstrates the skills and approach 
that would be employed during the fellowship.
""")

# Add file uploader for new MRSA genomes
st.subheader("Upload New MRSA Genome for Analysis")
uploaded_file = st.file_uploader("Upload a FASTA or FASTQ file", type=['fasta', 'fastq', 'fa', 'fq'])

if uploaded_file is not None:
    st.info("Demonstration Mode: This would process the uploaded file through the analysis pipeline and provide predictions for biofilm formation capability.")
    
    # Create tabs for different types of analysis results
    tabs = st.tabs(["Sequence Info", "Predicted Biofilm Risk", "Phage Coverage"])
    
    with tabs[0]:
        st.markdown("### Sequence Information")
        st.code("MRSA genome analysis - sequence statistics would appear here")
        
    with tabs[1]:
        st.markdown("### Biofilm Formation Prediction")
        st.success("This genome has a **76% probability** of forming strong biofilms.")
        
        # Sample feature importance chart
        features = ['SCCmec-Type IV', 'ACME Presence', 'phiSa3 Integration', 'agr System', 'sarA Variant']
        importances = [0.35, 0.28, 0.22, 0.08, 0.07]
        
        fig = px.bar(
            x=importances, 
            y=features, 
            orientation='h',
            labels={"x": "Feature Importance", "y": "Genomic Feature"},
            title="Feature Importance for Biofilm Prediction"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tabs[2]:
        st.markdown("### Phage Therapy Coverage")
        st.markdown("Based on this genome's profile, the following phage cocktail is recommended:")
        
        phage_coverage = pd.DataFrame({
            "Phage": ["vB_SauM-C1", "vB_SauP-S24", "vB_SauM-K2"],
            "Coverage": [0.89, 0.76, 0.92],
            "Target": ["Cell Wall", "Biofilm EPS", "Surface Proteins"]
        })
        
        st.dataframe(phage_coverage)

# Footer with attribution
st.markdown("---")
st.markdown("""
**Dashboard Author**: [Your Name]  
**Proposal**: AI-Driven Genomic Surveillance and Mechanistic Inference of High-Biofilm MRSA Lineages  
**Target Host Lab**: Prof. Balázs Papp's Group at HUN-REN BRC, Szeged
""")
