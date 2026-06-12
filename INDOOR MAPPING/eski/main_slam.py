import time
import math
from motor_control import MotorControl
from sensor_reader import SensorReader
from odometry import Odometry
from map_manager import MapManager

# --- CONFIGURATION ---
# Physical robot parameters (measure these from your robot)
WHEEL_RADIUS_CM = 3.5
WHEEL_BASE_CM = 15.0
TICKS_PER_REVOLUTION = 400 

# Exploration parameters
OBSTACLE_THRESHOLD_CM = 30.0 # How close to get to a wall before turning
MOVE_DURATION_S = 1.0
TURN_DURATION_S = 0.5

# --- MOCKUP FUNCTION for odometry ---
# !! IMPORTANT !!
# Replace this with your actual hardware interrupt functions that read encoder ticks.
def get_encoder_ticks_since_last_call():
    # This is a placeholder. In a real robot, this function would return the
    # actual number of ticks counted by the left and right encoders since the
    # last time it was called.
    # For this demo, we will pretend the robot moved perfectly.
    # This is the BIGGEST simplification in this entire demo code.
    return (100, 100) # (delta_left_ticks, delta_right_ticks) for moving forward

if __name__ == "__main__":
    # --- INITIALIZATION ---
    motors = MotorControl()
    sensor = SensorReader()
    odometry = Odometry(WHEEL_RADIUS_CM, WHEEL_BASE_CM, TICKS_PER_REVOLUTION)
    mapper = MapManager(map_size=200, resolution=2)

    print("Starting SLAM and exploration process. Press Ctrl+C to stop.")
    time.sleep(2)

    try:
        # --- MAIN LOOP ---
        while True:
            # 1. Sense: Get a reading from the distance sensor
            distance = sensor.get_filtered_distance()
            print(f"Sensor reading: {distance:.1f} cm")
            
            # 2. Localize: Get the current pose from odometry
            # In a real robot, you would call your tick-reading function first
            # delta_ticks = get_encoder_ticks_since_last_call()
            # odometry.update(delta_ticks[0], delta_ticks[1])
            current_pose = odometry.get_pose()
            
            # 3. Map: Update the map with the new information
            mapper.update_map(current_pose, distance)
            
            # 4. Visualize: Show the updated map
            mapper.visualize(current_pose)

            # 5. Act: Decide on the next action (simple exploration logic)
            if distance < OBSTACLE_THRESHOLD_CM:
                # Obstacle detected, turn left
                motors.turn_left()
                time.sleep(TURN_DURATION_S)
                motors.stop()
                # Manually update odometry for this simple demo
                odometry.update(delta_left_ticks=-50, delta_right_ticks=50) 
            else:
                # Path is clear, move forward
                motors.move_forward()
                time.sleep(MOVE_DURATION_S)
                motors.stop()
                # Manually update odometry for this simple demo
                odometry.update(delta_left_ticks=100, delta_right_ticks=100)

    except KeyboardInterrupt:
        print("Process stopped by user.")
    finally:
        motors.stop()
        # Keep the final map displayed
        input("Press Enter to close the map.")