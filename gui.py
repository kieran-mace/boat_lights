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
window.geometry("800x600")  # Set the initial window size


myFont = tkinter.font.Font(family = 'Helvetica', size = 26, weight = "bold")

# Configure the grid columns to be proportional
for i in range(6):
    window.grid_columnconfigure(i, weight=1)

# Create a frame to hold your buttons
frame = tk.Frame(window)
frame.pack(fill="both", expand=True)

# Create the buttons and set their size based on the window width
button_width = int((window.winfo_width() - 20) / 6)  # Adjust this value as needed
button_height = int((window.winfo_height() - 20) / 9)

### WIDGETS ###

buttons = []
labels = []
# Interior Lights
label = Label(frame, text="Interior Lights", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 1)
labels.append(label)
buttons.append(Relay(GPA0, mcp1, "Main cabin", frame, 2, 1))
buttons.append(Relay(GPA1, mcp1, "Stb Fwd", frame, 3, 1))
buttons.append(Relay(GPA2, mcp1, "Port Aft", frame, 4, 1))
buttons.append(Relay(GPA3, mcp1, "Workshop", frame, 5, 1))
buttons.append(Relay(GPA4, mcp1, "Port Fwd", frame, 6, 1))
buttons.append(Relay(GPA5, mcp1, "Saloon", frame, 7, 1))
buttons.append(Relay(GPA6, mcp1, "Stair", frame, 8, 1))
# Exterior Lights
label = Label(frame, text="Exterior Lights", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 2)
labels.append(label)
buttons.append(Relay(GPA7, mcp1, "Underwater", frame, 2, 2))
buttons.append(Relay(GPB0, mcp1, "Courtesy", frame, 3, 2))
buttons.append(Relay(GPB1, mcp1, "Spreader", frame, 4, 2))
buttons.append(Relay(GPB2, mcp1, "Awning", frame, 5, 2))
buttons.append(Relay(GPB3, mcp1, "Landing", frame, 6, 2))
# Navigation Lights
label = Label(frame, text="Navigation Lights", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 3)
labels.append(label)
buttons.append(Relay(GPB4, mcp1, "Tricolor", frame, 2, 3))
buttons.append(Relay(GPB5, mcp1, "Anchor", frame, 3, 3))
buttons.append(Relay(GPB6, mcp1, "Steaming", frame, 4, 3))
buttons.append(Relay(GPB7, mcp1, "Lower Nav", frame, 5, 3))
# Pumps
label = Label(frame, text="Pumps", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 4)
labels.append(label)
buttons.append(TemporaryRelay(GPA0, mcp2, "Fuel  P-S", frame, 2, 4))
buttons.append(TemporaryRelay(GPA1, mcp2, "Fuel  S-P", frame, 3, 4))
# Electrical
label = Label(frame, text="Electrical", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 5)
labels.append(label)
buttons.append(Relay(GPA2, mcp2, "Generator", frame, 2, 5))
buttons.append(Relay(GPA3, mcp2, "240 V Invert", frame, 3, 5))
buttons.append(Relay(GPA4, mcp2, "120 V Invert", frame, 4, 5))
buttons.append(Relay(GPA5, mcp2, "TV", frame, 5, 5))
buttons.append(Relay(GPA6, mcp2, "Watermaker", frame, 6, 5))
buttons.append(Relay(GPA7, mcp2, "Spare", frame, 7, 5))
# Electronics
label = Label(frame, text="Electronics", font=myFont, width=button_width, height=button_height)
label.grid(row = 1, column = 6)
labels.append(label)
buttons.append(Relay(GPB0, mcp2, "Instruments", frame, 2, 6))
buttons.append(Relay(GPB1, mcp2, "Autopilot", frame, 3, 6))
buttons.append(Relay(GPB2, mcp2, "VHF", frame, 4, 6))
buttons.append(Relay(GPB3, mcp2, "Radar", frame, 5, 6))
buttons.append(Relay(GPB4, mcp2, "Furler", frame, 6, 6))
buttons.append(Relay(GPB5, mcp2, "Music", frame, 7, 6))
buttons.append(Relay(GPB6, mcp2, "Video", frame, 8, 6))
buttons.append(Relay(GPB7, mcp2, "Security", frame, 9, 6))

exitButton = Button(frame, text='Exit', font=myFont, command=close, bg='blue', height=button_height, width=button_width)
exitButton.grid(row=9, column=1)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window
win.mainloop() # Loops forever
