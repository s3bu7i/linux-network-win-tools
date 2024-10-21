
import pyautogui as pt
import time
limit = int(input("Say: "))
message = input("message: ")
time.sleep(5)

i = 0

while i < limit:
    pt.write(message)
    pt.press("enter")
    i = i + 1
    print(i)

    time.sleep(0.1)
