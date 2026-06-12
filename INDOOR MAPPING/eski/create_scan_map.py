# create_scan_map.py

import math
import matplotlib.pyplot as plt
from map_manager import MapManager # This imports the *new* map_manager

def read_scan_data(filename="room_scan_data.txt"):
    """
    Reads scan data from a file.
    Expected format per line: 'angle_degrees,distance_cm'
    Returns:
        A list of (angle_radians, distance_cm) tuples.
    """
    scan_data = []
    print(f"Reading scan data from {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        angle_deg = float(parts[0])
                        distance_cm = float(parts[1])
                        # Convert angle to radians, as math functions use radians
                        angle_rad = math.radians(angle_deg)
                        scan_data.append((angle_rad, distance_cm))
                except ValueError:
                    print(f"Skipping invalid line: {line}")
        print(f"Successfully read {len(scan_data)} data points.")
        return scan_data
        
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Make sure {filename} exists.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    # 1. Initialize the map manager (this does NOT create a plot)
    mapper = MapManager(map_size=500, resolution=2)

    # 2. Read all data from the text file
    scan_data = read_scan_data()

    if scan_data:
        print("Processing data and building map grid in memory...")
        # 3. Process all data and update the map grid
        for scan_angle, distance in scan_data:
            # Simulate a robot at (0,0) spinning in place
            robot_pose = (0, 0, scan_angle)
            mapper.update_map(robot_pose, distance)

        print("Map generation complete. Displaying map...")
        
        # 4. Now, create and show the final plot *once*
        mapper.create_map_plot()
    
    else:
        print("No data was read. Cannot generate map.")