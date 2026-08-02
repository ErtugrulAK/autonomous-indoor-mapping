import math

class Odometry:
    """
    Tracks the robot's position (x, y) and orientation (theta) using wheel encoder data.
    This is a simplified model and requires integration with hardware interrupts to read encoder ticks.
    """
    def __init__(self, wheel_radius_cm, wheel_base_cm, ticks_per_revolution):
        """
        Initializes the odometry with the robot's physical parameters.
        Args:
            wheel_radius_cm (float): The radius of the robot's wheels in cm.
            wheel_base_cm (float): The distance between the centers of the two wheels in cm.
            ticks_per_revolution (int): The number of ticks the encoder generates for one full wheel revolution.
        """
        # Robot's physical constants
        self.wheel_radius = wheel_radius_cm
        self.wheel_base = wheel_base_cm
        self.distance_per_tick = (2 * math.pi * self.wheel_radius) / ticks_per_revolution

        # Robot's current state (pose)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  # Angle in radians

    def update(self, delta_left_ticks, delta_right_ticks):
        """
        Updates the robot's pose based on the number of ticks that have passed since the last update.
        Args:
            delta_left_ticks (int): Number of ticks from the left encoder.
            delta_right_ticks (int): Number of ticks from the right encoder.
        """
        distance_left = delta_left_ticks * self.distance_per_tick
        distance_right = delta_right_ticks * self.distance_per_tick

        delta_distance = (distance_left + distance_right) / 2
        delta_theta = (distance_right - distance_left) / self.wheel_base

        self.x += delta_distance * math.cos(self.theta + delta_theta / 2.0)
        self.y += delta_distance * math.sin(self.theta + delta_theta / 2.0)
        self.theta += delta_theta
        
        # Normalize theta to be within -pi to pi
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi

    def get_pose(self):
        """Returns the current estimated pose."""
        return (self.x, self.y, self.theta)