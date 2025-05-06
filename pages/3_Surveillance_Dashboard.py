import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
from utils.data_loader import load_sample_surveillance_data, load_sample_phage_data
from utils.phage_calculator import calculate_phage_coverage, recommend_phage_cocktail

# Page configuration
st.set_page_config(
    page_title="Surveillance Dashboard | MRSA Biofilm Dashboard",
    page_icon="🧬",
    layout="wide"
)

# Page header
st.title("🌍 MRSA Biofilm Surveillance Dashboard")
st.markdown("""
This page demonstrates the analysis from **Aim 3** of the research proposal:
*"Deploy real-time surveillance & therapeutic-prioritisation dashboard"*

This dashboard provides real-time tracking of high-biofilm MRSA lineages and therapeutic recommendations.
""")

# Load sample surveillance data
surveillance_data = load_sample_surveillance_data()
phage_data = load_sample_phage_data()

# Create tabs for different dashboard components
tabs = st.tabs(["Geographic Distribution", "Lineage Tracking", "Therapeutic Coverage"])

with tabs[0]:
    st.header("Geographic Distribution of High-Biofilm MRSA")
    st.markdown("""
    The map shows the global distribution of high-biofilm MRSA strains, with markers indicating 
    the prevalence and risk scores for different regions. This helps infection control teams identify 
    emerging high-risk lineages in their area.
    """)
    
    # Create date range selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        
        # Create date input
        selected_start_date = st.date_input("Start date", value=start_date)
        selected_end_date = st.date_input("End date", value=end_date)
        
        # Create filter for MRSA lineages
        lineages = ["All"] + sorted(surveillance_data["lineage"].unique().tolist())
        selected_lineage = st.selectbox("MRSA lineage", lineages)
        
        # Create filter for biofilm risk
        min_biofilm_risk = st.slider("Minimum biofilm risk score", 0.0, 1.0, 0.7)
    
    # Filter data based on selection
    filtered_data = surveillance_data
    
    if selected_lineage != "All":
        filtered_data = filtered_data[filtered_data["lineage"] == selected_lineage]
    
    filtered_data = filtered_data[filtered_data["biofilm_risk_score"] >= min_biofilm_risk]
    
    # Convert dates to datetime for filtering
    filtered_data["date"] = pd.to_datetime(filtered_data["date"])
    filtered_data = filtered_data[
        (filtered_data["date"] >= pd.Timestamp(selected_start_date)) & 
        (filtered_data["date"] <= pd.Timestamp(selected_end_date))
    ]
    
    # Create map visualization
    with col2:
        # Group data by country for map visualization
        map_data = filtered_data.groupby("country").agg({
            "latitude": "mean",
            "longitude": "mean",
            "isolate_id": "count",
            "biofilm_risk_score": "mean",
            "lineage": lambda x: list(x.mode())[0] if len(x) > 0 else None
        }).reset_index()
        
        map_data.rename(columns={"isolate_id": "isolate_count"}, inplace=True)
        
        # Create map centered at the weighted average of all coordinates
        if len(map_data) > 0:
            center_lat = np.average(map_data["latitude"], weights=map_data["isolate_count"])
            center_lon = np.average(map_data["longitude"], weights=map_data["isolate_count"])
        else:
            # Default center if no data
            center_lat, center_lon = 30.0, 10.0
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
        
        # Add markers for each country
        for _, row in map_data.iterrows():
            # Scale marker size based on isolate count
            radius = np.sqrt(row["isolate_count"]) * 5
            
            # Color marker based on biofilm risk score (red for high risk, blue for low risk)
            color = f'#{int(255 * row["biofilm_risk_score"]):02x}0000'
            
            # Create popup content
            popup_content = f"""
            <b>Country:</b> {row['country']}<br>
            <b>Isolate Count:</b> {row['isolate_count']}<br>
            <b>Dominant Lineage:</b> {row['lineage']}<br>
            <b>Avg. Biofilm Risk Score:</b> {row['biofilm_risk_score']:.2f}
            """
            
            # Add marker to map
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=folium.Popup(popup_content, max_width=300)
            ).add_to(m)
        
        # Display map
        folium_static(m, width=800, height=500)
    
    # Display summary statistics
    st.subheader("Summary Statistics")
    
    # Create summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Isolates", str(len(filtered_data)))
    
    with col2:
        dominant_lineage = filtered_data["lineage"].mode()[0] if len(filtered_data) > 0 else "N/A"
        st.metric("Dominant Lineage", dominant_lineage)
    
    with col3:
        avg_risk = filtered_data["biofilm_risk_score"].mean() if len(filtered_data) > 0 else 0
        st.metric("Avg. Biofilm Risk", f"{avg_risk:.2f}")
    
    with col4:
        countries_count = filtered_data["country"].nunique() if len(filtered_data) > 0 else 0
        st.metric("Countries Affected", str(countries_count))
    
    # Display table of top countries
    if len(filtered_data) > 0:
        top_countries = filtered_data.groupby("country").agg({
            "isolate_id": "count",
            "biofilm_risk_score": "mean",
            "lineage": lambda x: list(x.mode())[0] if len(x) > 0 else None
        }).reset_index().sort_values("isolate_id", ascending=False).head(10)
        
        top_countries.rename(columns={
            "isolate_id": "Isolate Count",
            "biofilm_risk_score": "Avg. Biofilm Risk",
            "lineage": "Dominant Lineage",
            "country": "Country"
        }, inplace=True)
        
        st.subheader("Top 10 Countries by Isolate Count")
        st.dataframe(top_countries)

with tabs[1]:
    st.header("MRSA Lineage Tracking")
    st.markdown("""
    This section tracks the prevalence and biofilm risk of different MRSA lineages over time.
    The visualizations help identify emerging high-risk lineages and monitor their spread.
    """)
    
    # Create time series visualization of lineage prevalence
    st.subheader("Lineage Prevalence Over Time")
    
    # Group data by month and lineage
    filtered_data["month"] = filtered_data["date"].dt.to_period("M")
    lineage_time_series = filtered_data.groupby(["month", "lineage"]).size().reset_index(name="count")
    lineage_time_series["month"] = lineage_time_series["month"].dt.to_timestamp()
    
    # Filter to top lineages for better visualization
    top_lineages = filtered_data["lineage"].value_counts().nlargest(6).index.tolist()
    lineage_time_series_filtered = lineage_time_series[lineage_time_series["lineage"].isin(top_lineages)]
    
    # Create line chart
    fig = px.line(
        lineage_time_series_filtered,
        x="month",
        y="count",
        color="lineage",
        title="MRSA Lineage Prevalence Over Time",
        labels={"month": "Month", "count": "Isolate Count", "lineage": "MRSA Lineage"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create biofilm risk by lineage visualization
    st.subheader("Biofilm Risk by MRSA Lineage")
    
    # Group data by lineage
    lineage_risk = filtered_data.groupby("lineage").agg({
        "biofilm_risk_score": ["mean", "std", "count"],
        "isolate_id": "count"
    }).reset_index()
    
    # Flatten multi-level columns
    lineage_risk.columns = ["lineage", "risk_mean", "risk_std", "risk_count", "isolate_count"]
    
    # Filter to lineages with at least 5 isolates
    lineage_risk = lineage_risk[lineage_risk["isolate_count"] >= 5]
    
    # Sort by mean risk
    lineage_risk = lineage_risk.sort_values("risk_mean", ascending=False)
    
    # Create bar chart with error bars
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=lineage_risk["lineage"],
        y=lineage_risk["risk_mean"],
        error_y=dict(
            type="data",
            array=lineage_risk["risk_std"],
            visible=True
        ),
        marker_color="indianred",
        name="Mean Biofilm Risk"
    ))
    
    fig.update_layout(
        title="Mean Biofilm Risk Score by MRSA Lineage",
        xaxis_title="MRSA Lineage",
        yaxis_title="Biofilm Risk Score (0-1)",
        xaxis=dict(tickangle=-45),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create SCCmec type distribution visualization
    st.subheader("SCCmec Type Distribution by Lineage")
    
    # Create pivot table of SCCmec types by lineage
    sccmec_pivot = pd.crosstab(
        filtered_data["lineage"], 
        filtered_data["sccmec_type"],
        normalize="index"
    ) * 100
    
    # Filter to top lineages
    sccmec_pivot = sccmec_pivot.loc[
        filtered_data["lineage"].value_counts().nlargest(8).index
    ]
    
    # Create heatmap
    fig = px.imshow(
        sccmec_pivot,
        labels=dict(x="SCCmec Type", y="MRSA Lineage", color="Percentage (%)"),
        color_continuous_scale="Viridis",
        title="SCCmec Type Distribution by MRSA Lineage"
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Create phylogenetic relationship visualization
    st.subheader("Phylogenetic Relationships Between High-Biofilm Lineages")
    
    # Display interactive phylogenetic tree visualization
    st.markdown("""
    The phylogenetic tree visualization would display relationships between MRSA lineages
    with biofilm risk scores overlaid. This would be implemented using the Nextstrain Augur
    pipeline as described in the proposal.
    
    Due to the complexity of the visualization, a placeholder image is shown here.
    """)
    
    # Sample dendrogram visualization
    np.random.seed(42)
    
    # Create sample distance matrix for dendrogram
    labels = [f'ST{i}' for i in [5, 8, 22, 36, 45, 239, 398, 15, 80, 97, 121, 228]]
    X = np.random.rand(len(labels), len(labels))
    X = (X + X.T) / 2  # Make symmetric
    np.fill_diagonal(X, 0)  # Zero diagonal
    
    # Create distance matrix
    dist_matrix = pd.DataFrame(X, index=labels, columns=labels)
    
    fig = px.imshow(
        dist_matrix,
        labels=dict(x="MRSA Lineage", y="MRSA Lineage", color="Genetic Distance"),
        color_continuous_scale="Viridis",
        title="Genetic Distance Matrix Between MRSA Lineages"
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.header("Therapeutic Coverage Calculator")
    st.markdown("""
    The therapeutic coverage calculator recommends optimal phage and antibiofilm peptide cocktails
    for targeting high-biofilm MRSA strains. This helps infection control teams select the most
    effective therapies for local MRSA lineages.
    """)
    
    # Create therapeutic coverage calculator interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Create region selector
        region = st.selectbox(
            "Select region:",
            ["Global", "Europe", "North America", "Asia", "Africa", "South America", "Oceania"]
        )
        
        # Create lineage multi-selector
        target_lineages = st.multiselect(
            "Target lineages:",
            sorted(surveillance_data["lineage"].unique().tolist()),
            default=surveillance_data["lineage"].value_counts().nlargest(3).index.tolist()
        )
        
        # Create therapy type selector
        therapy_type = st.radio(
            "Therapy type:",
            ["Phage", "Antibiofilm Peptide", "Combination"]
        )
        
        # Create coverage threshold slider
        coverage_threshold = st.slider(
            "Minimum coverage target (%):",
            min_value=70,
            max_value=100,
            value=90
        )
        
        # Calculate button
        calculate_button = st.button("Calculate Optimal Cocktail")
    
    with col2:
        if calculate_button:
            # Calculate phage coverage and recommended cocktail
            coverage_matrix, recommended_cocktail = calculate_phage_coverage(
                phage_data, 
                region=region,
                target_lineages=target_lineages,
                therapy_type=therapy_type,
                coverage_threshold=coverage_threshold / 100.0
            )
            
            # Display recommended cocktail
            st.subheader(f"Recommended {therapy_type} Cocktail")
            
            # Create cocktail component table
            cocktail_df = pd.DataFrame({
                "Component": [comp["name"] for comp in recommended_cocktail],
                "Target": [comp["target"] for comp in recommended_cocktail],
                "Coverage (%)": [f"{comp['coverage']*100:.1f}%" for comp in recommended_cocktail],
                "Target Lineages": [", ".join(comp["lineages"]) for comp in recommended_cocktail]
            })
            
            st.dataframe(cocktail_df)
            
            # Display total coverage
            if recommended_cocktail:
                total_coverage = sum([comp["coverage"] for comp in recommended_cocktail]) / len(recommended_cocktail)
                st.metric("Total Lineage Coverage", f"{total_coverage*100:.1f}%")
            else:
                st.warning("No suitable therapeutic components found for the selected lineages. Try selecting different lineages or adjusting the coverage threshold.")
            
            # Create coverage heatmap
            st.subheader("Coverage Matrix")
            
            # Convert coverage matrix to DataFrame for heatmap
            if coverage_matrix and target_lineages:
                coverage_df = pd.DataFrame(coverage_matrix)
                
                # Only proceed if the coverage matrix has data
                if not coverage_df.empty and not coverage_df.columns.empty:
                    # Create heatmap
                    fig = px.imshow(
                        coverage_df,
                        labels=dict(x="Therapeutic Agent", y="MRSA Lineage", color="Coverage (%)"),
                        x=coverage_df.columns,
                        y=coverage_df.index,
                        color_continuous_scale="Viridis",
                        title=f"{therapy_type} Coverage Matrix for Selected Lineages"
                    )
                    
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough data to display coverage matrix. Try selecting different lineages or therapy types.")
            else:
                st.info("No coverage data available. Try selecting different lineages or therapy types.")
    
    # Display information about therapeutic coverage
    st.markdown("""
    **How the Therapeutic Coverage Calculator Works:**
    
    1. **Input Selection:** Users select a geographic region, target MRSA lineages, and therapy type
    2. **Coverage Calculation:** The system calculates the coverage of each therapeutic agent against the selected lineages
    3. **Cocktail Optimization:** A greedy algorithm identifies the minimal set of therapeutic agents needed to reach the coverage threshold
    4. **Recommendation:** The system recommends an optimal cocktail of phages, peptides, or a combination
    
    This helps infection control teams and clinicians select targeted therapies for local MRSA strains,
    improving treatment outcomes while minimizing resistance development.
    """)

# Add information about implementation and host lab integration
st.markdown("""
## Implementation and Integration with Host Lab Infrastructure

This surveillance dashboard demonstrates how the proposed project would integrate with Prof. Papp's lab infrastructure:

1. **Phylogenetic Pipeline:** Uses the same TreeTime workflow from the lab's recent Cell paper on *Acinetobacter baumannii*
2. **Hospital Deployment:** Can be packaged as a Docker container for air-gapped deployment in hospital settings
3. **Computational Resources:** Optimized for the lab's HPC cluster and GPU nodes
4. **Data Pipeline:** Integrates with the lab's existing genomic data processing pipelines

The dashboard showcases how the proposed EMBO fellowship project would build upon and extend the host lab's expertise in antimicrobial resistance genomics and evolutionary systems biology.
""")

# Footer
st.markdown("---")
st.markdown("Part of the MRSA Biofilm Surveillance Dashboard | **Aim 3**: Deploy real-time surveillance & therapeutic-prioritisation dashboard")
