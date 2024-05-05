## Toggle an LED when the GUI button is pressed ##

from tkinter import *
import tkinter.font
import time
from mcp23017 import *
import smbus

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

class Relay:
  def __init__(self, gpioNumber, mcpController, name, window, row, col):
    self.name = name
    self.gpioNumber = gpioNumber
    self.mcpController = mcpController
    self.status = False
    self.window = window
    self.row = row
    self.col = col
    self.button = Button(self.window, text=self.name, font=myFont, command=self.flip, bg='bisque2', height=button_height, width=button_width)
    self.button.grid(row=self.row,column=self.col)

  def flip(self):
    if self.status:
        print("Flipping Relay " + self.name + " from on to off")
        self.status = False
        self.mcpController.digital_write(self.gpioNumber, LOW)
        self.button.config(bg="bisque2")
    else:
        print("Flipping Relay " + self.name + " from off to on")
        self.status = True
        self.mcpController.digital_write(self.gpioNumber, HIGH)
        self.button.config(bg="red")
    
class TemporaryRelay(Relay):
    def __init__(self, gpioNumber, mcpController, name, window, row, col):
        super().__init__(gpioNumber, mcpController, name, window, row, col)
        self.timer = None

    def flip(self):
        if self.status:
            print("Flipping Relay " + self.name + " from on to off")
            self.status = False
            self.mcpController.digital_write(self.gpioNumber, LOW)
            self.button.config(bg="bisque2")
            if self.timer is not None:
                self.window.after_cancel(self.timer)
                self.timer = None
        else:
            print("Flipping Relay " + self.name + " from off to on")
            self.status = True
            self.mcpController.digital_write(self.gpioNumber, HIGH)
            self.button.config(bg="red")
            self.timer = self.window.after(300000, lambda: self.flip())

def close():
    #RPi.GPIO.cleanup()
    win.destroy()

### Controller Definitions ###

MCP23017_IODIRA = 0x00
MCP23017_IODIRB = 0x01
MCP23017_GPIOA = 0x12
MCP23017_GPIOB = 0x13

bus = smbus.SMBus(1)

bus.write_byte_data(0x26,MCP23017_IODIRA,0x00)
bus.write_byte_data(0x26,MCP23017_IODIRB,0x00)
bus.write_byte_data(0x26,MCP23017_GPIOA,0x00)
bus.write_byte_data(0x26,MCP23017_GPIOB,0x00)
mcp1 = MCP23017(0x26, bus)  

# bus.write_byte_data(0x27,MCP23017_IODIRA,0x00)
# bus.write_byte_data(0x27,MCP23017_IODIRB,0x00)
# bus.write_byte_data(0x27,MCP23017_GPIOA,0x00)
# bus.write_byte_data(0x27,MCP23017_GPIOB,0x00)
# mcp2 = MCP23017(0x27, bus)  
mcp2 = 'mcp'

### GUI DEFINITIONS ###
win = Tk()
win.title("Relay Controller")
win.geometry("1920x1200")  # Set the initial win size


myFont = tkinter.font.Font(family = 'Helvetica', size = 35, weight = "bold")

# # Configure the grid columns to be proportional
# for i in range(6):
#     win.grid_columnconfigure(i, weight=1)

# # Create a frame to hold your buttons
# frame = Frame(win)
# frame.pack(fill="both", expand=True)

# Create the buttons and set their size based on the win width
# button_width = int((win.winfo_width() - 20) / 6)  # Adjust this value as needed
# button_height = int((win.winfo_height() - 20) / 9)
button_width = 11  # Adjust this value as needed
button_height = 2
### WIDGETS ###

buttons = []
labels = []
# Interior Lights
label = Label(win, text="Int. Lights", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 1)
labels.append(label)
buttons.append(Relay(GPA0, mcp1, "Main cabin", win, 2, 1))
buttons.append(Relay(GPA1, mcp1, "Stb Fwd", win, 3, 1))
buttons.append(Relay(GPA2, mcp1, "Port Aft", win, 4, 1))
buttons.append(Relay(GPA3, mcp1, "Workshop", win, 5, 1))
buttons.append(Relay(GPA4, mcp1, "Port Fwd", win, 6, 1))
buttons.append(Relay(GPA5, mcp1, "Saloon", win, 7, 1))
buttons.append(Relay(GPA6, mcp1, "Stair", win, 8, 1))
# Exterior Lights
label = Label(win, text="Ext. Lights", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 2)
labels.append(label)
buttons.append(Relay(GPA7, mcp1, "Underwater", win, 2, 2))
buttons.append(Relay(GPB0, mcp1, "Courtesy", win, 3, 2))
buttons.append(Relay(GPB1, mcp1, "Spreader", win, 4, 2))
buttons.append(Relay(GPB2, mcp1, "Awning", win, 5, 2))
buttons.append(Relay(GPB3, mcp1, "Landing", win, 6, 2))
# Navigation Lights
label = Label(win, text="Nav. Lights", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 3)
labels.append(label)
buttons.append(Relay(GPB4, mcp1, "Tricolor", win, 2, 3))
buttons.append(Relay(GPB5, mcp1, "Anchor", win, 3, 3))
buttons.append(Relay(GPB6, mcp1, "Steaming", win, 4, 3))
buttons.append(Relay(GPB7, mcp1, "Lower Nav", win, 5, 3))
# Pumps
label = Label(win, text="Pumps", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 4)
labels.append(label)
buttons.append(TemporaryRelay(GPA0, mcp2, "Fuel  P-S", win, 2, 4))
buttons.append(TemporaryRelay(GPA1, mcp2, "Fuel  S-P", win, 3, 4))
# Electrical
label = Label(win, text="Electrical", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 5)
labels.append(label)
buttons.append(Relay(GPA2, mcp2, "Generator", win, 2, 5))
buttons.append(Relay(GPA3, mcp2, "240 V Invert", win, 3, 5))
buttons.append(Relay(GPA4, mcp2, "120 V Invert", win, 4, 5))
buttons.append(Relay(GPA5, mcp2, "TV", win, 5, 5))
buttons.append(Relay(GPA6, mcp2, "Watermaker", win, 6, 5))
buttons.append(Relay(GPA7, mcp2, "Spare", win, 7, 5))
# Electronics
label = Label(win, text="Electronics", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 6)
labels.append(label)
buttons.append(Relay(GPB0, mcp2, "Instruments", win, 2, 6))
buttons.append(Relay(GPB1, mcp2, "Autopilot", win, 3, 6))
buttons.append(Relay(GPB2, mcp2, "VHF", win, 4, 6))
buttons.append(Relay(GPB3, mcp2, "Radar", win, 5, 6))
buttons.append(Relay(GPB4, mcp2, "Furler", win, 6, 6))
buttons.append(Relay(GPB5, mcp2, "Music", win, 7, 6))
buttons.append(Relay(GPB6, mcp2, "Video", win, 8, 6))
buttons.append(Relay(GPB7, mcp2, "Security", win, 9, 6))

exitButton = Button(win, text='Exit', font=myFont, command=close, bg='blue', height=button_height, width=button_width)
exitButton.grid(row=9, column=1)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window
win.mainloop() # Loops forever
