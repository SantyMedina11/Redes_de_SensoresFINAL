# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 20:51:18 2022

@author: precision
"""

# March 2020
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
exit(0)