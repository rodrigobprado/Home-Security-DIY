import time
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DefenseController:
    STATE_IDLE = "idle"
    STATE_WARNING = "warning"
    STATE_ARMED = "armed"
    STATE_ACTIVE = "active"

    def __init__(self, pin_code="1234"):
        self.state = self.STATE_IDLE
        self.pin_code = pin_code
        self.last_arm_time = 0
        self.ARM_TIMEOUT = 60 # Seconds
        logging.info("Defense Controller Initialized")

    def get_status(self):
        # Auto-disarm check
        if self.state == self.STATE_ARMED and (time.time() - self.last_arm_time > self.ARM_TIMEOUT):
            self.disarm("Timeout")
            
        return {
            "state": self.state,
            "armed_time_remaining": max(0, int(self.ARM_TIMEOUT - (time.time() - self.last_arm_time))) if self.state == self.STATE_ARMED else 0
        }

    def set_warning(self, level=1):
        """Activates warning lights/sound (Non-Lethal Level 1-2)"""
        if self.state == self.STATE_ACTIVE:
            logging.warning("Cannot downgrade from Active to Warning directly. Disarm first.")
            return False
            
        self.state = self.STATE_WARNING
        logging.info(f"Defense State: WARNING (Level {level}) - Lights/Sound ON")
        # Trigger hardware (GPIO/PWM) here
        return True

    def arm(self, pin):
        """Arms the active defense mechanism (Level 3). Requires PIN."""
        if pin == self.pin_code:
            self.state = self.STATE_ARMED
            self.last_arm_time = time.time()
            logging.warning("Defense State: ARMED - READY TO FIRE. DISARM IF NOT INTENDED.")
            return True
        else:
            logging.error("Arming Failed: Invalid PIN")
            return False

    def disarm(self, reason="Manual"):
        """Disarms system immediately."""
        self.state = self.STATE_IDLE
        logging.info(f"Defense State: IDLE (Reason: {reason})")
        # Cut power to actuator relay here
        return True

    def trigger(self):
        """Fires the active defense mechanism. Must be ARMED first."""
        if self.state == self.STATE_ARMED:
            # Check timeout again just in case
            if time.time() - self.last_arm_time > self.ARM_TIMEOUT:
                self.disarm("Timeout during trigger")
                return False

            self.state = self.STATE_ACTIVE
            logging.critical("Defense State: ACTIVE - FIRING DEFENSE MECHANISM")
            # Activate Solenoid/Pump/Spray
            return True
        else:
            logging.error(f"Trigger Failed: System is {self.state}, must be ARMED.")
            return False

# Example Usage / Test
if __name__ == "__main__":
    ctrl = DefenseController("9999")
    
    # 1. Normal Warning
    ctrl.set_warning(1)
    print(ctrl.get_status())
    
    # 2. Try to fire without arming
    ctrl.trigger()
    
    # 3. Arm with wrong PIN
    ctrl.arm("0000")
    
    # 4. Arm with correct PIN
    if ctrl.arm("9999"):
        print(ctrl.get_status())
        time.sleep(1)
        # 5. Fire
        ctrl.trigger()
        print(ctrl.get_status())
        
    # 6. Disarm
    ctrl.disarm()
