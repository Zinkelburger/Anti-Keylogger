import pyautogui
import random
from pynput import keyboard

# note to the wise:
"""
PyAutoGUI has a built in failsafe to terminate the program at any time. 
Just move your mouse to the top left corner of your main monitor where your x, y values 
would be 0, 0.
"""
def main():
    # loops inspired by https://www.reddit.com/r/learnpython/comments/8y0p3j/how_do_i_stop_for_loop_with_keyboard_listener/
    # possible improvement could be a "non blocking statement": https://stackoverflow.com/questions/59208869/python-multithreading-with-pynput-keyboard-listener
    with keyboard.Listener(on_press=on_press_start) as l:
        l.join()

    with keyboard.Listener(on_press=on_press_stop) as listener:
        while listener.running:
            doStuff()

def on_press_start(key):
    if key == keyboard.Key.ctrl_r:
        print("starting")
        return False

def on_press_stop(key):
    if key == keyboard.Key.ctrl_r:
        print("stopping")
        return False


def doStuff():
    # a = none uses the system time as the seed. Version 2 is the more modern version and convres everything to an int and uses all 4 bytes
    random.seed(a=None, version=2)

    #the number of random characters to write, 1 to 2
    #I tried random.randint(1, 5) initially, but it is too many I think. Just do 1
    #numChars =
    #for x in range(0, numChars):

    # write a random ascii value to the screen between 32, 127 inclusive
    # 32 is a space, before it are the control characters, 127 isDdelete
    pyautogui.write([chr(random.randint(32, 126)), "backspace"], interval =0)
    #pyautogui.press("backspace")


if __name__ == '__main__':
    main()






