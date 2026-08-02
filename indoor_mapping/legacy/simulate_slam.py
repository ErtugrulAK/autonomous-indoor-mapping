# simulate_slam.py
import numpy as np
import math
import time

# Import our existing helper classes
from odometry import Odometry
from map_manager import MapManager

# --- CONFIGURATION ---
WHEEL_RADIUS_CM = 3.5
WHEEL_BASE_CM = 15.0
TICKS_PER_REVOLUTION = 400 
OBSTACLE_THRESHOLD_CM = 40.0 # How close to get to a wall before turning


class VirtualWorld:
    """Creates a simple 2D grid world for the robot to navigate."""
    def __init__(self, size=200):
        self.size = size
        self.grid = np.zeros((size, size), dtype=np.uint8)
        # Create a U-shaped room
        self.grid[10:size-10, 10] = 1  # Left wall
        self.grid[10:size-10, size-10] = 1 # Right wall
        self.grid[10, 10:size-10] = 1  # Top wall
        # Add an obstacle in the middle
        self.grid[size//2 - 10 : size//2 + 10, size//2 - 5 : size//2 + 5] = 1

    def get_simulated_distance(self, pose):
        """Simulates a sensor reading by raycasting in the virtual world."""
        x, y, theta = pose
        
        # Translate robot's world coordinate (cm) to grid coordinate (pixels)
        grid_x = x + self.size // 2
        grid_y = y + self.size // 2
        
        for distance in range(1, 150): # Max range 150cm
            ox = grid_x + distance * math.cos(theta)
            oy = grid_y + distance * math.sin(theta)
            
            if not (0 <= ox < self.size and 0 <= oy < self.size):
                return distance # Out of bounds
            
            if self.grid[int(oy), int(ox)] == 1:
                return distance # Hit a wall
                
        return 150.0 # No obstacle found


class SimulatedRobot:
    """A simulated robot that moves and uses odometry."""
    def __init__(self):
        # Robot's *true* position in the world
        self.true_x = 0.0
        self.true_y = 0.0
        self.true_theta = math.pi / 2 # Start facing up

        # Robot's *estimated* position using odometry
        self.odometry = Odometry(WHEEL_RADIUS_CM, WHEEL_BASE_CM, TICKS_PER_REVOLUTION)
        
    def get_estimated_pose(self):
        return self.odometry.get_pose()

    def get_true_pose(self):
        return (self.true_x, self.true_y, self.true_theta)

    def _move(self, distance_cm, angle_rad):
        """Internal function to update true pose and odometry."""
        
        # 1. Update true pose (perfect movement)
        self.true_x += distance_cm * math.cos(self.true_theta)
        self.true_y += distance_cm * math.sin(self.true_theta)
        self.true_theta += angle_rad

        # 2. Simulate noisy encoder ticks for odometry
        # This simulates the robot's wheels slipping, etc.
        noise = np.random.uniform(0.95, 1.05)
        
        dist_per_tick = self.odometry.distance_per_tick
        
        if angle_rad == 0: # Moving forward
            delta_ticks_left = (distance_cm * noise) / dist_per_tick
            delta_ticks_right = (distance_cm * noise) / dist_per_tick
        else: # Turning
            # Calculate ticks needed to turn
            turn_dist = (angle_rad * self.odometry.wheel_base) / 2.0
            delta_ticks_right = (turn_dist * noise) / dist_per_tick
            delta_ticks_left = -delta_ticks_right
            
        # 3. Update odometry with noisy ticks
        self.odometry.update(delta_ticks_left, delta_ticks_right)


    def move_forward(self):
        print("Action: Moving forward 5 cm")
        self._move(distance_cm=5.0, angle_rad=0.0)

    def turn_left(self):
        print("Action: Turning left 15 degrees")
        self._move(distance_cm=0.0, angle_rad=math.radians(15))


if __name__ == "__main__":
    # --- INITIALIZATION ---
    print("Initializing simulation...")
    world = VirtualWorld()
    robot = SimulatedRobot()
    mapper = MapManager(map_size=200, resolution=1) # 1cm per pixel

    print("Starting SLAM simulation. This will take a moment...")

    try:
        # --- MAIN SIMULATION LOOP ---
        for i in range(150): # Run for 150 steps
            
            # 1. Sense: Get distance from the *virtual world* using *true* pose
            true_pose = robot.get_true_pose()
            distance = world.get_simulated_distance(true_pose)
            
            # 2. Localize: Get the *estimated* pose from *odometry*
            estimated_pose = robot.get_estimated_pose()
            
            # 3. Map: Update the map using the *estimated* pose
            mapper.update_map(estimated_pose, distance)
            
            # 4. Act: Decide what to do next
            if distance < OBSTACLE_THRESHOLD_CM:
                robot.turn_left()
            else:
                robot.move_forward()
            
            time.sleep(0.01) # Small pause

    except KeyboardInterrupt:
        print("Simulation stopped.")

    print("Simulation complete. Displaying map...")
    # 5. Visualize: Show the final map
    mapper.create_map_plot()