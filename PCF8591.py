#!/usr/bin/env python
#------------------------------------------------------
#
#		This is a program for PCF8591 Module.
#
#		Warnng! The Analog input MUST NOT be over 3.3V!
#    
#		In this script, we use a poteniometer for analog
#   input, and a LED on AO for analog output.
#
#		you can import this script to another by:
#	import PCF8591 as ADC
#	
#	ADC.Setup(Address)  # Check it by sudo i2cdetect -y -1
#	ADC.read(channal)	# Channal range from 0 to 3
#	ADC.write(Value)	# Value range from 0 to 255		
#
#------------------------------------------------------
import smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

#check your PCF8591 address by type in 'sudo i2cdetect -y -1' in terminal.
def setup(Addr):
	global address
	address = Addr

def read(chn): #channel
	try:
		if chn == 0:
			bus.write_byte(address,0x40)
		if chn == 1:
			bus.write_byte(address,0x41)
		if chn == 2:
			bus.write_byte(address,0x42)
		if chn == 3:
			bus.write_byte(address,0x43)
		bus.read_byte(address) # dummy read to start conversion
		return bus.read_byte(address)
	except:
		return 0

def write(val):
	try:
		temp = val # move string value to temp
		temp = int(temp) # change string to integer
		# print temp to see on terminal else comment out
		bus.write_byte_data(address, 0x40, temp)
	except:pass
