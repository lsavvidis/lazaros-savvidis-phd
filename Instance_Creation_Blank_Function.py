import matplotlib.pyplot as plt
import numpy as np
import math
import random

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
    
    # segmentation
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
    point["nectar_value"] = random.randint(0, 100)  # Nectar values ranges from 0 to 100
    return point


def compute_points(r, point_counter):
    num_chords, _ = calculate_chords(r)
    angles = np.linspace(0, 2*math.pi, num_chords, endpoint=False)
    nectar_values = [random.randint(0, 100) for _ in range(num_chords)]
    points = [create_point(r, angle, i, point_counter, nectar_values[i]) for i, angle in enumerate(angles)]
    return points, point_counter + num_chords 



def main_function(bee_data, ax):

    bee =  1   
    
    return bee
    
    
    
    
    
       



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


for bee_num, bee_data in segmented_data.items():
    main_function(bee_data, ax)  

plt.show()