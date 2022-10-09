import cv2
import mediapipe as mp
from math import sqrt
import time
import os
import pickle


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
                cv2.putText(img, f"{id}", (cx + 5, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 100),
                            2)  #debug id check
            mpDraw.draw_landmarks(
                img, handlms, mpHands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
#fps calcs

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, 'FPS: ' + str(int(fps)), (0, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (94.1, 12.5, 62.7), 2)


    if cordarr != [] and len(cordarr) < 22:
        baseline = {
            "thumb":distance(4,0),
            "pointer":distance(8,0),
            "middle":distance(12,0),
            "ring":distance(16,0),
            "pinkie":distance(20,0)
        }
    
    #finals
    cv2.imshow("Hand Tracker", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        with open('pickle.pk','wb') as file:
            pickle.dump(baseline,file)
        break
