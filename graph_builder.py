import csv
import json


#Uses our utility files. nodes.csv, cities,csv and edges.csv to constrct the graph represantation of our routes
#in the form of an adjacency list
def build_graph():
    #Read nodes and edges
    nodes = {}
    with open('data/nodes.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['node_id']] = row['city']
    graph = {}

    with open('data/edges.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u, v = row['node1'], row['node2']
            weight = float(row['distance']) * (1 + float(row['traffic']))
            if u not in graph:
                graph[u] = {}
            if v not in graph:
                graph[v] = {}
            graph[u][v] = weight
            graph[v][u] = weight  #Undirected graph

    #Save graph to CSV
    with open('data/graph.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['node', 'neighbors'])
        for node, neighbors in graph.items():
            writer.writerow([node, json.dumps(neighbors)])

if __name__ == "__main__":
    build_graph()
