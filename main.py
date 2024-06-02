# The Pantry Aid
# Inventory management system for your Pantry

# Import required libraries
from PantryAid_UI import *
from PiicoDev_CAP1203 import PiicoDev_CAP1203
from PiicoDev_Unified import sleep_ms
from machine import Pin
from Makerverse_hx710c import Makerverse_hx710c
import network
from umqtt.simple import MQTTClient

# WiFi network name (ssid) and password
wifi_ssid = #PUT YOUR SSID HERE
wifi_password = #PUT YOUR PASSWORD HERE

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep_ms(1000)
print("Connected to WiFi")

# Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "io.adafruit.com"
mqtt_username = #PUT YOUR USERNAME HERE
mqtt_password = #PUT YOUR PASSWORD HERE
mqtt_publish_topic = #PUT YOUR TOPIC HERE

# Random ID for this MQTT Client
mqtt_client_id = "pantryaidSIT210adafruitblrogersscale1"

# Initialize MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

# Initialise Touch Sensor and Scale
touchSensor = PiicoDev_CAP1203(touchmode='single')
LC = Makerverse_hx710c(dataPin = Pin(17), clkPin = Pin(16), calibration=1.4397e-3)

# Set number of samples to take when measuring weight
SAMPLES = 10

# Set global variables
menuSelection = 0
maximumValue = 50
currentValue = 0
alertThreshold = 50
standbyCounter = 0

# Run startup function
UI_Startup()
#UI_Initialize()

# Runs to handled unexpected errors (eg. divide by zero)
# Allows device to be reset
def errorOccured():
    confirmationCounter = 0
    UI_Error(False, confirmationCounter)
    sleep_ms(500)
    # Change Touch Sensor to read multiple inputs
    touchSensor = PiicoDev_CAP1203()
    touchStatus = touchSensor.read()
    # Wait until both left and right button are held to reset device
    while True:
        sleep_ms(100)
        touchStatus = touchSensor.read()
        if(not touchStatus[1] or not touchStatus[3]):
            UI_Error(False, confirmationCounter)
            confirmationCounter = 0
        elif(touchStatus[1] and touchStatus[3] and not confirmationCounter >= 50):
            UI_Error(True, confirmationCounter)
            confirmationCounter = confirmationCounter + 1
        elif(touchStatus[1] and touchStatus[3] and confirmationCounter >= 50):
            machine.reset()

# Checks if standby conditions are met and will turn off screen after 30 seconds
def standbyCheck(counter, currentValue, maximumValue, leftTouch, middleTouch, rightTouch):
    if(leftTouch or middleTouch or rightTouch):
        return 0
    else:
        if(counter < 300):
            return counter + 1
        elif(counter >= 300):
            timeCounter = 0
            UI_StandbyToggle(True)
            touchStatus = touchSensor.read()
            # Keep screen turned off until a button is pressed
            while (not touchStatus[1] and not touchStatus[2] and not touchStatus[3]):
                timeCounter = timeCounter + 1
                if(timeCounter >= 50):
                    try:
                        timeCounter = 0
                        currentValue = LC.read_hx710_calibrated()
                        percentageValue = int((currentValue/maximumValue)*100)
                        print(f'Publish {percentageValue:.2f}')

                        mqtt_client.publish(mqtt_publish_topic, str(percentageValue))
                    except Exception as e:
                        print(f'Failed to publish message: {e}')
                sleep_ms(100)
                touchStatus = touchSensor.read()
            UI_StandbyToggle(False)
            sleep_ms(500)
            return 0

# Checks current weight of item against preset maximum weight to determine percentage
def checkPercentage(maximumValue):
    # Start 30 second exit timer
    exitTimer = 0
    # If maximum weight is set at '0' then throw the error
    if(maximumValue == 0):
        errorOccured()
    # Read value from Scales
    currentValue = LC.read_hx710_calibrated()
    UI_CheckPercentage(int((currentValue/maximumValue)*100), False, False, False)
    sleep_ms(500)
    touchStatus = touchSensor.read()
    # Remain at this menu until option is selected
    while(not touchStatus[1] and not touchStatus[2] and not touchStatus[3]):
        currentValue = LC.read_hx710_calibrated()
        UI_CheckPercentage(int((currentValue/maximumValue)*100), False, False, False)
        sleep_ms(100)   
        touchStatus = touchSensor.read()
        exitTimer = exitTimer + 1
        if(exitTimer >= 300):
            break
    UI_CheckPercentage(int((currentValue/maximumValue)*100), touchStatus[1], touchStatus[2], touchStatus[3])
    sleep_ms(500)

# Sets minimum or maximum values based on menu selection
def setValues(menuSelection, maximumValue):
    # Start 30 second exit timer
    exitTimer = 0
    # Determine which menu was selected
    if(menuSelection == 1):
        minimum = True
        maximum = False
    elif(menuSelection == 2):
        minimum = False
        maximum = True
    confirmationCounter = 0
    UI_SetValues(minimum, maximum, False, confirmationCounter, False, False, False, False)
    sleep_ms(500)
    touchStatus = touchSensor.read()
    # Remain at this menu until option is selected
    while(not touchStatus[1] and not touchStatus[3]):
        # If confirmation is not being held
        if(not touchStatus[2]):
            UI_SetValues(minimum, maximum, False, confirmationCounter, False, touchStatus[1], touchStatus[2], touchStatus[3])
            confirmationCounter = 0
        # If confirmation is being held
        elif(touchStatus[2]):
            if(not confirmationCounter >= 30):
                UI_SetValues(minimum, maximum, True, confirmationCounter, False, touchStatus[1], touchStatus[2], touchStatus[3])
                confirmationCounter = confirmationCounter + 1
                exitTimer = 0
            elif(confirmationCounter >= 30):
                UI_SetValues(minimum, maximum, True, confirmationCounter, True, False, False, False)
                # If setting minimum value
                if(minimum):
                    LC.setZero()
                # If setting maximum value
                if(maximum):
                    for k in range(32):
                        tmp = LC.read_hx710_calibrated()
                    maximumValue = 0
                    for k in range(SAMPLES):
                        maximumValue += LC.read_hx710_calibrated()
                    maximumValue = maximumValue / SAMPLES
                confirmationCounter = 0
                UI_SetValues(minimum, maximum, True, confirmationCounter, True, False, False, False)
                sleep_ms(2000)
                break
        sleep_ms(100)   
        touchStatus = touchSensor.read()
        exitTimer = exitTimer + 1
        if(exitTimer >= 300):
            break
    return int(maximumValue)

# Sets Alert Threshold for when notification is sent to inventory list
def setThreshold(alertThreshold):
    # Start 30 second exit timer
    exitTimer = 0
    UI_AlertThreshold(alertThreshold, False, False, False, False)
    sleep_ms(500)
    touchStatus = touchSensor.read()
    # Remain at this menu until option is selected
    while True:
        if(touchStatus[1] and alertThreshold > 0):
            alertThreshold = alertThreshold - 10
            exitTimer = 0
        elif(touchStatus[3] and alertThreshold < 100):
            alertThreshold = alertThreshold + 10
            exitTimer = 0
        elif(touchStatus[2]):
            UI_AlertThreshold(alertThreshold, False, touchStatus[1], touchStatus[2], touchStatus[3])
            sleep_ms(500)
            UI_AlertThreshold(alertThreshold, True, False, False, False)
            sleep_ms(2000)
            menuSelection = 0
            break
        UI_AlertThreshold(alertThreshold, False, touchStatus[1], touchStatus[2], touchStatus[3])
        sleep_ms(100)
        touchStatus = touchSensor.read()
        exitTimer = exitTimer + 1
        if(exitTimer >= 300):
            break
    return alertThreshold

# Calibrate sensor if issue is found
def calibrateSensor():
    # Start 30 second exit timer
    exitTimer = 0
    confirmationCounter = 0
    UI_CalibrateSensorCheck(False, confirmationCounter, False, False, False)
    sleep_ms(500)
    touchStatus = touchSensor.read()
    while(not touchStatus[1] and not touchStatus[3]):
        if(not touchStatus[2]):
            UI_CalibrateSensorCheck(False, confirmationCounter, touchStatus[1], touchStatus[2], touchStatus[3])
            confirmationCounter = 0
        elif(touchStatus[2]):
            if(not confirmationCounter >= 30):
                UI_CalibrateSensorCheck(True, confirmationCounter, touchStatus[1], touchStatus[2], touchStatus[3])
                confirmationCounter = confirmationCounter + 1
                exitTimer = 0
            elif(confirmationCounter >= 30):
                UI_CalibrateSensorCheck(True, confirmationCounter, touchStatus[1], touchStatus[2], touchStatus[3])
                sleep_ms(2000)
                LC.calibrate()
                sleep_ms(2000)
                break
        sleep_ms(100)
        touchStatus = touchSensor.read()
        exitTimer = exitTimer + 1
        if(exitTimer >= 300):
            break

timeCounter = 0

# Display Main screen
while True:
    if(wlan.isconnected() == False):
        wlan.connect(wifi_ssid, wifi_password)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            UI_WiFiConnected(False)
            sleep_ms(1000)
        print("Connected to WiFi")
        UI_WiFiConnected(True)
        mqtt_client.connect()
        sleep_ms(2000)
    
    timeCounter = timeCounter + 1
    if(timeCounter >= 50):
        try:
            timeCounter = 0
            # Generate some dummy data that changes every loop
            currentValue = LC.read_hx710_calibrated()
            percentageValue = int((currentValue/maximumValue)*100)
            print(f'Publish {percentageValue:.2f}')
            # Publish the data to the topic!
            mqtt_client.publish(mqtt_publish_topic, str(percentageValue))
        except Exception as e:
            print(f'Failed to publish message: {e}')
            
    touchStatus = touchSensor.read()
       
    UI_Menu(menuSelection, touchStatus[1], touchStatus[2], touchStatus[3])
    data = LC.read_hx710_calibrated()
    
    # User presses the left button
    if(touchStatus[1]):
        UI_Menu(menuSelection, touchStatus[1], touchStatus[2], touchStatus[3])
        menuSelection = (menuSelection - 1) % 5
        sleep_ms(500)
        
    # User presses the right button
    elif(touchStatus[3]): 
        UI_Menu(menuSelection, touchStatus[1], touchStatus[2], touchStatus[3])
        menuSelection = (menuSelection + 1) % 5
        sleep_ms(500)
        
    # User presses the middle button
    elif(touchStatus[2]):
        UI_Menu(menuSelection, touchStatus[1], touchStatus[2], touchStatus[3])
        sleep_ms(500)
        # If Check Percentage was selected
        if(menuSelection == 0):
            checkPercentage(maximumValue)       
        # If Set Minimum or Set Maximum was selected
        elif(menuSelection == 1 or menuSelection == 2):
            maximumValue = setValues(menuSelection, maximumValue)
        # If Set Alert Threshold was selected
        elif(menuSelection == 3):
            alertThreshold = setThreshold(alertThreshold)
        # If Calibrate Sensor was selected
        elif(menuSelection == 4):
            calibrateSensor()
        menuSelection = 0
        sleep_ms(400)
    
    sleep_ms(100)
    standbyCounter = standbyCheck(standbyCounter, currentValue, maximumValue, touchStatus[1], touchStatus[2], touchStatus[3])
