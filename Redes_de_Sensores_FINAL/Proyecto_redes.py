# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 13:37:30 2023

@author: SANTIAGO MEDINA
"""

import os
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, Qt, QtWidgets, uic
import pandas as pd
import datetime
import random
import math
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import IMAGES_RC

Cont = 0
class Principal(QtWidgets.QMainWindow):
    def __init__(self):
        super(Principal, self).__init__()
        uic.loadUi('Ejercicio_1.ui',self)
        
        self.S_Proximidad.clicked.connect(self.sensor1)
        self.S_Velocidad.clicked.connect(self.sensor2)
        self.S_Peso.clicked.connect(self.sensor3)
        self.S_Temperatura.clicked.connect(self.sensor4)
        self.Comparacion.clicked.connect(self.comparacion)
        
    def sensor1(self):

        global Cont
        Cont = +1
        from digi.xbee.devices import XBeeDevice
        from digi.xbee.io import IOLine, IOMode
        # Serial port on Raspberry Pi
        SERIAL_PORT = "/dev/ttyUSB0"
        # BAUD rate for the XBee module connected to the Raspberry Pi
        BAUD_RATE = 9600
        # The name of the remote node (NI)
        REMOTE_NODE_ID = "SENSOR6"
        # Analog pin we want to monitor/request data
        ANALOG_LINE = IOLine.DIO3_AD3
        # Sampling rate
        SAMPLING_RATE = 15
        # Get an instance of the XBee device class
        device = XBeeDevice(SERIAL_PORT, BAUD_RATE)
        print(device)
        # Method to connect to the network and get the remote node by id
        def get_remote_device():
           """Get the remote node from the network 
           Returns:
           """
           # Request the network class and search the network for the remote node
           xbee_network = device.get_network()
           remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
           if remote_device is None:
              print("ERROR: Remove node id {0} not found.".format(REMOTE_NODE_ID))
              exit(1)
           remote_device.set_dest_address(device.get_64bit_addr())
           remote_device.set_io_configuration(ANALOG_LINE, IOMode.ADC)
           remote_device.set_io_sampling_rate(SAMPLING_RATE)

        def io_sample_callback(sample, remote, time):
           print("Reading from {0} at {1}:".format(REMOTE_NODE_ID, remote.get_64bit_addr()))
           # Get the temperature in Celsius
           VoltageOutput= ((sample.get_analog_value(ANALOG_LINE) * 1200.0 / 1024.0) - 500.0) / 10.0
           # Calculate temperature in Fahrenhei
           #print("\tTemperature is {0}C. {1}F".format(temp_c, temp_f))
           # Calculate supply voltage
           VoltageInput = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
           print("\tSupply Voltage Sensor 6 = {0}v".format(VoltageOutput,VoltageInput))
           
           import os
           import sys
           Save = open("./Data1.txt",'a')
           Save.write(f"{VoltageOutput} {VoltageInput}"+"\n")
           print (Save)
           '''save.write("Now is the time Group 6\n")
           save.write("Yes, It's the time Group 6\n")'''
           Save.close()

        try:
           print("Welcome to example of reading a remote sensor 6!")
           device.open() # Open the device class
           # Setup the remote device
           get_remote_device()
           # Register a listener to handle the samples received by the local device.
           device.add_io_sample_received_callback(io_sample_callback)
           
           while True:
               if(Cont==7):
                   Cont=0
                   break
                
               Save=open("Data1.txt","r")
               Row=Save.read().splitlines()
               EndRow=Row[-1]
               datta=EndRow.split(" ")
               WholeRow=list(map(float,datta))
               VoltageOutput = WholeRow[0]
               VoltageInput = WholeRow[1]
               Save.close()
               pass
        except KeyboardInterrupt:
           if device is not None and device.is_open():
              device.close()
              
        import http.client
        import time
        import urllib


            # API KEY
        THINGSPEAK_APIKEY = '30JE4MVSUT6X21LM'
        print("Welcome to the ThingSpeak Raspberry Pi Sensor 6, Press CTRL+C to stop.")
        
        # Setup the data to send in a JSON (dictionary)
        params = urllib.parse.urlencode(
            {
                'field1': VoltageOutput,
                'field2': VoltageInput,
                'key': THINGSPEAK_APIKEY,
            }
        )
        
        # Create the header
        headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': "text/plain"}
        # Create a connection over HTTP
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            # Execute the post (or update) request to upload the data
            conn.request("POST", "/update", params, headers)
            # Check response from server (200 is success)
            response = conn.getresponse()
            # Display response (should be 200)
            print("Response: {0} {1}".format(response.status,response.reason))
            # Read the data for diagnostics
            data = response.read()
            conn.close()
        except Exception as err:
            print("WARNING: ThingSpeak connection failed: {0}, " "data: {1}".format(err, data))
        # Sleep for 20 seconds
        time.sleep(20)
        #except KeyboardInterrupt:
        print("Thanks, bye!")
        
        def sensor2(self):
            Datatxt=open("./Data1.txt","r")
            Ma=[]
            for line in Datatxt:
                lines = (line.rstrip('\n'))
                Row = lines.split(' ')
                RowInt = list(map(float,Row))
                Ma.append(RowInt)
            Datatxt.close()
            # Data print label
            VoltageInputLast = Ma[len(Ma)-1] [0]
            VoltageOutputLast = Ma[len(Ma)-1] [1]
            print (str(self.comboBox.currentText()))
            if(str(self.comboBox.currentText())=="Dato 1"):
                self.LB1.setText(str(VoltageInputLast) +" Volt")
            if(str(self.comboBox.currentText())=="Dato 2"):
                self.LB1.setText(str(VoltageOutputLast) +" Volt")
            print (VoltageOutputLast)
            
        def sensor3(self):
            Datatxt = open("Data1.txt", "r")
            Mat=[]
            for line in Datatxt:
                lines = (line.rstrip('\n'))
                Row = lines.split(' ')
                RowInt = list(map(float,Row))
                Mat.append(RowInt)
            Datatxt.close()
            Tim=len(Mat)
            VoltageInput=[]
            VoltageOutput=[]
            for vis in range(Tim):
                VoltageInput.append(Mat[vis] [0])
                VoltageOutput.append(Mat[vis] [1])
                
            OutputMax = np.amax(VoltageOutput)+1
            ran=np.arange(0,OutputMax,1)
            plt.plot(VoltageInput,'y')
            plt.plot(VoltageOutput,'r')
            plt.xlabel('Eje X')
            plt.ylabel('Eje Y')   
            plt.title('Grafica Voltaje')
            plt.legend()
            plt.show()
    
'''       
         def sensor4(self):
            x= np.arange(1,201,1)
            
            plt.plot(x, S_Temperatura,linestyle=':', marker='.', markerfacecolor='green') 
            plt.xlabel('Tiempo (t)')
            plt.ylabel('Temperatura(°C)')
            plt.grid(True)
            plt.show()
          
        
            
        def led(self):
            
                    # Pin assignments
            import  RPi.GPIO as GPIO
            LED_PIN = 7
            BUTTON_PIN = 17
            # Setup GPIO module and pins
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LED_PIN, GPIO.OUT)
            GPIO.setup(BUTTON_PIN, GPIO.IN)
            # Set LED pin to OFF (no voltage)
            GPIO.output(LED_PIN, GPIO.LOW)
            try:
                # Loop forever
                while 1:
                    # Detect voltage on button pin
                    if GPIO.input(BUTTON_PIN) == 1:
                        # Turn on the LED
                        GPIO.output(LED_PIN, GPIO.HIGH)
                    else:
                        # Turn off the LED
                        GPIO.output(LED_PIN, GPIO.LOW)
            except KeyboardInterrupt:
                print('error')
            finally:
                GPIO.cleanup()
 '''                    
def main():
        import sys
        print('inicia')
        app=QtWidgets.QApplication(sys.argv)
        ventana=Principal()
        ventana.show()
        sys.exit(app.exec_())
        
if __name__=="__main__":
        main()
    