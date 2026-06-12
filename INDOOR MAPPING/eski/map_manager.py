# map_manager.py (Occupancy Grid Version)

import numpy as np
import matplotlib.pyplot as plt
import math

class MapManager:
    """
    Manages and updates a 2D occupancy grid map.
    This version implements statistical filtering by marking
    space as 'Free' or 'Occupied'.
    """
    def __init__(self, map_size=600, resolution=5):
        """
        Initializes the map grid in memory.
        Args:
            map_size (int): The width/height of the grid in pixels.
            resolution (float): How many cm each pixel represents.
        """
        self.map_size = map_size
        self.resolution = resolution  # cm per pixel
        
        # Grid stores log-odds, a statistical measure.
        # 0 = Unknown, >0 = Occupied, <0 = Free
        self.grid = np.zeros((map_size, map_size), dtype=np.float32)
        
        self.map_center_x = map_size // 2
        self.map_center_y = map_size // 2
        
        # Define log-odds updates
        self.log_odds_occupied = 1.0  # Confidence when we see an obstacle
        self.log_odds_free = -0.5 # Confidence when we see free space
        
        # Store robot path for final plot
        self.path_x, self.path_y = [], []
        
        self.fig = None
        self.ax = None

    def _world_to_grid(self, world_x, world_y):
        """Converts world coordinates (cm) to grid cell indices."""
        grid_x = self.map_center_x + int(round(world_x / self.resolution))
        grid_y = self.map_center_y + int(round(world_y / self.resolution))
        return grid_x, grid_y

    def update_map(self, robot_pose, distance):
        """
        Updates the occupancy grid using a single sensor reading.
        This traces a line from the robot and marks free space.
        """
        robot_x, robot_y, robot_theta = robot_pose
        
        # Store robot's position for plotting the path
        self.path_x.append(robot_x)
        self.path_y.append(robot_y)
        
        # --- 1. Mark Free Space ---
        # Ray-cast from robot up to (but not including) the obstacle
        # We step along the ray in increments of our resolution
        for d in np.arange(0, distance - self.resolution, self.resolution):
            ray_x = robot_x + d * math.cos(robot_theta)
            ray_y = robot_y + d * math.sin(robot_theta)
            
            grid_fx, grid_fy = self._world_to_grid(ray_x, ray_y)
            
            if 0 <= grid_fx < self.map_size and 0 <= grid_fy < self.map_size:
                self.grid[grid_fy, grid_fx] += self.log_odds_free

        # --- 2. Mark Occupied Space ---
        # Calculate the final obstacle coordinates
        obstacle_x = robot_x + distance * math.cos(robot_theta)
        obstacle_y = robot_y + distance * math.sin(robot_theta)
        
        grid_ox, grid_oy = self._world_to_grid(obstacle_x, obstacle_y)
        
        if 0 <= grid_ox < self.map_size and 0 <= grid_oy < self.map_size:
            self.grid[grid_oy, grid_ox] += self.log_odds_occupied
            
        # Clamp values to prevent them from growing indefinitely
        np.clip(self.grid, -20.0, 20.0, out=self.grid)

    def create_map_plot(self):
        """
        Creates and displays the final, filtered occupancy grid map.
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 10))

        # We display the grid as an image
        # 'gray' cmap: Free (<0) = White, Unknown (0) = Gray, Occupied (>0) = Black
        self.ax.imshow(self.grid, cmap='gray', origin='lower', 
                       interpolation='nearest', vmin=-5, vmax=5)
        
        # --- Plot Robot Path on Top ---
        # Convert robot's world path (cm) to grid path (pixels)
        grid_path_x = [self.map_center_x + p / self.resolution for p in self.path_x]
        grid_path_y = [self.map_center_y + p / self.resolution for p in self.path_y]
        
        self.ax.plot(grid_path_x, grid_path_y, 'r-', label='Robot Path')
        
        # Plot robot's stop/scan positions
        self.ax.plot(grid_path_x, grid_path_y, 'ro', markersize=4, label='Robot Scan Positions')
        
        self.ax.set_title("Statistically Filtered Occupancy Grid Map")
        self.ax.set_xlabel("Grid X")
        self.ax.set_ylabel("Grid Y")
        self.ax.legend()
        
        plt.show()