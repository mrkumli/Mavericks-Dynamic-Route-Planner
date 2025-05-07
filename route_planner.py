import csv
import json

#Load the graph adjacency list from data/graph.csv.

def load_graph():
    graph = {}
    with open('data/graph.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            graph[row['node']] = json.loads(row['neighbors'])
    return graph

#Custom heap functions
def heapify(arr, n, i):

    smallest = i  # Initializes the smallest as root
    left = 2 * i + 1
    right = 2 * i + 2

    #Checks if left child exists and is smaller than root
    if left < n and arr[left][0] < arr[smallest][0]:
        smallest = left

    #Checks if right child exists and is smaller than current smallest
    if right < n and arr[right][0] < arr[smallest][0]:
        smallest = right

  
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify(arr, n, smallest)


#Builds a min heap using an array
def build_min_heap(arr):
    n = len(arr)
    #Starts from last non-leaf node and heapify all nodes in reverse order
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


#We use this function to push items onto the heap
def heap_push(heap, item):
    heap.append(item)
    idx = len(heap) - 1
    parent = (idx - 1) // 2
    
    #Bubble up until we find the correct position
    while idx > 0 and heap[idx][0] < heap[parent][0]:
        heap[idx], heap[parent] = heap[parent], heap[idx]
        idx = parent
        parent = (idx - 1) // 2

#This function pops and returns the smallest element from the heap
def heap_pop(heap):
    if not heap:
        return None
    
    #Get the root (minimum value)
    min_item = heap[0]
    
    #Replace root with last element
    heap[0] = heap[-1]
    heap.pop()
    
    #Restore heap property
    if heap:
        heapify(heap, len(heap), 0)
    
    return min_item


#Uses djikstras algorithm to compute the shortest path with a min-heap
def dijkstra(graph, start, end):
    heap = [(0, start)]
    visited = set()
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    
    while heap:
        current_dist, current_node = heap_pop(heap)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heap_push(heap, (new_dist, neighbor))

    #Reconstruct path
    path = []
    node = end
    while node:
        path.append(node)
        node = previous[node]
    path.reverse()

    return path if distances[end] != float('inf') else None, distances[end]


#One of our main functions. Uses heap sort to sort an array.
def heap_sort(arr):
    #Build a min heap
    build_min_heap(arr)
    
    #Extract elements one by one
    sorted_arr = []
    while arr:
        sorted_arr.append(heap_pop(arr))
    
    return sorted_arr

if __name__ == "__main__":
    graph = load_graph()
    start = input("Enter starting node: ")
    end = input("Enter destination node: ")
    path, cost = dijkstra(graph, start, end)
    if path:
        print("Shortest path:", " → ".join(path))
        print("Total cost:", round(cost, 2))
    else:
        print("No path found.")