#!/usr/bin/env python3
import RPi.GPIO as GPIO
from subprocess import call

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# GPIO headers for orange LEDs
oled1=10
oled2=12
oled3=16
oled4=18
oled5=22

# RGB LED, green header/red header/blue header
rled=24
gled=26
bled=19

# Toggle switches
switch1=29
switch2=31
switch3=33
switch4=35
switch5=37

# Big Red Button
bigredbutton=40

# Make lists out of all that nonsense
outputs = [ oled1, oled2, oled3, oled4, oled5, gled, rled, bled ] 
inputs = [ switch1, switch2, switch3, switch4, switch5, bigredbutton ]

# Setup input/output GPIOs.
GPIO.setup (outputs, GPIO.OUT)
GPIO.setup (inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Turn off all LEDs
#for led in outputs:
#    GPIO.output(led, GPIO.HIGH)

# Turn RGB LED to green.
GPIO.output(rled, GPIO.HIGH)
GPIO.output(bled, GPIO.HIGH)
GPIO.output(gled, GPIO.LOW)

print("Hello!")
# Loop forever, check buttons, etc.
while True:
    for switch in [0, 1, 2, 3, 4]:
        if GPIO.input(inputs[switch]) == GPIO.HIGH:
            GPIO.output(outputs[switch], GPIO.LOW)
        else:
            GPIO.output(outputs[switch], GPIO.HIGH)

    # Check how many switches are pressed.
    pressed=0
    for switch in [1, 2, 3, 4, 5]:
        if GPIO.input(inputs[switch-1]) == GPIO.HIGH:
            pressed=pressed+1

    # Set RBG to red if anything other than 1 switch is flipped.
    # Unless it's 5, then turn everything on. So, white.
    if (pressed == 1):
        GPIO.output(gled, GPIO.LOW)
        GPIO.output(rled, GPIO.HIGH)
        GPIO.output(bled, GPIO.HIGH)
    elif (pressed == 5):
        GPIO.output(gled, GPIO.LOW)
        GPIO.output(rled, GPIO.LOW)
        GPIO.output(bled, GPIO.LOW)
    else:
        GPIO.output(rled, GPIO.LOW)
        GPIO.output(gled, GPIO.HIGH)
        GPIO.output(bled, GPIO.HIGH)


    if GPIO.input(bigredbutton) == GPIO.HIGH:
        pressed=0;
        print ("BRB pressed.")
        while GPIO.input(bigredbutton) == GPIO.HIGH:
            donothing=1

        print ("BRB Relesaed")
        for switch in [1, 2, 3, 4, 5]:
            if GPIO.input(inputs[switch-1]) == GPIO.HIGH:
                pressed=pressed+1
                print ("Switch " ,switch, " is on.")

        print (pressed, " switches are on.")

        if (pressed == 5):
            print ("(Not) Shutting down...")
            #call("sudo init 0", shell=True)

