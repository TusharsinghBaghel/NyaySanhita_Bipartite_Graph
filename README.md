# IPC to Bhartiya Nyay Sanhita Mapping Tool

## Introduction
This tool is designed to facilitate the transition from the Indian Penal Code (IPC) to the Bhartiya Nyay Sanhita, which will come into effect from 1st July 2024. It uses NLP techniques to create embeddings using the Sentence-transformer embedding model for legal sections and employs cosine similarity function of pytorch to map corresponding sections between the two codes. The tool features a Streamlit application that provides visualizations and search functionalities.

## Creation of sections dataset
"split.py" contains the script for splitting and creation of the sections dataset for both the documents.

## Features
- **Sentence Transformer Embeddings**: Utilizes 'sentence-transformers/all-MiniLM-L6-v2' model to create embeddings for the IPC and Nyay Sanhita sections.
- **Cosine Similarity Analysis**: Computes the similarity between IPC and Nyay Sanhita sections to identify correspondences.
- **Bipartite Graph**: Constructs a bipartite graph to represent the similarity relationships, with a user-defined threshold for similarity scores.
- **Streamlit Visualization**: Offers an interactive visualization of the bipartite graph and a search function to find related Nyay Sanhita sections for a given IPC section.

## Bipartite Mapping Visualization

![Bipartite Mapping Visualization](./0.7.png)


Link to the deployed streamlit application: https://nyaysanhitabipartitegraph-pvkgjyydo3iahrucb2eutf.streamlit.app/
