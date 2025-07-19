import time
import board
import gpiod
from adafruit_motorkit import MotorKit

# Initialize Motor HAT via I2C
kit = MotorKit(i2c=board.I2C())

# GPIO chip and line setup for gpiod
CHIP = "gpiochip0"
TRIG = 23
ECHO = 24

chip = gpiod.Chip(CHIP)
trig_line = chip.get_line(TRIG)
echo_line = chip.get_line(ECHO)

# Request lines
trig_line.request(consumer="ultrasonic", type=gpiod.LINE_REQ_DIR_OUT)
echo_line.request(consumer="ultrasonic", type=gpiod.LINE_REQ_DIR_IN)

# Ultrasonic distance function
def get_distance():
    trig_line.set_value(0)
    time.sleep(0.1)

    trig_line.set_value(1)
    time.sleep(0.00001)
    trig_line.set_value(0)

    timeout = time.time() + 1  # 1 second timeout

    # Wait for echo to go HIGH
    while echo_line.get_value() == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return -1

    # Wait for echo to go LOW
    while echo_line.get_value() == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return -1

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Motor control
def move_forward():
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = 1.0

def move_backward():
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = -1.0

def turn_left():
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = 1.0

def turn_right():
    kit.motor1.throttle = 1.0
    kit.motor2.throttle = -1.0

def stop():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

# Main drive logic
def drive():
    try:
        while True:
            distance = get_distance()
            print(f"Distance: {distance} cm")

            if distance < 0:
                print("Sensor timeout")
                stop()
            elif distance < 20:
                stop()
                print("Object detected! Stopping...")
                time.sleep(1)
                turn_left()
                print("Turning left")
                time.sleep(1)
                move_forward()
                print("Moving forward")
            else:
                move_forward()
                print("Moving forward")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting program.")
        stop()
        trig_line.release()
        echo_line.release()

if __name__ == "__main__":
    drive()
