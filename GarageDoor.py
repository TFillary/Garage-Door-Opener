#!/usr/bin/env python3
#############################################################################
# Filename    : GarageDoor.py
# Description :	Application to operate the Garage Door opener - simplified version to mimic remote switch
#                 1. Using web/browser interface - web browser i/f creates a text file to causes
#                    this program to activate the relay for the door
#                 2. Using local switch
# Author      : TDF
# modification: 11-08-2021
#############################################################################
import time
from datetime import datetime
import sys
from gpiozero import Button, OutputDevice
from pathlib import Path

# Import Adafruit libraries for temperature sensor
import board
import busio
import adafruit_mcp9808

# TODO Set to true to enable debug without hardware temperature sensor connected.  
# Switch and Relay setup works without the actual hardware, just won't do anything
NoHW = False

#
# Door variables / constans definitions
#
DoorButtonPin = 21  # Pin used for manual control of the door - physical pin 40, conveniently next to pin 39 which is ground
ButtonCommand = False   # If set indicates that a button commanded the garage door be activated rather than web i/f

#
# Temperature variable/constant definitions
#
unitsC = True  # Indicates whether C or F units
temperature = 0.00
now = 0.00
LowTemp = 99.00  # Set to crazy high temperature so will get set the first time through
LowTempTime = '0.0'
HiTemp = -99.00  # Set to crazy low temperature so will get set the first time through
HiTempTime = '0.0'
#
# Relay variable/constant definitions
#
Relay1Pin = 22  #Define the BCM pin for Relay 1 on the SB Zero Relay board (SB states Board Pin 15)

# Handle button presses
def btn1Handler():
    global ButtonCommand

    # Force door activation
    ButtonCommand = True
    

def readTemperature():
    global now, temperature, LowTemp, LowTempTime, HiTemp, HiTempTime
    
    # Read temperature from sensor and save in global variable
    temperature = mcp.temperature

    now = datetime.now()
    # print("now = ", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    print("Date and Time =", dt_string)
    print('Temperature: {} degrees C'.format(temperature))

    # Update lowest and highest temperature
    if temperature < LowTemp:
        LowTemp = temperature
        LowTempTime = dt_string
    
    if HiTemp < temperature:
        HiTemp = temperature
        HiTempTime = dt_string

    # Replace file with new temperature data
    file = "/var/www/html/garagetemp.txt"
    with open(file, 'w') as filetowrite:
        textlist = ['Current Temperature: ', str(temperature), ' C', '\n', 'Date and Time: ', dt_string, '\n\n']
        filetowrite.writelines(textlist)
        
        textlist = ['Low Temperature: ', str(LowTemp), ' C', '\n', 'Low Temperature Time: ', LowTempTime, '\n\n']
        filetowrite.writelines(textlist)

        textlist = ['High Temperature: ', str(HiTemp), ' C', '\n', 'High Temperature Time: ', HiTempTime]
        filetowrite.writelines(textlist)
        filetowrite.close()

def PulseRelay():
    # Setup path to disable command file
    disablefile = Path("/var/www/html/disabledoor.txt")
    if not disablefile.is_file() or ButtonCommand:
        # Pulse the garage door mechanism via a relay
        print("Activated Door")
        relay.on() # switch on
        time.sleep(0.5)  # Default to 0.5 second pulse
        relay.off() # switch off
    else:
        print("Remote Door Control Disabled")

def loop():
    global temperature, now, ButtonCommand, LowTemp, LowTempTime, HiTemp, HiTempTime

    # Setup loop delay variables for temperature measurements
    loop_delay = 60 #  For minute reslution, loop delay should be 60s for a second resolution loop delay should be 1s
    holdoff = False
    holdoffcount = 0

    # Setup path to command file
    activatefile = Path("/var/www/html/activatedoor.txt")

    while(True):
        # Check if a web interface or a button command to action
        if activatefile.is_file() or ButtonCommand:

            if not ButtonCommand:
                # get passed ip address
                ip_address = activatefile.read_text()

                match = False
                # Open file to check whether sent a registered IP address
                ip_log_file = open("/var/www/html/reg_ip_log.txt","r")
                for aline in ip_log_file:
                    print(aline.strip())
                    if aline.strip() == ip_address.strip():
                        print("match")
                        match = True
                        PulseRelay()  # Activate door
                        
                        file_to_remove = Path("/var/www/html/notauthorised.txt")
                        # Delete notauthorised file if match found
                        if file_to_remove.is_file():
                            file_to_remove.unlink() # Delete file command.

                        break  # Force exit from loop on first find
                
                if not match:
                    print("Not Authorised")
                    # Create notauthorised file
                    file = "/var/www/html/notauthorised.txt"
                    with open(file, 'w') as filetowrite:
                        filetowrite.writelines("Not Authorised")
                        filetowrite.close()

                                
            if ButtonCommand:
                PulseRelay()  # Activate door
                ButtonCommand = False # Reset flag for next button push
            else:  # Initiated via the web interfac
                # Remove file ready for next command
                # Note that I had to make 'pi' the owner of /var/www/html to allow deletions of the control file
                file_to_remove = Path("/var/www/html/activatedoor.txt")
                file_to_remove.unlink() # Delete file command.


        if holdoff: # Force delay in temperature measurement check to ensure don't make multiple temperature reads within the 1 minute resolution
            holdoffcount +=1
            time.sleep(1)  # Delay one second
            if holdoffcount > loop_delay:
                holdoffcount = 0
                holdoff = False
        
        m = datetime.now().minute
        h = datetime.now().hour
        if ((m % 15) == 0) and not holdoff:  # Temperature measurment frequency   
            # Read Temperature and Humidity from sensor only when necessary
            # Read temperature sensor if sensor present
            if not NoHW:
                readTemperature()
            
            holdoff = True  # make sure don't have loads of temperature measurements within a minute...
            
            # If midnight then reset the hi and low temperatures to the current temperature
            if h == 0:  # Check if midnight
                LowTemp = temperature
                LowTempTime = now.strftime("%d/%m/%Y %H:%M")
                HiTemp = temperature
                HiTempTime = now.strftime("%d/%m/%Y %H:%M")

        # Delay to allow RPi to process server requests
        time.sleep(0.2)  
            

# Main setup and initialisation code

# Button numbering is using BCM numbering
DoorButton = Button(DoorButtonPin, bounce_time=0.2)   # Assign button to a variable
# tell the button what to do when pressed
DoorButton.when_pressed = btn1Handler

# Create i2c and temperature sensor object2 if temperature sensor is present
if not NoHW:
    i2c = busio.I2C(board.SCL, board.SDA)  
    mcp = adafruit_mcp9808.MCP9808(i2c)   # Note using default address (ie address pins not connected)

# Set up Relay driver output
# Triggered by the output pin going high: active_high=True
# Initially off: initial_value=False
relay = OutputDevice(Relay1Pin, active_high=True, initial_value=False)

if __name__ == '__main__':
    print ('Program is starting ... ')
    
    # Log initial temperature before enters main loop with associated timings
    # Read temperature if sensor present
    if not NoHW:
        readTemperature()
    
    try:
        loop()
    #    while(True): #just look initially to test out the screens and buttons only.....
    #        pass

    except KeyboardInterrupt:
        # Tidy up if necessary (gpiozero does this itself)
        
        exit()


