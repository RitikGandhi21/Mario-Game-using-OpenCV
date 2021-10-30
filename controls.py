from pynput.keyboard import Key, Controller
import time


keyboard = Controller()

global key
global space_pressed

key = None
space_pressed = False




def do_nothing():
    global key
    global space_pressed

    
    if space_pressed:
        keyboard.release(Key.space)
        space_pressed = False

    if key != None:
        keyboard.release(key)

def move_left():

    global key
    global space_pressed

    
    if space_pressed:
        keyboard.release(Key.space)
        space_pressed = False

    if key == 'd':
        keyboard.release(key)

    key = 'a'
    for i in range(100):
        keyboard.press(key)

def move_right():
    global key
    global space_pressed
    
    
    if space_pressed:
        keyboard.release(Key.space)
        space_pressed = False

    if key == 'a':
        keyboard.release(key)

    key = 'd'
    for i in range(100):
        keyboard.press(key)

    

def jump():

    global key
    global space_pressed 

    
    if key != None:
        keyboard.release(key)

    keyboard.press(Key.space)

    space_pressed = True
   

