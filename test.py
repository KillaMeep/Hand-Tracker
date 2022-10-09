import cv2
from os.path import exists
import mediapipe as mp
from math import sqrt
import time
import os
import pickle
from termcolor import colored

os.system('color')
baseline = {}
baseline_raw = []
#import userdata
if exists('pickle.pk'):
    with open('pickle.pk', 'rb') as file:
        baseline = pickle.load(file)
        for x in range(0, len(baseline["raw"])):
            baseline_raw.append(baseline["raw"])
    print(colored("Loaded userdata.", 'green'))

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
cTime = 0
pTime = 0
print('Launching! Press "ESC" to exit.')
#main loop
global cordarr
cordarr = []
winsize=[]

def distance(finger1, finger2):
    finger1x = cordarr[finger1][0]
    finger1y = cordarr[finger1][1]
    finger2x = cordarr[finger2][0]
    finger2y = cordarr[finger2][1]
    xnumbers = (finger2x - finger1x)**2
    ynumbers = (finger2y - finger1y)**2
    numbers = xnumbers + ynumbers
    return sqrt(numbers)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    cordarr = []
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                cordarr.append([cx, cy])
                #if id == 8: #pointer detection, useless but cool
                #    cv2.circle(img, (cx, cy), 15, (139, 0, ), cv2.FILLED)
                cv2.putText(img, f"{id}", (cx + 5, cy), cv2.FONT_HERSHEY_SIMPLEX, .5,(0, 0, 100), 2)  #debug id check
            mpDraw.draw_landmarks(
                img, handlms, mpHands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
#fps calcs

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, 'FPS: ' + str(int(fps)), (0, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (94.1, 12.5, 62.7), 2)
    
    hand1 = []
    hand2 = []
    for x in range(0, len(cordarr)):
        if x < 22:
            hand1.append([cordarr[x][0], cordarr[x][1]])
        else:
            hand2.append([cordarr[x][0], cordarr[x][1]])
    
    if cordarr != [] and len(cordarr) < 22:
        if baseline!={}:
            scalar = abs(int(distance(5, 0) - baseline["pointer_base"]))
            if winsize != []:
                cv2.putText(img, f"Scalar: {scalar}", (winsize[3]-30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,(100, 100, 100), 2)
        else:
            scalar = 0
        # cv2.putText(img, "Index", (cordarr[8][0], cordarr[8][1]), cv2.FONT_HERSHEY_SIMPLEX, .6, (94.1,12.5,62.7), 2)
        if distance(8, 5) < 30 + scalar and distance(12, 9) < 30 + scalar and distance(16, 13) < 30 + scalar and distance(20, 17) < 30 + scalar:
            cv2.putText(img, "Fist", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        elif distance(8, 12) > 160 + scalar and distance(1, 12) < 65 + scalar and distance(4, 5) > 50 + scalar:
            cv2.putText(img, "Pointing", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        elif distance(6, 10) < 40 + scalar and distance(8, 5) < 40 + scalar and distance(9, 10) > 50 + scalar and distance(16, 13) < 50 + scalar:
            cv2.putText(img, "Flip", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        elif distance(8, 4) < 40 + scalar and distance(8, 12) > 50 + scalar and distance(12, 16) < 60 + scalar:
            cv2.putText(img, "OK", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        # Count amount of finger up? Maybe?
        elif distance(8, 12) > 160 + scalar and distance(0, 16) < 65 + scalar and distance(0, 20) < 85 + scalar and distance(1, 12) < 65 + scalar and distance(4, 10) < 40 + scalar:
            cv2.putText(img, "1", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        elif distance(8, 12) < 100 + scalar and distance(0, 16) < 65 + scalar and distance(0, 20) < 85 + scalar and distance(1, 12) > 165 + scalar and distance(4, 14) < 40 + scalar:
            cv2.putText(img, "2", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        elif distance(8, 12) < 100 + scalar and distance(0, 16) > 165 + scalar and distance(0, 20) < 85 + scalar and distance(1, 12) > 165 + scalar and distance(4, 18) < 40 + scalar:
            cv2.putText(img, "3", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
        elif distance(8, 12) < 100 + scalar and distance(0, 16) > 165 + scalar and distance(0, 20) > 165 + scalar and distance(1, 12) > 165 + scalar and distance(4, 13) < 40 + scalar:
            cv2.putText(img, "4", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,(94.1, 12.5, 62.7), 2)
    #finals
    cv2.imshow("Hand Tracker", img)
    winsize = list(cv2.getWindowImageRect('Hand Tracker'))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
      cv2.destroyAllWindows()
      break
            