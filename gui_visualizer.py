import turtle
import csv
import random
import math # Added for angle calculations
from route_planner import load_graph, dijkstra 

#These are the dimensions for the turtle graphics window

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Visual attributes of the nodes such as color, node radius, font size etc
NODE_RADIUS = 10
NODE_COLOR = "blue"
EDGE_COLOR = "gray"
PATH_NODE_COLOR = "green"
PATH_EDGE_COLOR = "red"
PATH_EDGE_WIDTH = 2 # Slightly thinner to make arrows clearer
LABEL_FONT_SIZE = 8
ARROW_SIZE = 8 # Size of the arrowhead

#Assigns random coordinates to the graph nodes and returns these coordinates in the form of a dictionary
def load_node_coordinates(graph, width, height):
    coordinates = {}
    padding = 50 # Padding from screen edges
    drawable_width = width - 2 * padding
    drawable_height = height - 2 * padding
    min_x, max_x = -drawable_width // 2, drawable_width // 2
    min_y, max_y = -drawable_height // 2, drawable_height // 2

    for node in graph:
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        coordinates[node] = (x, y)
    return coordinates

#Draws our node/circle onto the screen
def draw_node(pen, x, y, node_id, color=NODE_COLOR, radius=NODE_RADIUS):

    pen.penup()
    pen.goto(x, y - radius) #Position pen slightly below center for circle
    pen.pendown()
    pen.pencolor(color) #Use pencolor for outline in case fill is different
    pen.fillcolor(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()
    pen.penup()
    pen.goto(x, y + radius + 2) #Position for label slightly above node
    pen.write(node_id, align="center", font=("Arial", LABEL_FONT_SIZE, "normal"))


#Draws line/edge between two nodes
def draw_edge(pen, x1, y1, x2, y2, color=EDGE_COLOR, width=1):

    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.pencolor(color)
    pen.width(width)
    pen.goto(x2, y2)
    pen.width(1) #Resets the width


#draws a line indicating the direction being followed
def draw_directed_edge(pen, x1, y1, x2, y2, color=PATH_EDGE_COLOR, width=PATH_EDGE_WIDTH, arrow_size=ARROW_SIZE):

    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.pencolor(color)
    pen.width(width)

    #Calculates angle of the line
    angle = math.atan2(y2 - y1, x2 - x1)
    pen.setheading(math.degrees(angle))

    #Calculates the end point slightly before the actual node to make space for arrow
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    line_end_dist = max(0, dist - (NODE_RADIUS + arrow_size / 2)) # Draw line up to just before node radius + arrow buffer

    #Draws the main line segment
    pen.goto(x1 + line_end_dist * math.cos(angle), y1 + line_end_dist * math.sin(angle))

    #Draws the arrowhead
    pen.fillcolor(color)
    pen.begin_fill()
    #Positions pen at the tip of the arrow (original end point)
    pen.penup()
    pen.goto(x2 - NODE_RADIUS * math.cos(angle), y2 - NODE_RADIUS * math.sin(angle)) # Point arrow towards edge of the node circle
    pen.pendown()
    #Turn back and draw one side of the arrow
    pen.left(150)
    pen.forward(arrow_size)
    #Turn to draw the other side
    pen.goto(x2 - NODE_RADIUS * math.cos(angle), y2 - NODE_RADIUS * math.sin(angle))
    pen.right(300) # 150 + 150
    pen.forward(arrow_size)
    pen.goto(x2 - NODE_RADIUS * math.cos(angle), y2 - NODE_RADIUS * math.sin(angle)) # Back to tip
    pen.end_fill()

    pen.width(1) #Reset width
    pen.setheading(0) #Reset heading


def visualize_graph(graph, coordinates, shortest_path=None):
    """Draws the entire graph and highlights the shortest path if provided."""
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)#Turns off the screen updates for faster drawing

    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    pen.penup() 

    #Draws all non-path edges first
    drawn_edges = set()
    path_edges = set()
    if shortest_path:
        for i in range(len(shortest_path) - 1):
             # Store path edges to avoid drawing them gray first
             path_edges.add(tuple(sorted((shortest_path[i], shortest_path[i+1]))))

    for u, neighbors in graph.items():
        for v in neighbors:
            edge = tuple(sorted((u, v)))
            if edge not in path_edges and edge not in drawn_edges:
                ux, uy = coordinates[u]
                vx, vy = coordinates[v]
                draw_edge(pen, ux, uy, vx, vy, color=EDGE_COLOR)
                drawn_edges.add(edge)

    #Draws the highlighted shortest path with direction
    if shortest_path:
        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i+1]
            ux, uy = coordinates[u]
            vx, vy = coordinates[v]
            # Use the new function to draw directed edges for the path
            draw_directed_edge(pen, ux, uy, vx, vy, color=PATH_EDGE_COLOR, width=PATH_EDGE_WIDTH, arrow_size=ARROW_SIZE)

    #Draws all nodes (drawing nodes last ensures they are on top of edges)
    node_color_map = {node: NODE_COLOR for node in graph}
    if shortest_path:
        for node in shortest_path:
            node_color_map[node] = PATH_NODE_COLOR # Mark path nodes for coloring

    for node, (x, y) in coordinates.items():
        draw_node(pen, x, y, node, color=node_color_map[node])


    screen.update() 
    screen.mainloop() 


if __name__ == "__main__":
    print("Loading graph...")
    try:
        graph = load_graph() #
        if not graph:
            print("Error: Graph is empty or could not be loaded.")
            exit()
        print("Graph loaded.")
    except FileNotFoundError:
        print("Error: 'data/graph.csv' not found. Please run graph_builder.py first.")
        exit()
    except Exception as e:
        print(f"An error occurred loading the graph: {e}")
        exit()

    print("Assigning node coordinates...")
    node_coords = load_node_coordinates(graph, SCREEN_WIDTH, SCREEN_HEIGHT)
    print("Coordinates assigned.")

    while True:
        start_node = input(f"Enter starting node ID (e.g., {list(graph.keys())[0]}): ").strip().upper()
        if start_node in graph:
            break
        print(f"Error: Node '{start_node}' not found in graph. Available nodes: {list(graph.keys())}")

    while True:
        end_node = input(f"Enter destination node ID (e.g., {list(graph.keys())[-1]}): ").strip().upper()
        if end_node in graph:
            break
        print(f"Error: Node '{end_node}' not found in graph. Available nodes: {list(graph.keys())}")

    print(f"Calculating shortest path from {start_node} to {end_node}...")
    path, cost = dijkstra(graph, start_node, end_node) #

    if path:
        print("Shortest path:", " → ".join(path)) #
        print("Total cost:", round(cost, 2)) #
        print("Visualizing graph and highlighting path with direction...")
        visualize_graph(graph, node_coords, shortest_path=path)
    else:
        print("No path found between the specified nodes.") #
        print("Visualizing the full graph without highlighting...")
        visualize_graph(graph, node_coords)
