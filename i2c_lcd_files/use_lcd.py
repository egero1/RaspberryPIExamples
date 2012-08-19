#-------------------------------------------------------------------------------
# Name:        use_lcd
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
#!/usr/bin/python

import i2c_lcd, time, i2c

lcd = i2c_lcd.LCD(0x20)
lcd.clear()

lcd.lcd_home()
lcd.prints('Raspberry Pi')
lcd.lcd_line_two(4)
lcd.prints("Is awesome!!")
time.sleep(2)
lcd.lcd_home()

lcd.lcd_home()
lcd.prints('Raspberry Pi')

character = [0x1f,0x10,0x10,0x10,0x10,0x10,0x10,0x1f]
lcd.lcd_make_char(0, character)
lcd.lcd_line_two(0)
lcd.lcd_print_custom_char(0)

character = [0x17,0x15,0x15,0x15,0x17,0x0,0x1f,0x0]
lcd.lcd_make_char(1, character)
lcd.lcd_line_two(1)
lcd.lcd_print_custom_char(1)

character = [0xa,0xa,0xa,0xa,0xa,0x0,0x1f,0x0]
lcd.lcd_make_char(2, character)
lcd.lcd_line_two(2)
lcd.lcd_print_custom_char(2)

count = 0

while(count < 100):
    lcd.lcd_line_one(14)
    lcd.prints(str(count))
    print str(count)
    count = count + 1
    time.sleep(.25)


