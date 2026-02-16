#!/usr/bin/env python3
import time
import board
from adafruit_motorkit import MotorKit

# Initialize the Motor HAT
kit = MotorKit(i2c=board.I2C())

try:
    while True:
        print("Motor 1 ON (forward)")
        kit.motor1.throttle = 1.0     # full speed forward
        kit.motor2.throttle = 1.0     # full speed forward
        time.sleep(5)

        print("Motor 1 OFF")
        kit.motor1.throttle = 0       # stop motor
        kit.motor2.throttle = 0     
        time.sleep(5)

        print("Motor 1 ON (reverse)")
        kit.motor1.throttle = -1.0    # full speed reverse
        kit.motor2.throttle = -1.0    # full speed reverse
        time.sleep(5)

        print("Motor 1 OFF")
        kit.motor1.throttle = 0       # stop again
        kit.motor2.throttle = 0       # stop again
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping and cleaning up...")
    kit.motor1.throttle = 0
