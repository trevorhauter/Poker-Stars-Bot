import os, time, sys, traceback, subprocess
#be sure to use pynput 1.6.8 because other versions break when using pyinstaller to create EXE
import pynput
from pynput.keyboard import Key, Controller
import psutil,os
import win32gui, win32con, win32api
import re
keyboard = Controller()
import mouse
import pandas as pd

#gets the path that the script lives in - necessary to call the logins.csv file that contains users poker stars logins
path = os.getcwd() + "\\"

#presses shift tab to take the user up a level in the input field
def shiftTab():
    #press shift tab
    keyboard.press(Key.shift)
    keyboard.press(Key.tab)
    keyboard.release(Key.shift)
    keyboard.release(Key.tab)

#function presses the tab button
def tab():
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)

#function presses the enter button
def enter():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

#class used to set windows to the foreground
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

#function kills tasks
def killer(process_name):
    os.system('TASKKILL /F /T /IM ' + process_name + '')

#function types out any word 1 letter at a time
def typeText(text):
    for i in range(len(text)):
        var = text[i:i+1]
        keyboard.press(var)
        keyboard.release(var)

def splitCoordinates(currentPos, idealPos):
    return currentPos[0], currentPos[1], idealPos[0], idealPos[1]

def calculateMovement(currentPos, idealPos):
    #calls a funciton that returns the X and Y values for the current and ideal position for calculations
    curX, curY, idealX, idealY = splitCoordinates(currentPos, idealPos)

    moveX = idealX - curX
    moveY = idealY - curY

    newPos = [moveX, moveY]

    return newPos

def clickChips():
    #the position that we need the mouse to be in order to click the collect chips button
    idealPos = [1634, 40]

    #gets the current position
    currentPos = mouse.get_position()

    # calls a function to calculate what needs to happen so the mouse gets to the correct positon
    x, y = calculateMovement(currentPos, idealPos)
    #moves the mouse to the position
    mouse.move(x, y, absolute=False, duration=0.1)

    #clicks the mouse
    mouse.click('left')

def enterCredentials(username, password):
    shiftTab()
    typeText(username)
    tab()
    typeText(password)
    time.sleep(1)
    enter()

#parent function that carries out the entire process to automate collecting chips
def start():
    logins = pd.read_csv(path + 'logins.csv')
    #loops through the usernames - we use range so we can call the coresponding password... im sure theres a better way to do it but this is what we got
    for i, row in logins.iterrows():
        #starts pokerstars
        os.startfile("C:\\Program Files (x86)\\PokerStars.NET\\PokerStarsUpdate.exe")

        #sets the window to the foreground
        w = WindowMgr()
        w.find_window_wildcard(".*Poker.*")
        w.set_foreground()
        time.sleep(10)

        #gets the username and password
        username = row['username']
        password = row['password']

        print("getting chips for " + username)

        #enters the username and password
        enterCredentials(username, password)

        time.sleep(1)
        #fullscreens the window
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        time.sleep(2)


        #moves the moust and clicks on the collect chips button
        clickChips()
        time.sleep(3)
        # print(os.system("tasklist"))

        print("chips retrieved... killing process...")
        killer("PokerStars.exe")
        print("process killed")
        time.sleep(2)


        print(username)
        print(password)


start()
win32api.MessageBox(0, 'finished', 'Ayo boss all the chips have been collected done')