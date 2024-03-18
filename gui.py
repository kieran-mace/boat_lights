## Toggle an LED when the GUI button is pressed ##

from tkinter import *
import tkinter.font
#import RPi.GPIO as GPIO
import time


#GPIO.setmode(GPIO.BOARD)


class Relay:
  def __init__(self, gpioNumber, name, window, row, col):
    self.name = name
    self.gpioNumber = gpioNumber
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
    else:
        print("Flipping Relay " + self.name + " from off to on")
        self.status = True
    #GPIO.output(self.gpioNumber, not(self.status))


def close():
    #RPi.GPIO.cleanup()
    win.destroy()


### GUI DEFINITIONS ###
win = Tk()
win.title("Relay Controller")
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

### WIDGETS ###

button1 = Relay(16, "Button 16", win, 1, 1)
button2 = Relay(18, "Button 18", win, 1, 2)
exitButton = Button(win, text='Exit', font=myFont, command=close, bg='red', height=1, width=6)
exitButton.grid(row=2, column=1)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window
win.mainloop() # Loops forever
