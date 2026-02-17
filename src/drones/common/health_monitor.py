import time
import logging

class HealthMonitor:
    def __init__(self, battery_threshold=20, timeout_threshold=5.0):
        self.battery_threshold = battery_threshold
        self.timeout_threshold = timeout_threshold # Seconds
        self.last_heartbeat = time.time()
        self.battery_level = 100
        self.sensors_ok = True
        
    def update_heartbeat(self):
        self.last_heartbeat = time.time()
        
    def update_battery(self, level):
        self.battery_level = level
        
    def report_sensor_failure(self, sensor_name):
        logging.error(f"Sensor Failure Reported: {sensor_name}")
        self.sensors_ok = False
        
    def check_health(self):
        """
        Returns (status_bool, reason_string)
        True = Healthy
        False = Critical Failure (Stop immediately)
        """
        # 1. Connection Timeout
        if time.time() - self.last_heartbeat > self.timeout_threshold:
            return False, "Connection Timeout (Heartbeat lost)"
            
        # 2. Battery Critical
        if self.battery_level < self.battery_threshold:
            return False, f"Critical Battery ({self.battery_level}%)"
            
        # 3. Sensor Failure
        if not self.sensors_ok:
            return False, "Sensor Failure Detected"
            
        return True, "OK"
