from gpiozero import Robot
from time import sleep

class MotorControl:
    """
    Manages the robot's basic movements using the gpiozero library.
    Assumes a standard 2-wheel robot with a motor driver like the L298N.
    """
    def __init__(self, left_pins=(7, 8), right_pins=(9, 10)):
        """
        Initializes the Robot instance with the specified GPIO pins.
        Args:
            left_pins (tuple): A tuple containing (forward_pin, backward_pin) for the left motor.
            right_pins (tuple): A tuple containing (forward_pin, backward_pin) for the right motor.
        """
        # Adjust these pin numbers based on your actual wiring to the motor driver.
        self.robot = Robot(left=left_pins, right=right_pins)

    def move_forward(self, speed=0.5):
        """Moves the robot forward continuously at a given speed."""
        print("Action: Moving forward")
        self.robot.forward(speed)

    def turn_left(self, speed=0.4):
        """Turns the robot left on the spot continuously."""
        print("Action: Turning left")
        self.robot.left(speed)

    def turn_right(self, speed=0.4):
        """Turns the robot right on the spot continuously."""
        print("Action: Turning right")
        self.robot.right(speed)

    def stop(self):
        """Stops all motor movement."""
        print("Action: Stopping")
        self.robot.stop()