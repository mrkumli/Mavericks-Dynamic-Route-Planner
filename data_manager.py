import csv

#clears data in a csv file
def clear_csv(file_path):
    with open(file_path, 'w') as f:
        f.truncate()

#Allows us to dynamically udpdate traffic values and edges between two nodes
def update_traffic(edge_file, node1, node2, new_traffic):
    rows = []
    with open(edge_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row['node1'] == node1 and row['node2'] == node2) or (row['node1'] == node2 and row['node2'] == node1):
                row['traffic'] = new_traffic
            rows.append(row)

    with open(edge_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

#A helper function. Its main utility is allowing us to visualize our graph if neeeded.
def load_cities_data():
    cities = {}
    with open('data/nodes.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cities[row['node_id']] = row['city']
    return cities

if __name__ == "__main__":
    # clear_csv('data/edges.csv')
    # update_traffic('data/edges.csv', 'NYC', 'PHL', '0.5')
    pass
