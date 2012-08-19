#-------------------------------------------------------------------------------
# Name:        i2c_lcd
# Purpose:
#
# Author:      Eric Gero
#
# Created:     08/18/2012
#
#Beaglebone  
#	SCL P9 pin 19
#	SDA P9 pin 20
#Raspberry Pi  
#	SCL pin 5
#	SDA pin 3
#MCP23008
#	RS - GP1
#	EN - GP2
#	DB4 - GP3
#	DB5 - GP4
#	DB6 - GP5
#	DB7 - GP6
#	Light - GP7
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import i2c, time

IOMODE = 0x00
IOPOL = 0x01
IOCON = 0x05
GPIO = 0x09

class LCD:
    def __init__(self, address):
        self.address = address
        self.lcd = i2c.I2C(address)
        time.sleep(.2)
        
        self.set_iocon(0x20)			# turn of sequential increment on MCP23008
        self.set_io(0x00)				# set pins on MCP23008 to output
        

        self.lcd_command(0x03)			# start initialization of lcd as described in datasheet
        time.sleep(0.005)

        self.lcd_command(0x03)
        time.sleep(0.0002)

        self.lcd_command(0x03)
        time.sleep(0.0002)

        self.lcd_command(0x02)
        time.sleep(.05)

        self.lcd_command(0x28)  		# set 4 bit, 2 lines
        self.lcd_command(0x08)  		# no shift, hide cursor
        self.lcd_command(0x01)  		# clear display
        self.lcd_command(0x06)  		# cursor increment - right
        self.lcd_command(0x0F)  		# turn on display - no cursor
        self.lcd_command(0x80)  		# DDRAM address

    def lcd_send(self, data):			# Send data to MCP23008; this function is not called directly
        self.send_gpio(data | 0x80)

    def lcd_command(self, data):    
        highnib = (data >> 1) & 0x78	# Offset value so data is in bits 6,5,4,3
        lownib = (data << 3) & 0x78

        self.lcd_send((highnib | 0x04)) # Enable
        time.sleep(.001)
        self.lcd_send(highnib )			# This works similar to the pulseEnable functions seen in many examples
        time.sleep(.001)

        self.lcd_send(lownib | 0x04) 	# Enable
        time.sleep(.001)
        self.lcd_send(lownib)

    def lcd_write(self, data):
        highnib = (data >> 1) & 0x78  	# Offset value so data is in bits 6,5,4,3
        lownib = (data << 3) & 0x78

        self.lcd_send(highnib | 0x06) 	# Enable and RS
        time.sleep(.001)
        self.lcd_send(highnib | 0x02) 	# RS
        time.sleep(.001)

        self.lcd_send(lownib | 0x06) 	# Enable and RS
        time.sleep(.001)
        self.lcd_send(lownib | 0x02) 	# RS

    def prints(self, string):			# Print string to LCD
        for ch in string:
            self.lcd_write(ord(ch))

    def clear(self):					# Clear screen
        self.lcd_command(0x01)

    def lcd_home(self):					# Move to home position
        self.lcd_command(0x80)
        
    def lcd_line_one(self, pos):		# Move to line 1
        self.lcd_command(0x80 + pos)

    def lcd_line_two(self, pos):		# Move to line 2
        self.lcd_command(0x80 | (0x40 + pos))

    def lcd_make_char(self, pos, character):	# Create custom characters and store in memory
        pos = pos & 0x07
        self.lcd_command(0x40 | (pos << 3))
        for ch in character:
            self.lcd_write(ch)

    def lcd_print_custom_char(self, pos):		# Print custom characters stored in memory
        self.lcd_write(pos)

    def set_io(self, value):			# Set direction of gpio pins on MCP23008
		self.lcd.i2c_begin_transmission()
		self.lcd.i2c_send(IOMODE)
		self.lcd.i2c_send(value)
		self.lcd.i2c_end_transmission()
		
    def set_iocon(self, value):			# Disable sequential increment on MCP23008
		self.lcd.i2c_begin_transmission()
		self.lcd.i2c_send(IOCON)
		self.lcd.i2c_send(value)
		self.lcd.i2c_end_transmission()

    def set_polarity(self, value):		# Set polarity of gpio pins on MCP23008; not used here
		self.lcd.i2c_begin_transmission()
		self.lcd.i2c_send(IOPOL)
		self.lcd.i2c_send(value)
		self.lcd.i2c_end_transmission()
		
    def send_gpio(self, value):			# Send opcode then data to MCP23008
		self.lcd.i2c_begin_transmission()
		self.lcd.i2c_send(GPIO)
		self.lcd.i2c_send(value)
		self.lcd.i2c_end_transmission()
