import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt


graph = {
    "Railway Station": {
        "Bus Stand": 4,
        "Market": 2
    },
    "Bus Stand": {
        "Railway Station": 4,
        "Hospital": 5,
        "Market": 1
    },
    "Market": {
        "Railway Station": 2,
        "Bus Stand": 1,
        "Mall": 7
    },
    "Hospital": {
        "Bus Stand": 5,
        "University": 3
    },
    "Mall": {
        "Market": 7,
        "Airport": 4
    },
    "University": {
        "Hospital": 3,
        "Airport": 6
    },
    "Airport": {
        "Mall": 4,
        "University": 6
    }
}


def dijkstra(graph, start, end):
    import heapq

    distances = {node: float('inf') for node in graph}
    previous = {}

    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            break

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []

    current = end

    while current != start:
        path.append(current)

        if current not in previous:
            return None, None

        current = previous[current]

    path.append(start)
    path.reverse()

    return path, distances[end]


def show_route():

    source = source_var.get()
    destination = destination_var.get()

    if source == destination:
        messagebox.showerror(
            "Error",
            "Source and Destination cannot be same!"
        )
        return

    path, distance = dijkstra(
        graph,
        source,
        destination
    )

    result_label.config(
        text=f"Shortest Distance : {distance} km\nPath : {' ➜ '.join(path)}"
    )

    draw_graph(path)


def draw_graph(shortest_path):

    G = nx.Graph()

    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        node_color="skyblue",
        font_size=8
    )

    edge_labels = nx.get_edge_attributes(
        G,
        'weight'
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels
    )

    if shortest_path:

        edges = []

        for i in range(len(shortest_path) - 1):
            edges.append(
                (shortest_path[i],
                 shortest_path[i + 1])
            )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            edge_color="red",
            width=4
        )

    plt.title("Smart City Route Planner")
    plt.show()


root = tk.Tk()
root.title("Smart City Route Planner")
root.geometry("500x400")

title = tk.Label(
    root,
    text="Smart City Route Planner",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

locations = list(graph.keys())

source_var = tk.StringVar()
destination_var = tk.StringVar()

source_var.set(locations[0])
destination_var.set(locations[1])

tk.Label(root, text="Select Source",
         font=("Arial", 12)).pack()

ttk.Combobox(
    root,
    textvariable=source_var,
    values=locations
).pack(pady=5)

tk.Label(root, text="Select Destination",
         font=("Arial", 12)).pack()

ttk.Combobox(
    root,
    textvariable=destination_var,
    values=locations
).pack(pady=5)

tk.Button(
    root,
    text="Find Shortest Path",
    bg="green",
    fg="white",
    command=show_route
).pack(pady=20)

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 11)
)

result_label.pack()

root.mainloop()