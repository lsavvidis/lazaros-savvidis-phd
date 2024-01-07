import matplotlib.pyplot as plt
import numpy as np
import math
import random
import networkx as nx
from scipy.spatial import distance
# Initialize random seed for reproducibility
random.seed(0)

def calculate_chords(r):
    C = 2 * math.pi * r
    num_chords = round(C)
    chord_length = 2 * r * math.sin(math.pi / num_chords)
    return num_chords, chord_length

def create_point(r, angle, index, point_counter, nectar_value):
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    
    # logic for segmentation
    equal_part = math.ceil(math.degrees(angle) / (360 / num_scout_bees))
    
    if y == 0 and x > 0:
        equal_part = 1  # Assign to the first bee
    
    point = {
        "index": index + point_counter + 1,
        "coordinates": (x, y),
        "angle": math.degrees(angle),
        "distance_from_center": r,
        "segment": equal_part,
        "nectar_value": nectar_value 
    }
    point["nectar_value"] = random.randint(0, 100)  # Nectar value ranges from 0 to 100
    return point


def compute_points(r, point_counter):
    num_chords, _ = calculate_chords(r)
    angles = np.linspace(0, 2*math.pi, num_chords, endpoint=False)
    nectar_values = [random.randint(0, 100) for _ in range(num_chords)]
    points = [create_point(r, angle, i, point_counter, nectar_values[i]) for i, angle in enumerate(angles)]
    return points, point_counter + num_chords 
def create_graph_from_points(points):
    G = nx.Graph()
    for point in points:
        G.add_node(point["ID"], pos=point["Coordinates"])
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = distance.euclidean(points[i]["Coordinates"], points[j]["Coordinates"])
            G.add_edge(points[i]["ID"], points[j]["ID"], weight=dist)
    return G

def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def two_opt(route, G):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                if j - i == 1:  # Skip adjacent edges
                    continue
                new_route = route[:]
                new_route[i:j] = reversed(route[i:j])  # Reverse the segment
                if sum(calculate_distance(G.nodes[new_route[k]]['pos'], G.nodes[new_route[k - 1]]['pos']) for k in range(1, len(new_route))) < sum(calculate_distance(G.nodes[best[k]]['pos'], G.nodes[best[k - 1]]['pos']) for k in range(1, len(best))):
                    best = new_route
                    improved = True
    return best

def nearest_neighbor(G):
    start_node = list(G.nodes)[0]
    tour = [start_node]
    unvisited = set(G.nodes)
    unvisited.remove(start_node)

    while unvisited:
        nearest = min(unvisited, key=lambda x: G[tour[-1]][x]['weight'])
        tour.append(nearest)
        unvisited.remove(nearest)

    tour.append(start_node)  # Return to the starting node
    return tour

def bee_path(bee_data, ax):
    center = {"ID": 0, "Coordinates": (0, 0)}
    bee_data.insert(0, center)
    
    G = create_graph_from_points(bee_data)

    # Find the approximate solution using Christofides Algorithm
    approx_tour = nearest_neighbor(G)

    prev_length = float('inf')
    
    while True:
        # Apply 2-opt to find a better route
        circuit_optimized = two_opt(approx_tour, G)
        
        # Calculate the length of the optimized route
        current_length = sum(calculate_distance(G.nodes[circuit_optimized[k]]['pos'], G.nodes[circuit_optimized[k - 1]]['pos']) for k in range(1, len(circuit_optimized)))
        
        # If the length didn't improve, break out of the loop
        if current_length >= prev_length:
            break

        # Update the previous length and the best-known circuit
        prev_length = current_length
        approx_tour = circuit_optimized
    
    # Calculate the total weight of the approximate tour
    total_weight = sum(G[u][v]['weight'] for u, v in zip(approx_tour, approx_tour[1:]))
    print("Total Weight:", total_weight)
    
    for i in range(len(approx_tour) - 1):
        x1, y1 = G.nodes[approx_tour[i]]['pos']
        x2, y2 = G.nodes[approx_tour[i + 1]]['pos']
        x_coords = [x1, x2]
        y_coords = [y1, y2]
        ax.plot(x_coords, y_coords, color='red')
        
def draw_points(ax, points):
    for point in points:
        x, y = point["coordinates"]
        index = point["index"]
        nectar = point["nectar_value"]


        if nectar >= 90:
            color = 'red'
        elif nectar >= 80:
            color = 'green'
        elif nectar >= 70:
            color = 'yellow'
        elif nectar >= 60:
            color = 'pink'
        elif nectar >= 50:
            color = 'brown'
        else:
            color = 'black'

        ax.scatter(x, y, color=color)
        ax.text(x, y, str(index), fontsize=8)

    # Make the 0 point center bold
    ax.scatter(0, 0, color='black', zorder=5)
    ax.text(0, 0, "0", fontsize=12, ha='right', va='bottom')
    
    
    
    
    

# Initialize the plot
fig, ax = plt.subplots(figsize=(10,10))
plt.xlim(-12, 12)
plt.ylim(-12, 12)
ax.set_aspect('equal')

# Initialize variables
all_points = []
point_counter = 0
num_scout_bees = int(input("Enter the number of super scout bees: "))
num_radii = 11 #Number of circles

# Generate points
for r in range(1, num_radii):
    points, point_counter = compute_points(r, point_counter)
    all_points += points



# Plot the points
draw_points(ax, all_points)

# Plot concentric circles and radii
for r in range(1, num_radii):
    circle = plt.Circle((0, 0), r, color='gray', fill=False, linewidth=0.4)
    ax.add_artist(circle)

radii_angles = np.arange(0, 2*math.pi, math.radians(360/num_scout_bees))
for angle in radii_angles:
    ax.plot([0, 10 * np.cos(angle)], [0, 10 * np.sin(angle)], color='gray', linewidth=0.4)



# Segment the points for each super scout bee
segmented_data = {i+1: [] for i in range(num_scout_bees)}

for point in all_points:
    bee_num = point["segment"]
    segmented_data[bee_num].append({
        "ID": point["index"],
        "Coordinates": point["coordinates"],
        "Distance from Center": point["distance_from_center"],
        "Nectar": point["nectar_value"],
        "Angle": point["angle"]
        
    })

# Plot paths for all the super scout bees
for bee_num, bee_data in segmented_data.items():
    bee_path(bee_data, ax)  
plt.show()