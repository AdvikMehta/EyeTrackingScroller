import pyautogui
import cv2
import time
from gaze_tracking import GazeTracking

pyautogui.FAILSAFE = True
gaze = GazeTracking()
webcam = cv2.VideoCapture(1)
scrollActive = False
blinkTime = time.time()
blinkInterval = 0
blinksInRow = 0

while True:
    # get a new frame from the webcam
    _, frame = webcam.read()
    # send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        blinkInterval = time.time() - blinkTime
        if blinkInterval < 1:
            blinksInRow += 1
        blinkTime = time.time()

    if time.time() - blinkTime > 3:
        blinksInRow = 0
    if blinksInRow >= 5:
        blinksInRow = 0
        scrollActive = not scrollActive

    if gaze.vertical_ratio() and scrollActive:
        if gaze.vertical_ratio() > 0.73:  # looking down
            text = "Looking down"
            pyautogui.scroll(10)
        else:  # looking up
            text = "Looking Up"
            pyautogui.scroll(-10)

    softActive = "Software Active" if scrollActive else "Software Inactive"

    cv2.putText(frame, softActive, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.putText(frame, text, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    cv2.imshow("Blink n Scroll", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
