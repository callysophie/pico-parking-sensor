#Parking proximity sensor demo using a Raspberry Pi Pico SR04 ultrasonic sensor and green, yellow, red LEDs
#comment out the prints after adjusting everything for your own use

#imports Pin class to control GPIO pins and utime library for the time based functions required
from machine import Pin
import utime

#creates two objects the trigger and echo pins for ultrasonic sensor
#any GPIO pins will work - these are GPIO pin numbers not pinout numbers
#ground pin on sensor to any ground
#VCC pin on sensor to VBUS, pin 40 on Pico to get 5V from USB power
#if you are not using USB power this will not be powered so you'll need 5V from somewhere
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

#sets the GPIO pins for the three LEDs
#use a resistor on positive LED terminals - I used 220 ohm resistors
led_red = machine.Pin(10, machine.Pin.OUT)
led_yellow = machine.Pin(11, machine.Pin.OUT)
led_green = machine.Pin(14, machine.Pin.OUT)

#creates a function
def ultra():
   #turns off trigger, then waits 2 microseconds
   trigger.low()
   utime.sleep_us(2)
   #turns on trigger for 5 microseconds
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   #creates a loop that checks the echo pin - if nothing is received, updates a variable called signaloff
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   #creates another loop that checks echo pin - if something is received, updates a variable called signalon
   while echo.value() == 1:
       signalon = utime.ticks_us()
   #creates a variable called timepassed which stores the value of the time for the pulse to return as an echo
   timepassed = signalon - signaloff
   #creates a variable called distance to store value of timepassed as a distance in centimetres
   distance = (timepassed * 0.0343) / 2
   #creates an if statement to turn on red LED if the distance is under 5cm
   if distance < 5:
        print("Near")
        led_red.value(1)
        led_yellow.value(0)
        led_green.value(0)
        utime.sleep(0.1)
   #creates an if statement to turn on yellow LED if the distance is under 10cm
   elif distance < 10:
        print("Medium")
        led_yellow.value(1)
        led_green.value(0)
        led_red.value(0)
        utime.sleep(0.1)
   #creates an if statement to turn on green LED if the distance is under 20cm
   elif distance < 20:
        print("Far")
        led_green.value(1)
        led_red.value(0)
        led_yellow.value(0)
        utime.sleep(0.1)
   #creates an if statement to turn off all LEDs if the distance is equal to or over 20cm
   elif distance >= 20:
        led_green.value(0)
        led_yellow.value(0)
        led_red.value(0)
        utime.sleep(0.1)
   #prints distance in console
   print("The distance from object is ",distance,"cm")

#creates a loop to run the ultra function ten times a second
while True:
   ultra()
   utime.sleep(0.1)