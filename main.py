from tkinter import *
import random
from console.main import Console
from data.Students import Students
from lib.Window import Window
from threading import Thread

students = Students()


# Mainframe
def startWindow():
    Window().show()


# Console
def startConsole():
    mainloop = True
    while mainloop:
        mainloop = Console(students).reader(input())


t1 = Thread(target=startConsole)
t2 = Thread(target=startWindow)

t1.start()
t2.start()
