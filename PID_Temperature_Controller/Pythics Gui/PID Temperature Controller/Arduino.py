# Created by Connor McPartland
# University of Pittsburgh 2013

# An Arduino class
# Provides basic communication via Serial port


import serial

class Arduino:
    def __init__(self, COM= 'COM1', baudrate = 9600, timeout = 5.0):
        self.arduino = serial.Serial()
        self.arduino.port = COM 
        self.arduino.baudrate = baudrate
        self.arduino.timeout = timeout
        self.is_connected = False
        self.ID = ''
        self.ready = False
    
    def connect(self):
        try:
            self.arduino.open()
        except serial.SerialException:
            print 'Error in connecting to Arduino on %s.'%self.arduino.port
        else:
            if self.arduino.isOpen():
                self.is_connected = True
                print 'Successfully connected on %s.'%self.arduino.port
                if self.read() == 'Serial ready':
                    self.is_ready = True
                    self.write('r');
                    self.ID = self.read();
                else:
                    self.is_ready = False
                return True
            else:
                self.is_connected = False
                return False
    
    def disconnect(self):
        try:
            self.arduino.close()
        except serial.SerialException:
            print 'Error in disconnecting Arduino.'
        else:
            if not self.arduino.isOpen():
                self.is_connected = False
                return True
            else:
                self.is_connected = True
                print 'Successfully disconnected Arduino.'
                return False
    
    def write(self, message):
        try:
            self.arduino.write(message)
            self.arduino.flushInput()
        except serial.SerialException:
            print 'Error in writing %s to Arduino'%message
    
    def read(self):
        try:
            self.arduino.flush()
            response = self.arduino.readline().strip()
        except serial.SerialException:
            print 'Error in reading from Arduino.'
        else:
            return response
        