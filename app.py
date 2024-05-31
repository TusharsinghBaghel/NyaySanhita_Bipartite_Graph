import streamlit as st
from sentence_transformers import SentenceTransformer, util #Embedding model
import csv
import networkx as nx # A utility for creating graphs
import matplotlib.pyplot as plt  # for plotting
import pickle #Used pickle for storing the embeddings locally as .pkl file

csv_file_path = 'ns_sections_final.csv'
csv_file_path2 = 'IPC_sections_final.csv'

ns_sections = []
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        section_number = row[0]
        content = row[1]
        ns_sections.append((section_number, content))

#that means the index of section x of nyaysanhita is x-1
ipc_sections = []
with open(csv_file_path2, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        section_number = row[0]
        content = row[1]
        ipc_sections.append((section_number, content))


# ########### FOR CREATING NEW EMBEDDINGS ######################
# ns_content = [text for _, text in ns_sections]
# ipc_content = [text for _, text in ipc_sections]

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# ipc_embeddings = model.encode(ipc_content)
# ns_embeddings = model.encode(ns_content)

# with open('ipc_embeddings.pkl', 'wb') as f:
#     pickle.dump(ipc_embeddings, f)

# with open('ns_embeddings.pkl', 'wb') as f:
#     pickle.dump(ns_embeddings, f)


# Loading embeddings
with open('ipc_embeddings.pkl', 'rb') as f:
    ipc_embeddings = pickle.load(f)

with open('ns_embeddings.pkl', 'rb') as f:
    ns_embeddings = pickle.load(f)

# Streamlit app

# st.markdown("<h1 style='color:white; text-align:center; font-weight:bold;'>IPC to Bhartiya Nyay Sanhita</h1>", unsafe_allow_html=True)
st.markdown("""
    <h1 style='color:#ffffff; text-align:center; background-color:#333; padding:5px 15px; border-radius:10px; border:4px solid #4CAF50; margin-bottom:25px;'>
        Indian Penal Code to Bhartiya Nyay Sanhita
    </h1>""", unsafe_allow_html=True)

# # #CSS
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: #C7C9D3;
    }
    .stApp {
        background-color: #0E1117;
        color:white;
    }
    .css-18e3th9 {
        background-color: #0E1117;
        color:white;
    }
    .stButton button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .stSlider {
        color: #C7C9D3;
    }
    .stTextInput, .stSelectbox, .stCheckbox {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Input for threshold value
st.markdown(
    "<p style='color:white;'>Select % Similarity threshold: Greater threshold -> stricter similarity check</p>",
    unsafe_allow_html=True
)
threshold = st.slider('.', min_value=0.0, value=70.0, max_value=100.0)/100.0

# Function to print similar sections
def print_similar_ns_sections(ipc_sec):
    node = "ipc_" + ipc_sec
    similars = list(Graph.neighbors(node))
    if not similars:
        st.write(f"No similar Nyay Sanhita sections found: Try lowering the similarity threshold using the above slider")
        st.write("NOTE: Too low similarity % may lead to incorrect matchings")
    else:
        st.write(f"Sections similar to IPC section {ipc_sec}:")
        for similar in similars:
            sim_index = int(similar.replace("ns_", ""))
            section = ns_sections[sim_index-1]
            similarity_val = Graph[node][similar]['weight']
            st.write(f"Nyay Sanhita Section: {section[0]}, Similarity: {similarity_val * 100:.2f}%")
            st.write(section[1])
            st.write('---')

# Function to plot bipartite graph
def plot_bipartite_graph():
    pos = nx.bipartite_layout(Graph, [f"ipc_{ipc_sections[i][0]}" for i in range(len(ipc_sections))])
    ipc_nodes = [f"ipc_{ipc_sections[i][0]}" for i in range(len(ipc_sections))]
    ns_nodes = [f"ns_{ns_sections[i][0]}" for i in range(len(ns_sections))]

    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(Graph, pos, nodelist=ipc_nodes, node_size=100, node_color='red', label="IPC Sections")
    nx.draw_networkx_nodes(Graph, pos, nodelist=ns_nodes, node_size=100, node_color='green', label="Nyay Sanhita")
    nx.draw_networkx_edges(Graph, pos, edgelist=Graph.edges(data=True), width=1)
    plt.title(f"Bipartite Graph: Threshold {threshold}")
    plt.legend()
    st.pyplot(plt)

# Create the graph
Graph = nx.Graph()
Graph.add_nodes_from([f"ipc_{ipc_sections[i][0]}" for i in range(len(ipc_sections))], bipartite=0)
Graph.add_nodes_from([f"ns_{ns_sections[i][0]}" for i in range(len(ns_sections))], bipartite=1)

for i, ipc_embedding in enumerate(ipc_embeddings):
    similarities = util.pytorch_cos_sim(ipc_embedding, ns_embeddings)[0]
    for j, similarity in enumerate(similarities):
        if similarity > threshold:
            Graph.add_edge(f"ipc_{ipc_sections[i][0]}", f"ns_{ns_sections[j][0]}", weight=float(similarity))

# Create columns for layout
col1, col2, col3 = st.columns([3, 4, 3])

with col2:
    if st.button('Visualise the Graph Mapping'):
        plot_bipartite_graph()

# User input to select IPC section
ipc_section_names = [section[0] for section in ipc_sections]
selected_index = st.selectbox('Select IPC section', range(len(ipc_section_names)), format_func=lambda x: ipc_section_names[x])

# Display the selected IPC section content
selected_ipc_section = ipc_sections[selected_index]
st.write(f"<p style='color:white; '>IPC Section{selected_ipc_section[0]}</p>", unsafe_allow_html=True)

st.write(selected_ipc_section[1])

# Display similar Nyay Sanhita sections
if st.button('Show Similar Nyay Sanhita Sections'):
    print_similar_ns_sections(selected_ipc_section[0])
