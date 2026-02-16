from machine import Pin, ADC
import time

ldr = ADC(26)

while True:
    print(f"Light: {ldr.read_u16()}")
    time.sleep(1)