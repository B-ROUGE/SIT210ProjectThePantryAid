# User Interface and display for Pantry Aid

# Import required libaries
import math
from PiicoDev_SSD1306 import *
from PiicoDev_Unified import sleep_ms

display = create_PiicoDev_SSD1306()

PROJECTHEADING = "PANTRY AID"

def UI_Heading():
    display.text(PROJECTHEADING, int(64-((len(PROJECTHEADING)*8)/2)), 0, 1)
    display.line(int(64-((len(PROJECTHEADING)*8)/2))-5, 0, int(64-((len(PROJECTHEADING)*8)/2))-5, 11, 1)
    display.line(int(64-((len(PROJECTHEADING)*8)/2))-3, 0, int(64-((len(PROJECTHEADING)*8)/2))-3, 9, 1)
    display.line(int(64+((len(PROJECTHEADING)*8)/2))+2, 0, int(64+((len(PROJECTHEADING)*8)/2))+2, 9, 1)
    display.line(int(64+((len(PROJECTHEADING)*8)/2))+4, 0, int(64+((len(PROJECTHEADING)*8)/2))+4, 11, 1)
    display.line(int(64-((len(PROJECTHEADING)*8)/2))-5, 11, int(64+((len(PROJECTHEADING)*8)/2))+4, 11, 1)
    display.line(int(64-((len(PROJECTHEADING)*8)/2))-3, 9, int(64+((len(PROJECTHEADING)*8)/2))+2, 9, 1)

def UI_Startup():
    for counter in range(0,101):
        display.fill(0)
        UI_Heading()
        textLine1 = "Device starting"
        display.text(textLine1, int(64-((len(textLine1)*8)/2)), 27, 1)
        textLine2 = str(counter)
        display.text(textLine2, int(64-((len(textLine2)*8)/2)), 37, 1)
        display.show()
    sleep_ms(500)
    
def UI_Error(confirmed, counter):
    display.fill(0)
    UI_Heading()
    if(not confirmed):
        UI_4TextLine("DEVICE ERROR", "RESTART REQUIRED", "PRESS AND HOLD", "BOTH ARROWS")
    elif(confirmed):
        UI_2TextLine("HOLD TO RESET", str(round(5-(counter/10), 1)))
    display.show()
    
def UI_LeftButton(x, y, status):
    display.line(x, y+3, x+7, y, 1)
    display.line(x, y+3, x+7, y+6, 1)
    display.line(x+7, y, x+7, y+6, 1)
    if(status):
        display.line(x+1, y+3, x+6, y+1, 1)
        display.line(x+1, y+3, x+6, y+2, 1)
        display.line(x+1, y+3, x+6, y+3, 1)
        display.line(x+1, y+3, x+6, y+4, 1)
        display.line(x+1, y+3, x+6, y+5, 1)

def UI_RightButton(x, y, status):
    display.line(x+7, y+3, x, y, 1)
    display.line(x+7, y+3, x, y+6, 1)
    display.line(x, y, x, y+6, 1)
    if(status):
        display.line(x+6, 60, x+1, y+1, 1)
        display.line(x+6, 60, x+1, y+2, 1)
        display.line(x+6, 60, x+1, y+3, 1)
        display.line(x+6, 60, x+1, y+4, 1)
        display.line(x+6, 60, x+1, y+5, 1)

def UI_MiddleButton(x, y, status):
    display.line(x, y+2, x+2, y, 1)
    display.line(x+2, y, x+4, y, 1)
    display.line(x+4, y, x+6, y+2, 1)
    display.line(x+6, y+2, x+6, y+4, 1)
    display.line(x+6, y+4, x+4, y+6, 1)
    display.line(x+4, y+6, x+2, y+6, 1)
    display.line(x+2, y+6, x, y+4, 1)
    display.line(x, y+4, x, y+2, 1)
    if(status):
        display.line(x+2, y+1, x+4, y+1, 1)
        display.line(x+1, y+2, x+5, y+2, 1)
        display.line(x+1, y+3, x+5, y+3, 1)
        display.line(x+1, y+4, x+5, y+4, 1)
        display.line(x+2, y+5, x+4, y+5, 1)

def UI_1TextLine(line):
    display.text(line, int(64-((len(line)*8)/2)), 22, 1)

def UI_2TextLine(line1, line2):
    display.text(line1, int(64-((len(line1)*8)/2)), 17, 1)
    display.text(line2, int(64-((len(line2)*8)/2)), 27, 1)
    
def UI_4TextLine(line1, line2, line3, line4):
    display.text(line1, int(64-((len(line1)*8)/2)), 22, 1)
    display.text(line2, int(64-((len(line2)*8)/2)), 32, 1)
    display.text(line3, int(64-((len(line3)*8)/2)), 42, 1)
    display.text(line4, int(64-((len(line4)*8)/2)), 52, 1)
    
def UI_5TextLine(line1, line2, line3, line4, line5):
    display.text(line1, int(64-((len(line1)*8)/2)), 17, 1)
    display.text(line2, int(64-((len(line2)*8)/2)), 27, 1)
    display.text(line3, int(64-((len(line3)*8)/2)), 37, 1)
    display.text(line4, int(64-((len(line4)*8)/2)), 47, 1)
    display.text(line5, int(64-((len(line5)*8)/2)), 57, 1)
    
# Display menu selection at y
def UI_MenuButtons(leftTitle, leftStatus, middleTitle, middleStatus, rightTitle, rightStatus):
    display.line(0, 43, 127, 43, 1)
    display.line(0, 44, 127, 44, 1)
    display.text(leftTitle, int(17-((len(leftTitle)*8)/2)), 47, 1)
    UI_LeftButton(13, 57,leftStatus)
    display.line(35, 45, 35, 63, 1)
    display.line(36, 45, 36, 63, 1)
    display.text(middleTitle, int(64-((len(middleTitle)*8)/2)), 47, 1)
    UI_MiddleButton(60, 57, middleStatus)
    display.line(90, 45, 90, 63, 1)
    display.line(91, 45, 91, 63, 1)
    display.text(rightTitle, int(110-((len(rightTitle)*8)/2)), 47, 1)
    UI_RightButton(106, 57, rightStatus)

def UI_Menu(selection, leftTouch, middleTouch, rightTouch):
    display.fill(0)
    UI_Heading()
    UI_MenuButtons("BACK", leftTouch, "SELECT", middleTouch, "NEXT", rightTouch)
    
    if(selection == 0):
        UI_2TextLine("Check Percentage", "Remaining")
    elif(selection == 1):
        UI_2TextLine("Set Minimum", "(empty)")
    elif(selection == 2):
        UI_2TextLine("Set Maximum", "(full)")
    elif(selection == 3):
        UI_2TextLine("Set Alert", "Threshold")
    elif(selection == 4):
        UI_2TextLine("Calibrate Sensor", "<CAUTION>")
    
    display.show()
    
def UI_CheckPercentage(percentage, leftTouch, middleTouch, rightTouch):
    display.fill(0)
    UI_Heading()
    UI_MenuButtons("EXIT", leftTouch, "EXIT", middleTouch, "EXIT", rightTouch)
    
    UI_2TextLine(str(percentage) + "%", "Remaining")
    
    display.show()

def UI_SetValues(minimum, maximum, confirmed, counter, valueSet, leftTouch, middleTouch, rightTouch):
    display.fill(0)
    UI_Heading()
    UI_MenuButtons("EXIT", leftTouch, "SET", middleTouch, "EXIT", rightTouch)
    
    if(minimum and not confirmed):
        UI_2TextLine("Hold SET to", "set minimum")
    elif(minimum and confirmed and not valueSet):
        UI_2TextLine("Hold to confirm", str(round(3-(counter/10), 1)))
    elif(minimum and confirmed and valueSet and counter >= 30):
        UI_1TextLine("SETTING MINIMUM")
    elif(minimum and confirmed and valueSet):
        UI_1TextLine("MINIMUM SET")
        
    elif(maximum and not confirmed):
        UI_2TextLine("Hold SET to", "set maximum")
    elif(maximum and confirmed and not valueSet):
        UI_2TextLine("Hold to confirm", str(round(3-(counter/10), 1)))
    elif(maximum and confirmed and valueSet and counter >= 30):
        UI_1TextLine("SETTING MAXIMUM")
    elif(maximum and confirmed and valueSet):
        UI_1TextLine("MAXIMUM SET")
    
    display.show()

def UI_AlertThreshold(thresholdValue, valueSet, leftTouch, middleTouch, rightTouch):
    display.fill(0)
    UI_Heading()
    UI_MenuButtons("DOWN", leftTouch, "SET", middleTouch, "UP", rightTouch)
    
    if(not valueSet and thresholdValue == 0):
        UI_2TextLine("Alert threshold:", "OFF")
    elif(not valueSet and thresholdValue == 100):
        UI_2TextLine("Alert threshold:", "FULL")
    elif(not valueSet):
        UI_2TextLine("Alert threshold:", str(thresholdValue) + "%")
    elif(valueSet and thresholdValue == 0):
        UI_1TextLine("ALERT OFF")
    elif(valueSet):
        UI_1TextLine("THRESHOLD SET")
        
    display.show()

def UI_CalibrateSensorCheck(confirmed, counter, leftTouch, middleTouch, rightTouch):
    display.fill(0)
    UI_Heading()
    UI_MenuButtons("EXIT", leftTouch, "RESET", middleTouch, "EXIT", rightTouch)
    
    if(not confirmed):
        UI_2TextLine("CALIBRATE WITH", "CAUTION")
    elif(confirmed and counter < 30):
        UI_2TextLine("HOLD TO RESET", str(round(3-(counter/10), 1)))
    elif(confirmed and counter >= 30):
        UI_2TextLine("STARTING", "CALIBRATION")
                     
    display.show()
    
def UI_SensorCalibration(calibrationWeight, inProgress, completed):
    display.fill(0)
    UI_Heading()
    
    if(not calibrationWeight and not inProgress and not completed):
        UI_5TextLine("REMOVE ALL", "WEIGHT FROM", "SENSOR, THEN", "PRESS THE MIDDLE", "BUTTON ONCE")
    elif(not calibrationWeight and inProgress and not completed):
        UI_2TextLine("CALIBRATION", "IN PROGRESS")
    elif(calibrationWeight and not inProgress and not completed):
        UI_5TextLine("PLACE 50G", "WEIGHT ON", "SENSOR, THEN", "PRESS THE MIDDLE", "BUTTON ONCE")
    elif(calibrationWeight and inProgress and not completed):
        UI_2TextLine("CALIBRATION", "IN PROGRESS")
    elif(not calibrationWeight and not inProgress and completed):
        UI_2TextLine("CALIBRATION", "COMPLETED")
        
    display.show()
    
def UI_StandbyToggle(power):
    if(power):
        display.poweroff()
    elif(not power):
        display.poweron()
        
def UI_WiFiConnected(connected):
    display.fill(0)
    UI_Heading()
    if(not connected):
        UI_2TextLine("CONNECTING", "TO WIFI")
    if(connected):
        UI_1TextLine("WIFI CONNECTED")
        
    display.show()
    
