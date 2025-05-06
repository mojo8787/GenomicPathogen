import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import networkx as nx

def plot_sample_phylogeny():
    """
    Create a sample phylogenetic tree visualization of MRSA strains.
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure with phylogenetic tree
    """
    # Create sample tree data
    np.random.seed(42)
    
    # Define lineages
    lineages = ["ST5", "ST8", "ST22", "ST36", "ST45", "ST239", "ST398"]
    
    # Create nodes
    nodes = []
    for lineage in lineages:
        # Add lineage as main node
        nodes.append({
            "id": lineage,
            "label": lineage,
            "level": 0,
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
                "label": strain_id,
                "parent": lineage,
                "level": 1,
                "biofilm_risk": biofilm_risk
            })
    
    # Convert to DataFrame
    nodes_df = pd.DataFrame(nodes)
    
    # Create edges
    edges = []
    for node in nodes:
        if "parent" in node:
            edges.append({
                "source": node["parent"],
                "target": node["id"]
            })
    
    # Convert to DataFrame
    edges_df = pd.DataFrame(edges)
    
    # Create network layout
    G = nx.Graph()
    
    # Add nodes
    for _, node in nodes_df.iterrows():
        G.add_node(node["id"])
    
    # Add edges
    for _, edge in edges_df.iterrows():
        G.add_edge(edge["source"], edge["target"])
    
    # Create layout
    pos = nx.spring_layout(G, seed=42)
    
    # Extract x and y coordinates
    node_x = []
    node_y = []
    node_ids = []
    node_levels = []
    node_biofilm_risks = []
    
    for node_id in G.nodes():
        node_data = nodes_df[nodes_df["id"] == node_id].iloc[0]
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)
        node_ids.append(node_id)
        node_levels.append(node_data["level"])
        node_biofilm_risks.append(node_data["biofilm_risk"])
    
    # Create a DataFrame for the nodes
    node_trace_df = pd.DataFrame({
        "x": node_x,
        "y": node_y,
        "id": node_ids,
        "level": node_levels,
        "biofilm_risk": node_biofilm_risks
    })
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_trace_df["x"],
        y=node_trace_df["y"],
        mode="markers+text",
        text=node_trace_df["id"],
        textposition="top center",
        marker=dict(
            color=node_trace_df["biofilm_risk"],
            colorscale="Reds",
            size=15,
            colorbar=dict(title="Biofilm Risk")
        ),
        hovertemplate="Strain: %{text}<br>Biofilm Risk: %{marker.color:.2f}<extra></extra>"
    )
    
    # Create edge traces
    edge_x = []
    edge_y = []
    
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        
        source_pos = pos[source]
        target_pos = pos[target]
        
        edge_x.append(source_pos[0])
        edge_x.append(target_pos[0])
        edge_x.append(None)
        
        edge_y.append(source_pos[1])
        edge_y.append(target_pos[1])
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=1, color="#888"),
        hoverinfo="none"
    )
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title="MRSA Phylogenetic Tree with Biofilm Risk Scores",
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def plot_regulatory_network(network_type="Full network", highlight_node=None, show_labels=True):
    """
    Plot a regulatory network for MRSA biofilm formation.
    
    Args:
        network_type (str): Type of network to display.
        highlight_node (str): Node to highlight.
        show_labels (bool): Whether to show node labels.
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure with network visualization
    """
    # Create sample regulatory network
    nodes = [
        {"id": "sarA", "type": "regulator", "color": "#ff4d4d"},
        {"id": "agr", "type": "regulator", "color": "#ff4d4d"},
        {"id": "ica", "type": "target", "color": "#4da6ff"},
        {"id": "fnbA", "type": "target", "color": "#4da6ff"},
        {"id": "clfA", "type": "target", "color": "#4da6ff"},
        {"id": "sigB", "type": "regulator", "color": "#ff4d4d"},
        {"id": "saeRS", "type": "regulator", "color": "#ff4d4d"},
        {"id": "rot", "type": "regulator", "color": "#ff4d4d"},
        {"id": "spa", "type": "target", "color": "#4da6ff"},
        {"id": "hla", "type": "target", "color": "#4da6ff"},
        {"id": "SCCmec", "type": "MGE", "color": "#4dff4d"},
        {"id": "phiSa3_int", "type": "MGE", "color": "#4dff4d"},
        {"id": "ACME", "type": "MGE", "color": "#4dff4d"}
    ]
    
    edges = [
        {"source": "sarA", "target": "ica", "type": "activation", "color": "#00cc00", "width": 2.0},
        {"source": "sarA", "target": "fnbA", "type": "activation", "color": "#00cc00", "width": 1.5},
        {"source": "sarA", "target": "clfA", "type": "activation", "color": "#00cc00", "width": 1.5},
        {"source": "agr", "target": "sarA", "type": "repression", "color": "#cc0000", "width": 1.0},
        {"source": "agr", "target": "rot", "type": "repression", "color": "#cc0000", "width": 2.0},
        {"source": "agr", "target": "hla", "type": "activation", "color": "#00cc00", "width": 2.5},
        {"source": "rot", "target": "spa", "type": "activation", "color": "#00cc00", "width": 1.5},
        {"source": "sigB", "target": "sarA", "type": "activation", "color": "#00cc00", "width": 1.0},
        {"source": "sigB", "target": "ica", "type": "activation", "color": "#00cc00", "width": 0.5},
        {"source": "saeRS", "target": "fnbA", "type": "activation", "color": "#00cc00", "width": 1.0},
        {"source": "phiSa3_int", "target": "agr", "type": "modulation", "color": "#aaaaaa", "width": 1.0},
        {"source": "SCCmec", "target": "sarA", "type": "modulation", "color": "#aaaaaa", "width": 0.8},
        {"source": "ACME", "target": "ica", "type": "activation", "color": "#00cc00", "width": 1.2}
    ]
    
    # Filter based on network type
    if network_type == "Core regulators only":
        # Filter out MGE nodes
        filtered_nodes = [node for node in nodes if node["type"] != "MGE"]
        node_ids = [node["id"] for node in filtered_nodes]
        filtered_edges = [edge for edge in edges if edge["source"] in node_ids and edge["target"] in node_ids]
        
        nodes = filtered_nodes
        edges = filtered_edges
    elif network_type == "MGE interactions":
        # Keep only edges involving MGEs
        mge_nodes = [node["id"] for node in nodes if node["type"] == "MGE"]
        filtered_edges = [edge for edge in edges if edge["source"] in mge_nodes or edge["target"] in mge_nodes]
        
        # Keep nodes involved in these edges
        involved_nodes = set()
        for edge in filtered_edges:
            involved_nodes.add(edge["source"])
            involved_nodes.add(edge["target"])
        
        filtered_nodes = [node for node in nodes if node["id"] in involved_nodes]
        
        nodes = filtered_nodes
        edges = filtered_edges
    
    # Highlight selected node
    if highlight_node:
        for node in nodes:
            if node["id"] == highlight_node:
                node["size"] = 15
                node["line_width"] = 2
                node["line_color"] = "#000000"
            else:
                node["size"] = 10
                node["line_width"] = 0.5
                node["line_color"] = "#ffffff"
        
        # Highlight connected edges
        for edge in edges:
            if edge["source"] == highlight_node or edge["target"] == highlight_node:
                edge["highlight"] = True
                edge["width"] *= 2
            else:
                edge["highlight"] = False
    else:
        for node in nodes:
            node["size"] = 10
            node["line_width"] = 0.5
            node["line_color"] = "#ffffff"
    
    # Create network layout
    G = nx.DiGraph()
    
    # Add nodes and edges
    for node in nodes:
        G.add_node(node["id"])
    
    for edge in edges:
        G.add_edge(edge["source"], edge["target"])
    
    # Create layout
    pos = nx.spring_layout(G, seed=42, k=0.5)
    
    # Create edge traces
    edge_traces = []
    
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        
        if source not in pos or target not in pos:
            continue
        
        source_pos = pos[source]
        target_pos = pos[target]
        
        edge_x = [source_pos[0], target_pos[0]]
        edge_y = [source_pos[1], target_pos[1]]
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(
                width=edge["width"],
                color=edge["color"]
            ),
            hoverinfo="none"
        )
        
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_x = []
    node_y = []
    node_colors = []
    node_sizes = []
    node_line_widths = []
    node_line_colors = []
    node_text = []
    
    for node in nodes:
        if node["id"] not in pos:
            continue
            
        x, y = pos[node["id"]]
        node_x.append(x)
        node_y.append(y)
        node_colors.append(node["color"])
        node_sizes.append(node["size"])
        node_line_widths.append(node["line_width"])
        node_line_colors.append(node["line_color"])
        node_text.append(node["id"])
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text" if show_labels else "markers",
        marker=dict(
            color=node_colors,
            size=node_sizes,
            line=dict(
                width=node_line_widths,
                color=node_line_colors
            )
        ),
        text=node_text,
        textposition="top center",
        hovertemplate="%{text}<extra></extra>"
    )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])
    
    # Update layout
    title = "MRSA Biofilm Regulatory Network"
    if network_type != "Full network":
        title += f" - {network_type}"
    if highlight_node:
        title += f" (Highlighting: {highlight_node})"
    
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    # Add arrow annotations for directed edges
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        
        if source not in pos or target not in pos:
            continue
            
        source_pos = pos[source]
        target_pos = pos[target]
        
        # Calculate midpoint
        mid_x = (source_pos[0] + target_pos[0]) / 2
        mid_y = (source_pos[1] + target_pos[1]) / 2
        
        # Calculate direction vector
        dx = target_pos[0] - source_pos[0]
        dy = target_pos[1] - source_pos[1]
        
        # Normalize
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            dx /= length
            dy /= length
        
        # Add annotation
        fig.add_annotation(
            x=mid_x + dx * 0.03,
            y=mid_y + dy * 0.03,
            ax=mid_x - dx * 0.03,
            ay=mid_y - dy * 0.03,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=edge["color"]
        )
    
    return fig
