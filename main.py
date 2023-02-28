import pyautogui
import random
import os
from time import sleep
from pynput import keyboard

#note to the wise:
"""
PyAutoGUI has a built in failsafe to terminate the program at any time. 
Just move your mouse to the top left corner of your main monitor where your x, y values 
would be 0, 0.
"""
#epic global variables
#I don't want to use global variables, I have grown to dislike pynput. Probably will just use SFML in c++ in the future
rightCtrlPressed = False
def main():
    #alt tab into the text editor (open the text editor and minimize it before running the program)
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    # open a text edtior of your choice. I chose xed, windows could use notepad
    #os.system("xed")*
    # get the active window (the window you want to typ:ce stuff in), and the xed window (the one to type garbage in)

    with keyboard.Listener(on_press=on_press) as l:
        l.join()

def doStuff():
    # place your mouse on the box you want to type in
    x, y = pyautogui.position()
    # move the cursor to the right window, where there ix xed
    pyautogui.moveTo(1000, 200)
    pyautogui.click()
    # a = none uses the system time as the seed. Version 2 is the more modern version and convres everything to an int and uses all 4 bytes
    random.seed(a=None, version=2)
    # write two random ascii value to the xed between 0, 127 inclusive
    pyautogui.write(chr(random.randint(0, 127)))
    pyautogui.write(chr(random.randint(0, 127)))
    if (random.randint(1, 2) == 1):
        pyautogui.write(chr(random.randint(0, 127)))
    # move the cursor back to the window where the user wants to type
    pyautogui.moveTo(x, y)
    pyautogui.click()
    # sleep for a random amount of time https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
    # this is the user's chance to type
    #actual program will be shorter, test needs a longer time
    sleep(random.uniform(0.5, 1))

def on_press(key):
    global rightCtrlPressed
    #print('\nYou Entered {0}'.format(key))
    #fail safe so your computer is not consumed by random, rapid mouse movement and key presses (happened more than once)
    #spam and hold the right alt button to get the program to exit as a last resort
    if key == keyboard.Key.alt_r:
        return False
    if key == keyboard.Key.ctrl_r:
        if rightCtrlPressed:
            print("Now False")
            rightCtrlPressed = False
            #move the mouse to indicate successful ending
            pyautogui.moveTo(0, 0)
            sleep(2)
        else:
            print("Now True")
            rightCtrlPressed = True;

    if rightCtrlPressed:
        doStuff()
            
if __name__ == '__main__':
    main()






