# Mavericks-Dynamic-Route-Planner

A dynamic, traffic-aware route planner that computes and visualizes the shortest path between two locations in a city graph using **Dijkstra’s Algorithm**. The system simulates traffic changes in real time, adapts the route accordingly, and provides an interactive visualization using Python's turtle graphics.

________________________________________________________________________________

## TLDR: How to Use the Project

### Step 1: Prepare Your Data
- **cities.csv**: Contains the list of cities and their IDs. Modify it to include the cities you want in the graph.
- **nodes.csv**: Maps the node IDs to the city names. Node IDs here must match city IDs in `cities.csv`.
- **edges.csv**: Represents the connections (roads) between cities, containing:
  - `node1`, `node2`: IDs of the two connected cities.
  - `distance`: Distance between the cities.
  - `traffic`: A traffic factor that adjusts the distance.

> 📝 **Note:**  
> The **graph is initially empty**. You need to build it using `graph_builder.py`, which generates `graph.csv`.

### Step 2: Build the Graph
Run:

```bash
python graph_builder.py
```

This creates `graph.csv`, representing the graph as an adjacency list with traffic-adjusted weights.

### Step 3: Visualize the Graph
Run:

```bash
python gui_visualiser.py
```

It will prompt you for start and end nodes and visualize the graph with the shortest path highlighted.

### Step 4: Find the Shortest Path and Cost
Run:

```bash
python route_planner.py
```

It will ask for the start and end nodes and print the shortest path and total cost.

---

## 📂 Input Files Format

| File | Format | Example |
|:----|:------|:--------|
| `cities.csv` | `city_id,city_name` | `1,Karachi` |
| `nodes.csv` | `node_id,city_name` | `KHI,Karachi` |
| `edges.csv` | `node1,node2,distance,traffic` | `KHI,LHR,150,0.2` |
> 0 <= 'traffic' <= 1 for effective weight calculation

- **cities.csv**: Simple mapping of unique city IDs to names.
- **nodes.csv**: Used to assign cities to nodes during visualization.
- **edges.csv**: Contains the roads. `traffic` is a multiplier:  
  > e.g., traffic = 0.2 means the road feels 0.2× longer due to congestion.

The `graph.csv` generated later will use an adjacency list format based on these inputs.

________________________________________________________________________________

## Features

- **Dynamic Traffic Simulation:** Real-time traffic changes during runtime.
- **Dijkstra’s Algorithm:** For shortest path calculation with dynamic weights.
- **Adjacency List Representation:** Efficient graph structure.
- **Visualization:** Real-time visual output with Turtle graphics.
- **CSV Input and Output:** Easy to edit and extend.

________________________________________________________________________________

## Tools & Technologies

- **Python 3.x**
- **Libraries:** `csv`, `math`, `random`, `turtle`
- **File Formats:** `.csv` for data, `.py` for scripts.

________________________________________________________________________________

## Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/route-planner.git
   cd route-planner
   ```

2. Install necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure your CSVs are in the `data` folder or update paths accordingly.

________________________________________________________________________________

## How It Works

1. **Graph Representation:** Cities as nodes, roads as edges with distance × traffic factor as weights.
2. **Sorting:** Min Heap Sort employed to effectively sort nodes in order.
3. **Traffic Simulation:** Random changes to traffic on each run.
4. **Pathfinding:** Shortest path found using Dijkstra's algorithm.
5. **Visualization:** Turtle graphics shows the graph and the optimal route.

________________________________________________________________________________

## Testing & Evaluation

- **Input:** Start and end nodes.
- **Output:** Shortest path and its total cost.
- **Visual Output:** Path is shown in green, others in light blue.

________________________________________________________________________________

## Limitations & Future Improvements

- Random traffic simulation (not live traffic).
- Turtle graphics is slow for large graphs.
- May need optimization for bigger maps.

**Future Plans:**
- Integrate real-time traffic APIs.
- Upgrade GUI with Tkinter or PyQt.
- Add support for one-way and multi-lane roads.
- Build mobile-friendly versions.
________________________________________________________________________________

## 📜 Detailed Code Explanation

### 1. `data_manager.py`
- `clear_csv(file_path)`: Clears a CSV file.
- `update_traffic(edge_file, node1, node2, new_traffic)`: Update traffic value.
- `load_cities_data()`: Load node-to-city mappings.

### 2. `graph_builder.py`
- `build_graph()`: Reads CSVs and builds an adjacency list, saving it as `graph.csv`.

### 3. `gui_visualiser.py`
- `load_node_coordinates(graph, width, height)`: Randomly place nodes.
- `draw_node(pen, x, y, node_id)`: Draw cities.
- `draw_edge(pen, x1, y1, x2, y2)`: Draw edges (roads).
- `draw_directed_edge(pen, x1, y1, x2, y2)`: Highlight path.
- `visualize_graph(graph, coordinates, shortest_path=None)`: Main visualization.

### 4. `route_planner.py`
- `load_graph()`: Loads the graph from `graph.csv`.
- `dijkstra(graph, start, end)`: Dijkstra's algorithm to compute the shortest route.
- Heap helper functions for managing the priority queue manually.
