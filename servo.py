
import RPi.GPIO as GPIO
import time
#GPIO.cleanup()
servoPIN =26 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) 
try:
  while True:
    p.ChangeDutyCycle(1)
    time.sleep(1)
    p.ChangeDutyCycle(12)
    time.sleep(1)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
