from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
import time
from paho.mqtt import client as mqtt_client

MQTTdata = None

broker = "io.adafruit.com"
port = 1883
topic = #PUT YOUR TOPIC HERE
username = #PUT YOUR USERNAME HERE
password = #PUT YOUR PASSWORD HERE

# Random ID for this MQTT Client
client_id = "pantryaidSIT210adafruitblrogerslist"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global MQTTdata
        MQTTdata = msg.payload.decode()
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    client.subscribe(topic)
    client.on_message = on_message

class MyWindow(QMainWindow):   

    itemOneToggle = False
    itemTwoToggle = False
    itemThreeToggle = False
    
    itemOneData = None

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("PANTRY AID")
        self.initUI()
    
    def initUI(self):
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText("Pantry Management System")
        self.titleLabel.move(10, 10)
        
        #self.lastupdateLabel = QtWidgets.QLabel(self)
        #self.lastupdateLabel.setText("Last Updated: ")
        #self.lastupdateLabel.move(10, 25)
        
        self.itemHeading = QtWidgets.QLabel(self)
        self.itemHeading.setText("SCALES: ")
        self.itemHeading.move(10, 40)
        
        self.valueHeading = QtWidgets.QLabel(self)
        self.valueHeading.setText("REMAINING: ")
        self.valueHeading.move(140, 40)
        
        self.itemOneLabel = QtWidgets.QLabel(self)
        self.itemOneLabel.setText("SCALE ONE")
        self.itemOneLabel.move(10, 70)
        self.itemOneValue = QtWidgets.QLabel(self)
        self.itemOneValue.setText(str(self.itemOneData) + "%")
        self.itemOneValue.move(140, 70)
        
        self.itemTwoLabel = QtWidgets.QLabel(self)
        self.itemTwoLabel.setText("SCALE TWO")
        self.itemTwoLabel.move(10, 100)
        self.itemTwoValue = QtWidgets.QLabel(self)
        self.itemTwoValue.setText("XXX%")
        self.itemTwoValue.move(140, 100)
        
        self.itemThreeLabel = QtWidgets.QLabel(self)
        self.itemThreeLabel.setText("SCALE THREE")
        self.itemThreeLabel.move(10, 130)
        self.itemThreeValue = QtWidgets.QLabel(self)
        self.itemThreeValue.setText("XXX%")
        self.itemThreeValue.move(140, 130)

        self.itemOneCheck = QtWidgets.QPushButton(self)
        self.itemOneCheck.setText("Reviewed?")
        self.itemOneCheck.clicked.connect(self.clickedItemOne)
        self.itemOneCheck.move(190, 64)
        
        self.itemTwoCheck = QtWidgets.QPushButton(self)
        self.itemTwoCheck.setText("Reviewed?")
        self.itemTwoCheck.clicked.connect(self.clickedItemTwo)
        self.itemTwoCheck.move(190, 94)
        
        self.itemThreeCheck = QtWidgets.QPushButton(self)
        self.itemThreeCheck.setText("Reviewed?")
        self.itemThreeCheck.clicked.connect(self.clickedItemThree)
        self.itemThreeCheck.move(190, 124)
        
        self.buttonUpdate = QtWidgets.QPushButton(self)
        self.buttonUpdate.setText("Click to update")
        self.buttonUpdate.clicked.connect(self.clickedUpdate)
        self.buttonUpdate.move(30, 260)
        
        self.buttonExit = QtWidgets.QPushButton(self)
        self.buttonExit.setText("Click to exit")
        self.buttonExit.clicked.connect(self.close)
        self.buttonExit.move(170, 260)
        
        self.update()
        
    def clickedItemOne(self): 
        if(self.itemOneToggle):
            f = self.itemOneLabel.font()
            f.setStrikeOut(False)
            self.itemOneLabel.setFont(f)
            self.itemOneToggle = False
        elif(not self.itemOneToggle):
            f = self.itemOneLabel.font()
            f.setStrikeOut(True)
            self.itemOneLabel.setFont(f)
            self.itemOneToggle = True
            
    def clickedItemTwo(self): 
        if(self.itemTwoToggle):
            f = self.itemTwoLabel.font()
            f.setStrikeOut(False)
            self.itemTwoLabel.setFont(f)
            self.itemTwoToggle = False
        elif(not self.itemTwoToggle):
            f = self.itemTwoLabel.font()
            f.setStrikeOut(True)
            self.itemTwoLabel.setFont(f)
            self.itemTwoToggle = True

    def clickedItemThree(self): 
        if(self.itemThreeToggle):
            f = self.itemThreeLabel.font()
            f.setStrikeOut(False)
            self.itemThreeLabel.setFont(f)
            self.itemThreeToggle = False
        elif(not self.itemThreeToggle):
            f = self.itemThreeLabel.font()
            f.setStrikeOut(True)
            self.itemThreeLabel.setFont(f)
            self.itemThreeToggle = True
            
    def clickedUpdate(self): 
        counter = 0
        client = connect_mqtt()
        client.loop_start()
        while (counter < 10):
            counter = counter + 1 
            time.sleep(1)
            subscribe(client)
            self.itemOneData = MQTTdata
        client.loop_stop()
        print("Disconected from MQTT Broker")
        self.itemOneValue.setText(str(self.itemOneData) + "%")
        self.update()
        
    def update(self):
        self.titleLabel.adjustSize()
        self.itemHeading.adjustSize()
        self.valueHeading.adjustSize()
        #self.lastupdateLabel.adjustSize()
        self.itemOneLabel.adjustSize()
        self.itemOneValue.adjustSize()
        self.itemTwoLabel.adjustSize()
        self.itemTwoValue.adjustSize()
        self.itemThreeLabel.adjustSize()
        self.itemThreeValue.adjustSize()
            
def window():
    app = QApplication (sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())

window()
