from signal import pause
from gpiozero import DistanceSensor
from signal import pause
from bluedot import BlueDot
import RPi.GPIO as GPIO
import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from gpiozero import LED
import subprocess
#PARA SERVO Y BLUEDOT
servoPIN =26 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p2 = GPIO.PWM(servoPIN, 50) 
p2.start(12) 

bd=BlueDot()

#PARA LEDS
#¬∑ultrasonico
led_rojo=LED(10)
#servo
led_verdeS=LED(22)
#ultrasonico
led_verdeU=LED(9)
#PARA sensor
ini=23
ena=24
trig=17
echo=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ini,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
p=GPIO.PWM(ena,1000)
p.start(25)
#------------------------------------------para el oled
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)
def dpad(pos):
    if pos.top:
        p2.ChangeDutyCycle(1)
        time.sleep(0.5)
        print("abierto")
        led_verdeS.on()
    elif pos.bottom:
        p2.ChangeDutyCycle(12)
        time.sleep(0.5)
        print("cerrado")
        led_verdeS.off()

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)


mensaje="Se ha detectado el vaso"
#BOTON VASO
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
draw.text((0, 0), "ELIGE SABOR " , font=font, fill=255)
# Display image
oled.image(image)
oled.show()
time.sleep(.1)

sabor="NINGUNO"

#bd.wait_for_press()
bd.when_pressed = dpad

try:
    while True:
        #bd.when_pressed = dpad
        #--ACCION OLED
        #--ACCION SENSOR
        GPIO.output(trig,GPIO.LOW)
        time.sleep(0.5)

        GPIO.output(trig,GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig,GPIO.LOW)

        while True:
            pulso_inicio=time.time()
            if(GPIO.input(echo)==GPIO.HIGH):
                break

        while True:
            pulso_fin=time.time()
            if(GPIO.input(echo)==GPIO.LOW):
                break 
        duracion=pulso_fin-pulso_inicio
        distancia=34300*duracion/2
        print("Distancia :",distancia)
        #---ACCION MOTOR
        if distancia<7:
           led_verdeU.on()
           led_rojo.off()
           print("sirviendo refresco")  
           GPIO.output(ini,GPIO.HIGH)
           # Draw a black filled box to clear the image.
           draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
           draw.text((0, 0), "Sirviendo refresco" , font=font, fill=255)
           # Display image
           oled.image(image)
           oled.show()
           time.sleep(.1)
        else:
           led_verdeU.off()
           led_rojo.on()
           print("esperando refresco")
           GPIO.output(ini,GPIO.LOW)
           # Draw a black filled box to clear the image.
           draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
           draw.text((0, 0), "Quitaste el vaso " , font=font, fill=255)
#             Display image
           oled.image(image)
           oled.show()
           time.sleep(.1)


except KeyboardInterrupt:
    GPIO.cleanup()
    p.stop()





#		requests.post('https://api.telegram.org/bot'+API_TOKEN+'/sendMessage',data={'chat_id':'-779005981','text':mensaje,'parse_mode':'HTML'})



#PI_TOKEN = '5198248925:AAHSnTII8zvxnV7yA76RQziHT0DFNdGsGmw'
#bot = telebot.TeleBot(API_TOKEN)


