import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def display_graph(graph, pos, edge_labels=None):
    """Affiche le graphe avec Matplotlib."""
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=15, font_color="black")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red", font_size=12)
    st.pyplot(plt)

def bellman_ford(graph, source):
    """Implémente l'algorithme Bellman-Ford pour le calcul du plus court chemin."""
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[source] = 0
    # Relaxation des arêtes
    for _ in range(len(graph.nodes()) - 1):
        for u, v, weight in graph.edges(data="weight"):
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u

    # Détection des cycles négatifs
    for u, v, weight in graph.edges(data="weight"):
        if distances[u] + weight < distances[v]:
            return None, None  # Cycle négatif détecté

    return distances, predecessors
    
def reconstruct_path(predecessors, target):
    """Reconstruit le chemin le plus court à partir des prédécesseurs."""
    path = []
    while target is not None:
        path.insert(0, target)
        target = predecessors[target]
    return path

def main():
    st.title("Choix des noeuds et poids avec Bellman-Ford")
    st.sidebar.title("Paramètres du graphe")

    # Création d'un graphe orienté
    G = nx.DiGraph()

    # Choisir les noeuds
    nodes = st.sidebar.text_input("Liste des noeuds (ex: A,B,C)", value="A,B,C,D")
    nodes = [n.strip() for n in nodes.split(',') if n.strip()]

    for node in nodes:
        G.add_node(node)

    # Ajouter des arêtes manuellement
    st.sidebar.subheader("Ajouter les arêtes")
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j and st.sidebar.checkbox(f"Lier {nodes[i]} → {nodes[j]}", key=f"link_{nodes[i]}_{nodes[j]}"):
                weight = st.sidebar.number_input(f"Poids entre {nodes[i]} → {nodes[j]}", min_value=-100, max_value=100, value=1, key=f"weight_{nodes[i]}_{nodes[j]}")
                edges.append((nodes[i], nodes[j], weight))

    # Ajouter les arêtes au graphe
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)

    # Afficher le graphe
    st.subheader("Représentation du Graphe")
    pos = nx.circular_layout(G)
    edge_labels = nx.get_edge_attributes(G, "weight")
    display_graph(G, pos, edge_labels)

    # Choix de la source et de la cible
    st.subheader("Calcul du plus court chemin")
    source = st.selectbox("Noeud source", options=nodes)
    target = st.selectbox("Noeud cible", options=nodes)

    # Exécuter Bellman-Ford
    if st.button("Calculer le plus court chemin"):
        distances, predecessors = bellman_ford(G, source)
        if distances is None:
            st.error("Cycle négatif détecté !")
        else:
            if distances[target] == float('inf'):
                st.warning(f"Aucun chemin trouvé entre {source} et {target}.")
            else:
                path = reconstruct_path(predecessors, target)
                st.success(f"Le plus court chemin est : {' → '.join(path)} avec un coût de {distances[target]}")

                # Affichage visuel du chemin
                path_edges = list(zip(path[:-1], path[1:]))
                edge_colors = ["red" if (u, v) in path_edges else "black" for u, v in G.edges()]
                plt.figure(figsize=(8, 6))
                nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=15, font_color="black", edge_color=edge_colors)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=12)
                st.pyplot(plt)

if __name__ == "__main__":
    main()
