from gpiozero import DistanceSensor
import collections

class SensorReader:
    """
    Reads and filters data from an ultrasonic distance sensor (e.g., HC-SR04).
    Uses a median filter to reduce noise and outliers in the sensor readings.
    """
    def __init__(self, echo_pin=24, trigger_pin=18, filter_window_size=5):
        """
        Initializes the distance sensor and the filter window.
        Args:
            echo_pin (int): The GPIO pin number for the sensor's Echo pin.
            trigger_pin (int): The GPIO pin number for the sensor's Trigger pin.
            filter_window_size (int): The number of recent readings to use for the median filter.
        """
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)
        self.median_window = collections.deque(maxlen=filter_window_size)

    def _median_filter(self, new_measurement):
        """Private method to apply the median filter."""
        self.median_window.append(new_measurement)
        sorted_window = sorted(self.median_window)
        median_index = len(sorted_window) // 2
        return sorted_window[median_index]

    def get_filtered_distance(self):
        """
        Gets a new reading from the sensor, applies the filter, and returns the result.
        Returns:
            float: The filtered distance in centimeters.
        """
        raw_distance_cm = self.sensor.distance * 100
        filtered_distance = self._median_filter(raw_distance_cm)
        return filtered_distance