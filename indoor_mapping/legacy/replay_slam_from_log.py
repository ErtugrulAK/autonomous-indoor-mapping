# replay_slam_from_log.py

import math
import matplotlib.pyplot as plt
from map_manager import MapManager # Imports our updated map_manager

def read_slam_log(filename="slam_log_data.txt"):
    """
    Reads a full SLAM log file.
    Expected format per line: 'x,y,theta_rad,distance_cm'
    Returns:
        A list of (pose_tuple, distance_cm) tuples.
    """
    log_data = []
    print(f"Reading SLAM log from {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue  # Skip comments or empty lines
                try:
                    parts = line.split(',')
                    if len(parts) == 4:
                        x = float(parts[0])
                        y = float(parts[1])
                        theta = float(parts[2])
                        distance = float(parts[3])
                        
                        pose = (x, y, theta)
                        log_data.append((pose, distance))
                except ValueError:
                    print(f"Skipping invalid line: {line}")
        print(f"Successfully read {len(log_data)} data points.")
        return log_data
        
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
    slam_log = read_slam_log(filename="merged_slam_log.txt")

    if slam_log:
        print("Processing log data and building map...")
        # 3. Process all data and update the map grid
        for robot_pose, measured_distance in slam_log:
            # robot_pose is (x, y, theta)
            mapper.update_map(robot_pose, measured_distance)

        print("Map generation complete. Displaying map...")
        
        # 4. Now, create and show the final plot *once*
        mapper.create_map_plot()
    
    else:
        print("No data was read. Cannot generate map.")