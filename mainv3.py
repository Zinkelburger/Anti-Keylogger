import pyautogui
import random
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller

# several orders of magnitude above version 1. Pressing right_ctrl notes your mouse position, which should be on the text box you want the password to go into.
# it then selects the right side of your screen, where I have xed open. Garbage is typed here at random intervals. Type your password into the garbage, and press right_ctrl when you are done.
# the program remembers what it has typed, and tracks what is typed overall. By finding the differences between what it typed and what was typed in aggregate, it can figure out what you typed
# it then types what you typed to the textbox you selected at the beginning, alternating between typing your character and 2-8 characters in the right side garbage window.

# note to the wise:
"""
PyAutoGUI has a built in failsafe to terminate the program at any time. 
Just move your mouse to the top left corner of your main monitor where your x, y values 
would be 0, 0.
"""
# I originally used pyautogui to type, but there is a stupid bug where it types < when given >. Known issue! https://github.com/asweigart/pyautogui/issues/749
generated = []
typed = []
toType = []
# initialize to 1 and not 0 because 0, 0 will cause pyAutoGUI to fail
x = 1
y = 1
k = Controller()


def main():
    global typed
    global generated
    global toType
    global x
    global y
    global k

    # alt tab into the text editor (open the text editor and minimize it before running the program)
    k.press(Key.alt)
    k.press(Key.tab)
    k.release(Key.tab)
    k.release(Key.alt)

    # loops inspired by https://www.reddit.com/r/learnpython/comments/8y0p3j/how_do_i_stop_for_loop_with_keyboard_listener/
    # possible improvement could be a "non blocking statement": https://stackoverflow.com/questions/59208869/python-multithreading-with-pynput-keyboard-listener
    with keyboard.Listener(on_press=on_press_start) as l:
        l.join()

    # place your mouse on the box you want to type in
    x, y = pyautogui.position()
    # move the cursor to the right window, where there ix xed
    pyautogui.moveTo(1000, 200)
    pyautogui.click()

    with keyboard.Listener(on_press=on_press_stop) as listener:
        while listener.running:
            typeRandomChar()
            # replace keyboard.space thing with the ' ' character
            try:
                typed[typed.index(keyboard.Key.space)] = ' '
            except ValueError:
                # idk do nothing, python index throws an error if it doesn't exist
                pass

    compareGeneratedToTyped()
    # at the end, type the text we need to type
    typeToType()


def compareGeneratedToTyped():
    global typed
    global generated
    global toType

    # strange bug where the first character generated is in generated but not typed, throws everything off
    if generated[0] != typed[0]:
        typed.insert(0, f"{generated[0]}")

    # python does not have for loops with multiple conditions. The loop runs until it hits the length of generated or it finds a mismatch between generated and typed
    for i in range(0, len(generated)):
        if str(generated[i]) != typed[i]:
            toType.append(typed[i])
            typed.pop(i)
        if len(typed) < len(generated):
            raise Exception("Something has gone horribly wrong. Typed is smaller than generated")


def typeToType():
    global toType
    for i in range(0, len(toType)):
        # move the cursor to the left window, where there ix the text box we want to input into
        pyautogui.moveTo(x, y)
        pyautogui.click()
        # clicking could be anywhere in the line, we only want to type at the end
        # typing space doesn't seem to work unless I do ctrl + end
        k.press(Key.ctrl)
        k.press(Key.end)
        k.release(Key.end)
        k.release(Key.ctrl)

        toWrite = str(toType[i])

        if toWrite == 'backspace':
            k.press(Key.backspace)
            k.release(Key.backspace)
        elif toWrite == ' ':
            k.press(Key.space)
            k.release(Key.space)
        else:
            k.type(toWrite)

        # type 2-8 random characters after your letter
        # move the cursor to the right window, where there ix xed
        pyautogui.moveTo(1000, 200)
        pyautogui.click()

        for j in range(0, random.randint(2, 8)):
            typeRandomChar()


def on_press_start(key):
    if key == keyboard.Key.ctrl_r:
        return False


def on_press_stop(key):
    global typed
    if key == keyboard.Key.ctrl_r:
        return False
    if key == keyboard.Key.shift:
        return
    if key == keyboard.Key.space:
        typed.append(' ')
        return

    key = key.char
    if key == 'Key.backspace':
        key = 'backspace'

    typed.append(key)


def typeRandomChar():
    global generated
    global k
    # a = none uses the system time as the seed. Version 2 is the more modern version and converts everything to an int and uses all 4 bytes
    random.seed(a=None, version=2)

    # the number of random characters to write, 1 to 2
    # I tried random.randint(1, 5) initially, but it is too many I think. Just do 1
    # numChars =
    # for x in range(0, numChars):

    # write a random ascii value to the screen between 32, 127 inclusive
    # 32 is a space, before it are the control characters, 127 is delete
    # there is a ridiculous bug where generated records < but typed records >, it makes no sense! Hopefully casting to a string will fix that...
    # also is a bug where ' is recorded as \', but only ' is typed to the screen
    c = chr(random.randint(32, 126))
    generated.append(c)
    # don't ask questions, I swear if I do pyautogui.write(c) it occasionally writes a different character than c
    # so I just write the last character of generated instead
    k.type(generated[len(generated)-1])
    # pynput does not have a delay by default like pyauogui does
    time.sleep(random.uniform(0, 0.1))


if __name__ == '__main__':
    main()
