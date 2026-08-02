import matplotlib.pyplot as plt
import numpy as np

def load_map_points(filename="arena_data.txt"):
    """
    Reads 2D spatial point coordinates (x, y) from a structured plain-text file.
    """
    x_points = []
    y_points = []
    
    print(f"Loading map dataset from file: {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue  # Skip comments and empty lines
                
                try:
                    parts = line.split(',')
                    if len(parts) == 2:
                        x_points.append(float(parts[0]))
                        y_points.append(float(parts[1]))
                except ValueError:
                    print(f"Skipping malformed line: {line}")
                    
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' was not found.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while reading file: {e}")
        return None, None

    print(f"Successfully loaded {len(x_points)} spatial map points.")
    return x_points, y_points

if __name__ == "__main__":
    
    # 1. Load point cloud data from file
    x_coords, y_coords = load_map_points()
    
    if x_coords:
        print("Rendering final occupancy map...")
        
        # 2. Initialize figure canvas
        plt.figure(figsize=(10, 10))
        
        # 3. Scatter plot raw obstacle boundary coordinates
        plt.scatter(x_coords, y_coords, s=1, c='red', label='Obstacle Boundaries (Raw Data)')
        
        # 4. Configure axis parameters and plot aesthetic properties
        plt.title("Final Occupancy Map Output (Arena Recording)", fontsize=16)
        plt.xlabel("X Position (cm)")
        plt.ylabel("Y Position (cm)")
        plt.grid(True)
        plt.axis('equal')
        
        # Plot initial robot origin position
        plt.plot(250, 250, 'bo', markersize=8, label='Robot Origin Pose') 
        plt.legend()
        
        # Render plot modal
        plt.show()
        
    else:
        print("Failed to display map: Dataset loading incomplete.")