# -*- coding: utf-8 -*-
"""
Created on Sat May 27 09:44:20 2023

@author: SANTIAGO MEDINA

DISEÑO E IMPLEMENTACIÓN DE LA INTERFAZ DEL EJERCICIO_1

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
'''from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine,IOMode'''

Rango_datos=200
S_Proximidad = np.random.randint(0, 10, Rango_datos)#datos de distancia de 0 a 10 metros
S_Velocidad = np.random.randint(1, 35,Rango_datos)#datos de velocidad de 1 a 35 km/h
S_Peso = np.random.randint(10, 100, Rango_datos)#datos de pesos entre 10 y 100 kg
S_Temperatura = np.random.randint(0,100, Rango_datos)#datos de temperatura de 0 a 100 °C
      
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
        self.LED.clicked.connect(self.led)
        '''self.XBee.clicked.connect(self.XBee)'''
        
        self.Tabla_datos()
    
    def Tabla_datos(self):
        
        data = []
        with open ("./Ejercicio_1.txt", "r") as file:
            for line in file:
                line_data = line.strip().split()
                data.append(line_data)
        
        self.Tabla.setColumnCount(len(data[0]))
        self.Tabla.setRowCount(len(data))
        self.Tabla.setHorizontalHeaderLabels(['fecha', 'Hora', 'S_Proximidad', 'S_Velocidad', 'S_Peso','S_Temperatura'])
        
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.Tabla.setItem(i, j, QtWidgets.QTableWidgetItem(item))
    
    '''def XBee(self):
        
        SERIAL_PORT="/dev/ttyS0"
        BAUD_RATE=9600
        REMOTE_NODE_ID="TMP36"
        ANALOG_LINE=IOLine.DIO3_AD3
        SAMPLING_RATE = 15
        device=XBeeDevice(SERIAL_PORT,BAUD_RATE)
        
        #
        from __future__ import print_function
        # Python imports
        import http.client
        import time
        import urllib


        # API KEY
        THINGSPEAK_APIKEY = '30JE4MVSUT6X21LM'
        print("Welcome to the ThingSpeak Raspberry Pi temperature sensor 6! Press CTRL+C to stop.")
        try:
          while 1:
             # Calcula la temperatura en °C
             Temp_C = ((500 * 3.30) - 0.5) * 10
             # Calculate velocidad en km/h
             Vel_Km = (10 * 9.0 / 5.0) + 50.0
             # Calculate Peso en kg
             Peso_kg = (2.58 * 35) + 20     
             # Calculate Proximidad en m
             Prox_m = (Vel_Km + 50)
             
             # Display the results for diagnostics
             print("Uploading {0:.2f} C, {1:.2f} F" "".format(Temp_C, Vel_Km), end=' ... ')
             # Setup the data to send in a JSON (dictionary)
             params = urllib.parse.urlencode(
                  {
                     'field1': Temp_C,
                     'field2': Vel_Km,
                     'field3': Peso_kg,
                     'field4': Prox_m,
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
        except KeyboardInterrupt:
             print("Thanks, bye!")
        exit(0)'''

    def comparacion(self):
        x= np.arange(1,201,1)
        fig, (axs0, axs1, axs2, axs3) = plt.subplots(4, 1)
        
        axs0.plot(x, S_Proximidad, linestyle='--', marker='*', markerfacecolor='blue')
        axs0.set_ylabel('Distancia (m)')
        axs0.grid(True)
        
        axs1.plot(x, S_Velocidad,linestyle='--', marker='o', markerfacecolor='pink') 
        axs1.set_ylabel('Velocidad (km/h)')
        axs1.grid(True)
        
        axs2.plot(x, S_Peso,linestyle=':', marker='o', markerfacecolor='red') 
        axs2.set_ylabel('Peso(Kg)')
        axs2.grid(True)
        
        axs3.plot(x, S_Temperatura,linestyle=':', marker='.', markerfacecolor='green') 
        axs3.set_xlabel('Tiempo (t)')
        axs3.set_ylabel('Temperatura(°C)')
        axs3.grid(True)
        plt.show()
    
    def sensor1(self):
        x= np.arange(1,201,1)
                
        plt.plot(x, S_Proximidad, linestyle='--', marker='*', markerfacecolor='blue')
        plt.xlabel('Tiempo (t)')
        plt.ylabel('Distancia (m)')
        plt.grid(True)
        plt.show()
        
    def sensor2(self):
        x= np.arange(1,201,1)
        
        plt.plot(x, S_Velocidad,linestyle='--', marker='o', markerfacecolor='pink') 
        plt.xlabel('Tiempo(t)')
        plt.ylabel('Velocidad (km/h)')
        plt.grid(True)
        plt.show()
        
    def sensor3(self):
        x= np.arange(1,201,1)
        
        plt.plot(x, S_Peso,linestyle=':', marker='o', markerfacecolor='red') 
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Peso(Kg)')
        plt.grid(True)
        plt.show()

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
                
                
def main():
    import sys
    print('inicia')
    app=QtWidgets.QApplication(sys.argv)
    ventana=Principal()
    ventana.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main()
    