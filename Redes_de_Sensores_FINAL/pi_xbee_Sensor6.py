# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 05:37:29 2022

@author: precision
"""
#
# Raspberry Pi Data Aggregator - Beginning Sensor Networks Second Edition
#
# For this script. we read data from an XBee remote data mode
# from a ZigBee Coordinator connected to a Raspberry Pi via a
# serial interface.

#
# The data read includes an analog value from DIO3/AD3 and the current voltage value.
#
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
# Serial port on Raspberry Pi
SERIAL_PORT = "/dev/ttyUSB0"  # "/dev/ttyS0"
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

# Method to connect to the network and get the remote node by id
def get_remote_device():
   """Get the remote node from the network 
   Returns:
   """
   # Request the network class and search the network for the remote node
   xbee_network = device.get_network()
   remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
   if remote_device is None:
      print("ERROR: Remote node id {0} not found.".format(REMOTE_NODE_ID))
      exit(1)
   remote_device.set_dest_address(device.get_64bit_addr())
   remote_device.set_io_configuration(ANALOG_LINE, IOMode.ADC)
   remote_device.set_io_sampling_rate(SAMPLING_RATE)

def io_sample_callback(sample, remote, time):
   print("Reading from {0} at {1}:".format(REMOTE_NODE_ID, remote.get_64bit_addr()))
   # Get the temperature in Celsius
   temp_c = ((sample.get_analog_value(ANALOG_LINE) * 1200.0 / 1024.0) - 500.0) / 10.0
   # Calculate temperature in Fahrenheit
   temp_f = ((temp_c * 9.0) / 5.0) + 32.0
   print("\tTemperature is {0}C. {1}F".format(temp_c, temp_f))
   # Calculate supply voltage
   volts = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
   print("\tSupply voltage = {0}v".format(volts))

try:
   print("Welcome to example of reading a remote TMP36 sensor!")
   device.open() # Open the device class
   # Setup the remote device
   get_remote_device()
   # Register a listener to handle the samples received by the local device.
   device.add_io_sample_received_callback(io_sample_callback)
   while True:
       pass
except KeyboardInterrupt:
   if device is not None and device.is_open():
      device.close()