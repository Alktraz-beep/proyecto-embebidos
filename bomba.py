import RPi.GPIO as GPIO

ini=23
ena=24


GPIO.setmode(GPIO.BCM)
GPIO.setup(ini,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
p=GPIO.PWM(ena,1000)
p.start(25)


try:
    while True:
        print("sirv refresco")
        GPIO.output(ini,GPIO.HIGH)
except KeyboardInterrupt:
    GPIO.cleanup()
