#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import time
import math
import smbus
import RPi.GPIO as GPIO

ADDR                = (0x58)

# int pin
INI_PIN = 23
RST_PIN = 24

class AW9523B:
    def __init__(self, address=ADDR, debug=1):
        self.i2c = smbus.SMBus(1)
        self.address = address
        
        self.debug = debug
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(INI_PIN, GPIO.IN)
        
        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.output(RST_PIN, 0)
        time.sleep(0.1)
        GPIO.output(RST_PIN, 1)

        self.ID = self.ReadByte(0x10) # ID
        if(self.ID != 0x23): # ID = 0X23
            print("not find AW9523B")
            sys.exit()
        else:
            print("find AW9523B, ID = 0x%x"%(self.ID))
            
        self.LEDModeSwitch(0, 1)#set out mode gpio
        self.PortCtrl(1, 0) #set all gpio Push-Pull
        self.LEDModeSwitch(1, 1)#set out mode gpio
        
    def ReadByte(self, Addr):
        return self.i2c.read_byte_data(self.address, Addr)

    def WriteByte(self, Addr, val):
        self.i2c.write_byte_data(self.address, Addr, val & 0xFF)

    #port 8pin
    def PortMode(self, port, mode):#port:04H 05H , mode:0-out 1-in
        if(self.debug == 1):
            print("set port%d mode = %s"%(port, "out" if mode==0 else "in"))
        self.WriteByte(0x04 if port==0 else 0x05, 0 if mode==0 else 0xff)
    def PortInput(self, port):#port:00h 01H
        if(self.debug == 1):
            print("input port%d val = 0x%x"%(port, self.ReadByte(0x00 if port==0 else 0x01)))
        return self.ReadByte(0x00 if port==0 else 0x01)
    def PortOutput(self, port, val):#port:02H 03H , mode:0-Llev 0xff-Hlev
        if(self.debug == 1):
            print("output port%d val = 0x%x"%(port, val))		
        self.WriteByte(0x02 if port==0 else 0x03, val)
    def PortInt(self, port, en):#port:06h 07h, en:0-enable 1-uenable
        if(self.debug == 1):
            print("enable port%d int = 0x%x"%(port, en))
        self.WriteByte(0x06 if port==0 else 0x07, en)
    def PortIntClear(self, port):#port:06h 07h, en:0-enable 1-uenable
        if(self.debug == 1):
            print("clear port%d int" %port)
        self.ReadByte(0x06 if port==0 else 0x07)

    def PinMode(self, port, pin, mode):#port:04H 05H , mode:0-out 1-in
        self.WriteByte(0x04 if port==0 else 0x05, mode<<pin)
    def PinInput(self, port, pin):#port:00h 01H
        return self.ReadByte(0x00 if port==0 else 0x01)&(1<<pin)
    def PinOutput(self, port, pin, val):#port:02H 03H , mode:0-Llev 0-Hlev
        self.WriteByte(0x02 if port==0 else 0x03, val<<pin)
    def PinInt(self, port, pin, en):#port:06h 07h, en:0-enable 1-uenable
        self.WriteByte(0x06 if port==0 else 0x07, en<<pin)
        
    #gpomd=D[4]:0-Open-Drain 1-Push-Pull; just p0
    #iseld[1:0]:00-11(IMAX×1/4,IMAX×2/4, IMAX×3/4,IMAX)
    def PortCtrl(self,  gpomd, isel):
        g = gpomd << 4
        s = isel << 2
        val = g | s
        self.WriteByte(0x11, val)#AW9523B_REG_GLOB_CTR
        
    def LEDModeSwitch(self, port, mode):# PORT 12H 13H, MODE:0(led) 1(gpio)
        self.WriteByte(0x12 if port==0 else 0x13, 0 if mode==0 else 0xff)

    def LEDDims(self, lednum, i):# lednum:0x20->0x2F, i: i/255×IMAX, IMAX= 37Ma
        self.WriteByte(lednum, i)

if __name__ == '__main__':
    print("test:Connect the 0 port to the 1 port")
    gpio = AW9523B()

    #ouput
    gpio.PortMode(0, 0)
    # gpio.PortOutput(0, 0xf0)
    # gpio.PortMode(1, 0)
    # gpio.PortOutput(1, 0xff)
    # gpio.PortInput(1)

    #input	
    gpio.PortMode(1, 1) 
    gpio.PortInt(1, 0)
    tm = 1
    # while(1):		
    for x in range(0, 8):
        gpio.PortOutput(0, 1<<x)
        time.sleep(0.1)
        if(GPIO.input(INI_PIN) == 0):
            while(GPIO.input(INI_PIN) != 0):
                # gpio.PortIntClear(1)
                print("sss")
            gpio.PortInput(1)
            print("read is change, Trigger interrupted %d" %tm)			
        tm = tm + 1

