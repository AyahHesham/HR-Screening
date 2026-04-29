# semantic_network.py - Fixed for Streamlit
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def draw_semantic_network():
    G = nx.DiGraph()
    
    # Nodes
    G.add_node("Qualified Candidate", color="#90EE90")
    G.add_node("Hold Candidate", color="#FFD700")
    G.add_node("Rejected Candidate", color="#FF9999")

    # Edges (from your presentation)
    G.add_edge("Qualified Candidate", "> 3 years experience")
    G.add_edge("Qualified Candidate", "Related Degree")
    G.add_edge("Qualified Candidate", "Strong Skills (Python/Java/SQL)")

    G.add_edge("Hold Candidate", "1-2 years experience")
    G.add_edge("Hold Candidate", "Demonstrated Potential")

    G.add_edge("Rejected Candidate", "< 1 year experience")
    G.add_edge("Rejected Candidate", "Insufficient Skills")
    G.add_edge("Rejected Candidate", "Unrelated Degree")

    # Draw the graph
    pos = nx.spring_layout(G, seed=42)
    colors = [G.nodes[n].get('color', 'lightblue') for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=3500, 
            font_size=9, font_weight="bold", arrows=True, ax=ax)
    
    plt.title("Semantic Network - HR Screening Knowledge Representation", fontsize=14, pad=20)
    
    # Show in Streamlit (this replaces plt.show())
    st.pyplot(fig)
    
    # Optional: Also save as image
    # plt.savefig("semantic_network.png")
    # st.image("semantic_network.png")