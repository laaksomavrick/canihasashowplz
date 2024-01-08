import networkx as nx


def generate_graph(model, data):
    graph = nx.Graph()

    for show in data.columns:
        show_data = data[[show]].T
        _, indices = model.kneighbors(show_data, n_neighbors=5)
        similar_shows = data.iloc[indices[0]].index.tolist()

        for similar_show in similar_shows:
            if similar_show != show:
                graph.add_edge(show, similar_show)

    return graph
