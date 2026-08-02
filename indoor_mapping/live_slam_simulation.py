# live_slam_simulation.py
# Performs real-time SLAM simulation in a 2D virtual environment.
# Usage: python live_slam_simulation.py
# Dependencies: numpy, matplotlib

import numpy as np
import matplotlib.pyplot as plt
import math
import time

class VirtualWorld:
    """
    Creates a simulated 2D room environment represented as a grid array.
    Grid representation: 1 = Wall/Obstacle, 0 = Free Space.
    """
    def __init__(self, width_cm, height_cm):
        self.width = width_cm
        self.height = height_cm
        # Initialize a 2D array filled with zeros (1cm = 1 pixel)
        self.grid = np.zeros((height_cm, width_cm), dtype=np.uint8)

        # Construct outer boundary walls (1 = Wall)
        self.grid[10:height_cm-10, 10] = 1            # Left wall
        self.grid[10:height_cm-10, width_cm-10] = 1   # Right wall
        self.grid[10, 10:width_cm-10] = 1            # Top wall
        self.grid[height_cm-10, 10:width_cm-10] = 1   # Bottom wall
        
        # Place a central obstacle
        self.grid[150:200, 200:250] = 1
        
        # Construct an internal alcove (L-shape feature)
        self.grid[100:200, 10] = 0   # Opening in left wall
        self.grid[100, 10:100] = 1   # Alcove top wall
        self.grid[200, 10:100] = 1   # Alcove bottom wall
        self.grid[100:200, 99] = 1   # Alcove inner back wall


class SimulatedRobot:
    """
    Simulated mobile robot capable of autonomous motion and distance sensor measurement generation.
    """
    def __init__(self, start_x, start_y, virtual_world):
        self.x = start_x
        self.y = start_y
        self.theta = math.pi / 2  # Orientation angle in radians (facing upwards)
        self.world = virtual_world
        
        self.move_speed = 2.0               # Linear velocity: 2 cm per step
        self.turn_speed = math.radians(5)   # Angular velocity: 5 degrees per step
        
        # Finite State Machine state for exploration
        self.state = "moving_forward"

    def scan(self, max_range=400):
        """
        Sensor Raycasting Simulation.
        Casts a ray along the robot's heading direction until encountering an obstacle (1).
        """
        for distance in range(1, max_range):
            # Compute ray endpoint coordinates
            ray_x = int(self.x + distance * math.cos(self.theta))
            ray_y = int(self.y + distance * math.sin(self.theta))

            # Out of bounds check
            if not (0 <= ray_x < self.world.width and 0 <= ray_y < self.world.height):
                return distance  # Return max range if boundary exceeded
            
            # Obstacle collision check
            if self.world.grid[ray_y, ray_x] == 1:
                return distance  # Return measured distance to obstacle
        
        return max_range  # No obstacle detected within max range

    def move_and_scan(self):
        """
        Executes robot navigation control logic and sensor acquisition.
        """
        # 1. Perform range measurement from current pose
        distance = self.scan()

        # 2. Obstacle avoidance logic
        if distance < 20:  # Proximity threshold trigger
            self.state = "turning_left"
        else:
            self.state = "moving_forward"
            
        # 3. Apply state motion updates
        if self.state == "moving_forward":
            self.x += self.move_speed * math.cos(self.theta)
            self.y += self.move_speed * math.sin(self.theta)
        elif self.state == "turning_left":
            self.theta += self.turn_speed
            
        return distance


# --- Main Simulation Script ---

if __name__ == "__main__":
    
    # 1. Initialize Environment and Robot
    world_cm = 500  # 500cm x 500cm room dimensions (5m x 5m)
    world = VirtualWorld(world_cm, world_cm)
    robot = SimulatedRobot(start_x=250, start_y=250, virtual_world=world)

    # 2. Configure Interactive Matplotlib Plotting
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot element initialization for optimized updates
    map_plot, = ax.plot([], [], 'r.', markersize=0.5)  # Mapped wall points (red dots)
    robot_plot, = ax.plot([], [], 'bo', markersize=5)  # Robot pose indicator
    
    ax.set_title("Live SLAM Simulation (Arena Recording)")
    ax.set_xlabel("X Position (cm)")
    ax.set_ylabel("Y Position (cm)")
    ax.set_xlim(0, world_cm)
    ax.set_ylim(0, world_cm)
    ax.set_aspect('equal')
    ax.grid(True)

    # Global point cloud storage
    map_points_x = []
    map_points_y = []

    print("Simulation initialized. Close the window to terminate.")

    # 3. Execution Loop
    try:
        while True:
            # Advance robot state and acquire sensor reading
            distance = robot.move_and_scan()
            
            # Compute global obstacle coordinates (x, y)
            obstacle_x = robot.x + distance * math.cos(robot.theta)
            obstacle_y = robot.y + distance * math.sin(robot.theta)
            
            # Append measurement to point cloud
            map_points_x.append(obstacle_x)
            map_points_y.append(obstacle_y)
            
            # Efficient plot data update
            map_plot.set_data(map_points_x, map_points_y)
            robot_plot.set_data(robot.x, robot.y)
            
            plt.pause(0.001)

    except plt.TclError:
        print("Simulation GUI window closed.")
    except KeyboardInterrupt:
        print("Simulation interrupted by user.")
    finally:
        plt.ioff()
        print("Simulation complete.")