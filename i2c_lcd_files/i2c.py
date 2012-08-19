#-------------------------------------------------------------------------------
# Name:        i2c
# Purpose:
#
# Author:      Eric Gero
#
# Created:     08/18/2012
#
# Beaglebone - '/dev/i2c-3'
# Raspberry Pi - '/dev/i2c-0'
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import fcntl

IOCTL_I2C_SLAVE = 0x0703

class I2C:

    def __init__(self, address):
        self.address = address
        self.fileHandle = None

    def i2c_begin_transmission(self):
        if self.fileHandle:
            self.end_transmission()
            raise Exception('File is already open.')
        self.fileHandle = open('/dev/i2c-0', 'r+', 1)
        fcntl.ioctl(self.fileHandle, IOCTL_I2C_SLAVE, self.address)

    def i2c_write(self, val):
        if not self.fileHandle:
            raise Exception('File must be open before writing.')
        self.fileHandle.write(val)
        self.fileHandle.flush()

    def i2c_read(self):
        if not self.fileHandle:
            raise Exception('File must be open before reading.')
        line = self.fileHandle.read(1)
        return line

    def i2c_send(self, val):
        if not self.fileHandle:
            raise Exception('File must be open before writing.')
        self.fileHandle.write(chr(val))

    def i2c_end_transmission(self):
        self.fileHandle.close()
        self.fileHandle = None
