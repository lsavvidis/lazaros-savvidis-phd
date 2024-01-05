import matplotlib.pyplot as plt
import numpy as np
import math
import random
from scipy.spatial import distance

# Initialize random seed for reproducibility
random.seed(0)

def calculate_chords(r): # chord length 
    C = 2 * math.pi * r
    num_chords = round(C)
    chord_length = 2 * r * math.sin(math.pi / num_chords)
    return num_chords, chord_length

def create_point(r, angle, index, point_counter, nectar_value):
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    
    # segmentation
    equal_part = math.ceil(math.degrees(angle) / (360 / num_scout_bees))
    
    if y == 0 and x > 0:
        equal_part = 1  # Assign first segment to the first bee
    
    point = {
        "index": index + point_counter + 1,
        "coordinates": (x, y),
        "angle": math.degrees(angle),
        "distance_from_center": r,
        "segment": equal_part,
        "nectar_value": nectar_value 
    }
    point["nectar_value"] = random.randint(0, 100)  # Nectar value from 0 to 100 for the future
    return point

def compute_points(r, point_counter):
    num_chords, _ = calculate_chords(r)
    angles = np.linspace(0, 2*math.pi, num_chords, endpoint=False)
    nectar_values = [random.randint(0, 100) for _ in range(num_chords)]
    points = [create_point(r, angle, i, point_counter, nectar_values[i]) for i, angle in enumerate(angles)]
    return points, point_counter + num_chords



def find_shorter_adjacent_pairs(bee_data, ax, num_radii):
    first_path_best_pairs = []
    second_path_best_pairs = []
    sorted_data = sorted(bee_data, key=lambda x: x['Distance from Center'])
    radii = sorted(list(set([x['Distance from Center'] for x in sorted_data])))[:num_radii]
    for i, r in enumerate(radii):
        remaining_points = [f for f in sorted_data if f['Distance from Center'] == r]
        next_radius_remaining_points = [f for f in sorted_data if f['Distance from Center'] == r + 1]
        remaining_radii = len(radii) - i - 1
        skip_next = True if remaining_radii % 2 != 0 else False

        if len(remaining_points) >= 2 and not skip_next:
            remaining_points = sorted(remaining_points, key=lambda x: x['Angle'])
            next_radius_remaining_points = sorted(next_radius_remaining_points, key=lambda x: x['Angle'])
            
            best_distance = float('inf')
            best_pair_first_path = None
            best_pair_second_path = None
            
            for i in range(len(remaining_points) - 1):
                for j in range(len(next_radius_remaining_points) - 1):
                    dist1 = distance.euclidean(remaining_points[i]['Coordinates'], next_radius_remaining_points[j]['Coordinates'])
                    dist2 = distance.euclidean(remaining_points[i + 1]['Coordinates'], next_radius_remaining_points[j + 1]['Coordinates'])
                    total_dist = dist1 + dist2
                    
                    if total_dist < best_distance:
                        best_distance = total_dist
                        best_pair_first_path = (remaining_points[i], next_radius_remaining_points[j])
                        best_pair_second_path = (remaining_points[i + 1], next_radius_remaining_points[j + 1])
            
            if best_pair_first_path and best_pair_second_path:
                first_path_best_pairs.append(best_pair_first_path)
                second_path_best_pairs.append(best_pair_second_path)
                
                # Plotting logic for best pairs
                x_coords = [best_pair_first_path[0]['Coordinates'][0], best_pair_first_path[1]['Coordinates'][0]]
                y_coords = [best_pair_first_path[0]['Coordinates'][1], best_pair_first_path[1]['Coordinates'][1]]
                ax.plot(x_coords, y_coords, color='blue')
                
                x_coords = [best_pair_second_path[0]['Coordinates'][0], best_pair_second_path[1]['Coordinates'][0]]
                y_coords = [best_pair_second_path[0]['Coordinates'][1], best_pair_second_path[1]['Coordinates'][1]]
                ax.plot(x_coords, y_coords, color='green')

    return first_path_best_pairs, second_path_best_pairs


def find_closest_point(base_point, point_list):
    min_distance = float("inf")
    closest_point = None
    for point in point_list:
        dist = distance.euclidean(base_point['Coordinates'], point['Coordinates'])
        if dist < min_distance:
            min_distance = dist
            closest_point = point
    return closest_point, min_distance

def update_visited(visited_points, visited_ids, point):
    if point not in visited_points:
        visited_points.append(point)
        visited_ids.append(point['ID'])
    return visited_points, visited_ids, point

def pick_closest_pair(points1, points2):
    dist_first_to_first = distance.euclidean(points1[0]['Coordinates'], points2[0]['Coordinates'])
    dist_last_to_last = distance.euclidean(points1[-1]['Coordinates'], points2[-1]['Coordinates'])
    return (points1[0], points2[0]) if dist_first_to_first < dist_last_to_last else (points1[-1], points2[-1])

def handle_first_path(radii, sorted_data, ax, first_path_best_pairs, second_path_best_pairs, num_radii):
    visited_points = []
    visited_ids = []
    last_visited = center_point = {'Coordinates': (0, 0), 'Distance from Center': 0, 'Angle': 0, 'ID': '0'}
    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, center_point)
    index_to_check = None
    odd_radii = (num_radii - 1) % 2 != 0

    for i, r in enumerate(radii):
        remaining_radii = len(radii) - i - 1
        skip_next = remaining_radii % 2 != 0
        remaining_points = [f for f in sorted_data if f['Distance from Center'] == r]
        next_radius_remaining_points = [f for f in sorted_data if f['Distance from Center'] == r + 1]

        if r == 1 and len(remaining_points) >= 2:
            if odd_radii:
                visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, remaining_points[0])
                
                index_to_check = 0
            else:
                closest_point_1, closest_point_2 = pick_closest_pair(remaining_points, next_radius_remaining_points)
                visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_1)
                visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_2)
               
                index_to_check = 0 if last_visited == next_radius_remaining_points[0] else -1

        elif len(remaining_points) == 1:
            if len(next_radius_remaining_points) > 2:
                if not skip_next:
                    closest_point, _ = find_closest_point(remaining_points[0], next_radius_remaining_points)
                    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, remaining_points[0])
                    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point)
                    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, next_radius_remaining_points[-1])
                    
                    index_to_check = -1
                else:
                    closest_point_1, closest_point_2 = pick_closest_pair(remaining_points, next_radius_remaining_points)
                    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_1)
                    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_2)
                    
                    index_to_check = 0 if last_visited == next_radius_remaining_points[0] else -1
            else:
                closest_point_1, closest_point_2 = pick_closest_pair(remaining_points, next_radius_remaining_points)
                visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_1)
                visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_2)
                
                index_to_check = 0 if last_visited == next_radius_remaining_points[0] else -1
                
        elif r == 2 and len(next_radius_remaining_points) == 2:
            closest_point_1, closest_point_2 = pick_closest_pair(remaining_points, next_radius_remaining_points)
            visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_1)
            visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, closest_point_2)
            
            index_to_check = 0 if last_visited == next_radius_remaining_points[0] else -1

            if not skip_next and last_visited == center_point:
                visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, remaining_points[0])
          
                index_to_check = 0
                break
                
        elif last_visited == center_point and len(remaining_points) == 2:
            visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, remaining_points[0])
            
            index_to_check = 0
            
    return last_visited, index_to_check, visited_points, visited_ids

    
def bee_path(bee_data, ax, num_radii):

    radii = sorted(list(set([x['Distance from Center'] for x in bee_data])))[:num_radii]    
    center_point = {'Coordinates': (0, 0), 'Distance from Center': 0, 'Angle': 0, 'ID': '0'}
    
    first_path_best_pairs, second_path_best_pairs = find_shorter_adjacent_pairs(bee_data, ax, num_radii)
    last_visited, index_to_check, visited_points, visited_ids = handle_first_path(radii, bee_data, ax, first_path_best_pairs, second_path_best_pairs, num_radii)
    
    radius = last_visited['Distance from Center'] 
    found_first_best_pair = None
    found_second_best_pair = None
    
    for i in range(radius, num_radii):
        
        remaining_points = [f for f in bee_data if f['Distance from Center'] == i and f['ID'] ]
        remaining_radii = num_radii - i - 1
        skip_next = 'Odd' if remaining_radii % 2 != 0 else 'Even'  
        
        if index_to_check == 0:
            if  skip_next == 'Odd':
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'], reverse=True)
            else:
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'])
                found_first_best_pair = True
                
            for j, point in enumerate(remaining_points):
            
                if any(point['ID'] == pair[0]['ID'] or point['ID'] == pair[1]['ID'] for pair in first_path_best_pairs):
                    found_first_best_pair = True
                
                elif any(point['ID'] == pair[0]['ID'] or point['ID'] == pair[1]['ID'] for pair in second_path_best_pairs):
                    found_first_best_pair = False
                    continue
                    
                if found_first_best_pair:
                    visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, point)
                       
        else:                                
            if  skip_next == 'Odd':
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'])
            else:
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'], reverse=True)
                found_second_best_pair = True
                
            for j, point in enumerate(remaining_points):            
            
                if any(point['ID'] == pair[0]['ID'] or point['ID'] == pair[1]['ID'] for pair in second_path_best_pairs):
                    found_second_best_pair = True
                
                elif any(point['ID'] == pair[0]['ID'] or point['ID'] == pair[1]['ID'] for pair in first_path_best_pairs):
                    found_second_best_pair = False
                    continue
                    
                if found_second_best_pair:
                        visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, point)
                         

                        
    test = visited_points.copy()
    
    
    for r in reversed(radii):
        remaining_points = [f for f in bee_data if f['Distance from Center'] == r and f['ID'] ]
        remaining_radii = num_radii - r
        skip_next = 'Odd' if remaining_radii % 2 != 0 else 'Even'
        
        if index_to_check == 0:
            if  skip_next == 'Odd':
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'])   
            else:
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'], reverse=True)
        else:
            if  skip_next == 'Odd':
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'], reverse=True)               
            else:
                remaining_points = sorted(remaining_points, key=lambda x: x['Angle'])
                
             
        for j, point in enumerate(remaining_points):
            visited_points, visited_ids, last_visited = update_visited(visited_points, visited_ids, point)
               

    visited_points.append(center_point)
    visited_ids.append(center_point['ID'])                      
    total_distance = 0
    for i in range(len(visited_points) - 1):
        x1, y1 = visited_points[i]['Coordinates']
        x2, y2 = visited_points[i + 1]['Coordinates']
        x_coords = [x1, x2]
        y_coords = [y1, y2]
        ax.plot(x_coords, y_coords, color='black', linewidth=2)
        distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        total_distance += distance
    
    for i in range(len(test) - 1):
        x1, y1 = test[i]['Coordinates']
        x2, y2 = test[i + 1]['Coordinates']
        x_coords = [x1, x2]
        y_coords = [y1, y2]
        ax.plot(x_coords, y_coords, color='red', linewidth=2)
        

    print(f"Total distance: {total_distance}") 
    # print(visited_ids)
   

           
def draw_points(ax, points):
    for point in points:
        x, y = point["coordinates"]
        index = point["index"]


        color = 'grey'

        ax.scatter(x, y, color=color, s=25)
        ax.text(x, y, str(index), fontsize=8)

    
    ax.scatter(0, 0, color='black', zorder=5)
    ax.text(0, 0, "0", fontsize=12, ha='right', va='bottom')

# Initialize the plot
fig, ax = plt.subplots(figsize=(10,10))
plt.xlim(-11, 11)
plt.ylim(-11, 11)
ax.set_aspect('equal')

# Initialize variables
all_points = []
point_counter = 0
num_scout_bees = int(input("Enter the number of super scout bees: "))
num_radii = 11

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
    bee_path(bee_data, ax, num_radii)  

plt.show()

#-------------------------------------------------------------------------------------------------
# Initialize the plot
fig, ax = plt.subplots(figsize=(11,11))
plt.xlim(-12, 12)
plt.ylim(-12, 12)
ax.set_aspect('equal')

# Initialize variables
all_points1 = []
point_counter1 = 0

odd_num_radii = num_radii + 1
# Generate points
for r in range(1, odd_num_radii):
    points1, point_counter1 = compute_points(r, point_counter1)
    all_points1 += points1



# Plot the points
draw_points(ax, all_points1)

# Plot concentric circles and radii
for r in range(1, odd_num_radii):
    circle = plt.Circle((0, 0), r, color='gray', fill=False, linewidth=0.4)
    ax.add_artist(circle)

radii_angles1 = np.arange(0, 2*math.pi, math.radians(360/num_scout_bees))
for angle in radii_angles1:
    ax.plot([0, 10 * np.cos(angle)], [0, 10 * np.sin(angle)], color='gray', linewidth=0.4)



# Segment the points for each super scout bee
segmented_data1 = {i+1: [] for i in range(num_scout_bees)}

for point in all_points1:
    bee_num1 = point["segment"]
    segmented_data1[bee_num1].append({
        "ID": point["index"],
        "Coordinates": point["coordinates"],
        "Distance from Center": point["distance_from_center"],
        "Nectar": point["nectar_value"],
        "Angle": point["angle"]
        
    })



# Plot paths for all the super scout bees

for bee_num1, bee_data in segmented_data1.items():
    bee_path(bee_data, ax, odd_num_radii)  

plt.show()
