## Toggle an LED when the GUI button is pressed ##

from tkinter import *
import tkinter.font
import time
#from mcp23017 import *
#import smbus
GPA0 = 0
GPA1 = 1
GPA2 = 2
GPA3 = 3
GPA4 = 4
GPA5 = 5
GPA6 = 6
GPA7 = 7
GPB0 = 8
GPB1 = 9
GPB2 = 10
GPB3 = 11
GPB4 = 12
GPB5 = 13
GPB6 = 14
GPB7 = 15
ALL_GPIO = [GPA0, GPA1, GPA2, GPA3, GPA4, GPA5, GPA6, GPA7, GPB0, GPB1, GPB2, GPB3, GPB4, GPB5, GPB6, GPB7]

HIGH = 0xFF
LOW = 0x00

INPUT = 0xFF
OUTPUT = 0x00

#GPIO.setmode(GPIO.BOARD)


class Relay:
  def __init__(self, gpioNumber, mcpController, name, window, row, col):
    self.name = name
    self.gpioNumber = gpioNumber
    #self.mcpController = mcpController
    self.status = False
    #GPIO.setup(gpioNumber, GPIO.OUT)
    self.window = window
    self.row = row
    self.col = col
    self.button = Button(self.window, text=self.name, font=myFont, command=self.flip, bg='bisque2', height=1, width=24)
    self.button.grid(row=self.row,column=self.col)

  def flip(self):
    if self.status:
        print("Flipping Relay " + self.name + " from on to off")
        self.status = False
        #self.mcpController.digitalWrite(self.gpioNumber, LOW)
    else:
        print("Flipping Relay " + self.name + " from off to on")
        self.status = True
        #self.mcpController.digitalWrite(self.gpioNumber, HIGH)
    

def close():
    #RPi.GPIO.cleanup()
    win.destroy()

### Controller Definitions ###

#bus = smbus.SMBus(1)

#mcp1 = MCP23017(0x26, bus)  
#mcp2 = MCP23017(0x27, bus)  

mcp1 = 'mcp1'
mcp2 = 'mcp2'


### GUI DEFINITIONS ###
win = Tk()
win.title("Relay Controller")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

### WIDGETS ###

buttons = []
buttons.append(Relay(GPA0, mcp1, "Main cabin", win, 1, 1))
buttons.append(Relay(GPA1, mcp1, "Stb Fwd", win, 2, 1))
buttons.append(Relay(GPA2, mcp1, "Port Aft", win, 3, 1))
buttons.append(Relay(GPA3, mcp1, "Workshop", win, 4, 1))
buttons.append(Relay(GPA4, mcp1, "Port Fwd", win, 5, 1))
buttons.append(Relay(GPA5, mcp1, "Saloon", win, 6, 1))
buttons.append(Relay(GPA6, mcp1, "Stair", win, 7, 1))
buttons.append(Relay(GPA7, mcp1, "Underwater", win, 8, 1))
buttons.append(Relay(GPB0, mcp1, "Courtesy", win, 9, 1))
buttons.append(Relay(GPB1, mcp1, "Spreader", win, 10, 1))
buttons.append(Relay(GPB2, mcp1, "Awning", win, 11, 1))
buttons.append(Relay(GPB3, mcp1, "Landing", win, 12, 1))
buttons.append(Relay(GPB4, mcp1, "Tricolor", win, 13, 1))
buttons.append(Relay(GPB5, mcp1, "Anchor", win, 14, 1))
buttons.append(Relay(GPB6, mcp1, "Steaming", win, 15, 1))
buttons.append(Relay(GPB7, mcp1, "Lower Nav", win, 16, 1))
buttons.append(Relay(GPA0, mcp2, "Fuel  P-S", win, 1, 2))
buttons.append(Relay(GPA1, mcp2, "Fuel  S-P", win, 2, 2))
buttons.append(Relay(GPA2, mcp2, "Generator", win, 3, 2))
buttons.append(Relay(GPA3, mcp2, "240 V Invert", win, 4, 2))
buttons.append(Relay(GPA4, mcp2, "120 V Invert", win, 5, 2))
buttons.append(Relay(GPA5, mcp2, "TV", win, 6, 2))
buttons.append(Relay(GPA6, mcp2, "Watermaker", win, 7, 2))
buttons.append(Relay(GPA7, mcp2, "Spare", win, 8, 2))
buttons.append(Relay(GPB0, mcp2, "Instruments", win, 9, 2))
buttons.append(Relay(GPB1, mcp2, "Autopilot", win, 10, 2))
buttons.append(Relay(GPB2, mcp2, "VHF", win, 11, 2))
buttons.append(Relay(GPB3, mcp2, "Radar", win, 12, 2))
buttons.append(Relay(GPB4, mcp2, "Furler", win, 13, 2))
buttons.append(Relay(GPB5, mcp2, "Music", win, 14, 2))
buttons.append(Relay(GPB6, mcp2, "Video", win, 15, 2))
buttons.append(Relay(GPB7, mcp2, "Security", win, 16, 2))

exitButton = Button(win, text='Exit', font=myFont, command=close, bg='red', height=1, width=6)
exitButton.grid(row=17, column=1)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window
win.mainloop() # Loops forever
