import cv2
import mediapipe as mp
from math import sqrt
import time
import os
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
cordarr=[]

def distance(finger1x, finger1y, finger2x, finger2y):
    xnumbers = (finger2x - finger1x)**2
    ynumbers = (finger2y - finger1y)**2
    numbers = xnumbers + ynumbers
    return sqrt(numbers)
    

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    cordarr=[]
    if results.multi_hand_landmarks:
        os.system('cls')
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                cordarr.append([cx,cy])
                #if id == 8: #pointer detection, useless but cool
                #    cv2.circle(img, (cx, cy), 15, (139, 0, ), cv2.FILLED)
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
#fps calcs
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, 'FPS: '+str(int(fps)), (0,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (94.1,12.5,62.7), 2)

    hand1=[]
    hand2=[]
    for x in range(0,len(cordarr)):
        if x < 22:
            hand1.append([cordarr[x][0],cordarr[x][1]])
        else:
            hand2.append([cordarr[x][0],cordarr[x][1]])

    if cordarr != [] and len(cordarr) < 22:
        # cv2.putText(img, "Index", (cordarr[8][0], cordarr[8][1]), cv2.FONT_HERSHEY_SIMPLEX, .6, (94.1,12.5,62.7), 2)
        if distance(cordarr[8][0], cordarr[8][1], cordarr[12][0], cordarr[12][1]) > 160 and distance(cordarr[1][0], cordarr[1][1], cordarr[12][0], cordarr[12][1]) < 65:
            cv2.putText(img, "Pointing", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (94.1,12.5,62.7), 2)
            print("POINTING")
        elif distance(cordarr[8][0], cordarr[8][1], cordarr[4][0], cordarr[4][1]) < 30 and distance(cordarr[8][0], cordarr[8][1], cordarr[12][0], cordarr[12][1]) > 50:
            cv2.putText(img, "OK", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (94.1,12.5,62.7), 2)
    
    #finals
    cv2.imshow("Hand Tracker", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
