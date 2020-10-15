import pyautogui
import pyperclip

# print('test')
# pos = pyautogui.position()  # current mouse x and y
# print(pos)
# size = pyautogui.size()  # current screen resolution width and height
# print(size)
#pyautogui.PAUSE = 2.5  # Set up a 2.5 second pause after each PyAutoGUI call
# pyautogui.sleep(2)
# check = pyautogui.onScreen(20, 3000)  # True if x & y are within the screen.
# print(check)

# pyautogui.moveTo(10, 300, duration=1)  # move mouse to XY coordinates over num_second seconds
# pyautogui.moveRel(10, 300, duration=1)  # move mouse relative to its current position
# pyautogui.dragTo(100, 300, duration=1)  # drag mouse to XY
# pyautogui.dragRel(100, 300, duration=0.1)  # drag mouse relative to its current position
# pyautogui.click(x=100, y=300, clicks=1, interval=1, button='left')  # The button keyword argument can be 'left', 'middle', or 'right'.

# pyautogui.typewrite('Hello world!\n', interval=0.1)  # useful for entering text, newline is Enter
# pyautogui.typewrite(['a', 'b', 'c', 'left', 'backspace', 'enter', 'f1'], interval=1)
# pyautogui.alert('This displays some text with an OK button.')
# pyautogui.confirm('This displays text and has an OK and Cancel button.')
# pyautogui.prompt('This lets the user type in a string and press OK.')

# pyautogui.screenshot('foo.png')  # returns a Pillow/PIL Image object, and saves it to a file
# loc = pyautogui.locateOnScreen('loc.png')  # returns (left, top, width, height) of first place it is found
# print(loc)
# loc = pyautogui.locateCenterOnScreen('loc.png')  # returns center x and y
# print(loc)
# pyautogui.leftClick(loc)

# show desktop
# loc = pyautogui.locateCenterOnScreen('./pyautoPics/showDesktop.png')  # returns center x and y
# pyautogui.leftClick(loc)
# pyautogui.sleep(0.2)

# run mofidtrader
# loc = pyautogui.locateCenterOnScreen('./pyautoPics/mofidapp.png')  # returns center x and y
# pyautogui.doubleClick(loc)
# if loc is None:
#     pyautogui.alert('can not find mofidtrader icon')

# pyautogui.sleep(3)

# find symbol tab
loc = pyautogui.locateCenterOnScreen('./pyautoPics/symbolsTab.png')  # returns center x and y
print(loc)
if loc is not None:
    print("finded tab")
    pyautogui.click(loc)
    pyautogui.move(0, -50)
    pyautogui.click()
    pyautogui.hotkey("end")

loc = pyautogui.locateCenterOnScreen('./pyautoPics/addSymbol.png')  # returns center x and y
#
if loc is not None:
    pyautogui.doubleClick(loc)
    pyperclip.copy("دلر")
    pyautogui.sleep(0.5)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.sleep(0.5)
    pyautogui.hotkey("enter")
else:
    print("can not locate add symbol")

# pyautogui.rightClick()