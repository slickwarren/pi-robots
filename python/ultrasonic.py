import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

# Initialize Motor HAT via I2C
kit = MotorKit(i2c=board.I2C())

# Pin setup for ultrasonic sensor
TRIG = 23
ECHO = 24

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Ultrasonic distance function
def get_distance():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.1)

    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Motor control using Motor HAT
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

            if distance < 20:
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
        GPIO.cleanup()

if __name__ == "__main__":
    drive()
