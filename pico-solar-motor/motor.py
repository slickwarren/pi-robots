from machine import Pin, ADC
import time

# Pins
in1 = Pin(12, Pin.OUT)
in2 = Pin(13, Pin.OUT)
ldr = ADC(26)  # GP26 - analog input

# Thresholds (you may need to adjust these!)
# Higher value = more light needed to turn on
SUNRISE_THRESHOLD = 30000  # Turn on when light > this
SUNSET_THRESHOLD = 10000   # Turn off when light < this

# Hysteresis - prevents rapid flipping at twilight
HYSTERESIS = 5000

def read_light():
    """Read LDR value (0-65535, higher = more light)"""
    return ldr.read_u16()

def motor_forward():
    in1.value(1)
    in2.value(0)

def motor_reverse():
    in1.value(0)
    in2.value(1)

def motor_off():
    in1.value(0)
    in2.value(0)

# State tracking
motor_running = False

print("Light-controlled motor starting...")
print(f"Sunrise threshold: {SUNRISE_THRESHOLD}")
print(f"Sunset threshold: {SUNSET_THRESHOLD}")

try:
    while True:
        light_level = read_light()
        
        # Check if it's dark (below sunset threshold)
        if motor_running and light_level < SUNSET_THRESHOLD:
            print(f"Dark ({light_level}) - turning motor OFF")
            motor_off()
            motor_running = False
        
        # Check if it's light enough (above sunrise threshold)
        elif not motor_running and light_level > SUNRISE_THRESHOLD:
            print(f"Light ({light_level}) - turning motor ON (forward)")
            motor_forward()
            motor_running = True
            
            # Run for 10 seconds then reverse
            time.sleep(10)
            print("Reversing...")
            motor_reverse()
            time.sleep(10)
            motor_off()
            motor_running = False
            print("Motor stopped, waiting for next sunrise...")
        
        # Debug output every minute (optional)
        if int(time.time()) % 60 == 0:
            print(f"Light level: {light_level}, Motor: {'ON' if motor_running else 'OFF'}")
        
        time.sleep(5)  # Check every 5 seconds

except KeyboardInterrupt:
    motor_off()
    print("Stopped")