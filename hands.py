import cv2
import mediapipe as mp
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
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        cordarr=[]
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
    
    cv2.putText(img, 'FPS: '+str(int(fps)), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (94.1,12.5,62.7), 2)

    if cordarr != []:
        print(cordarr[8][0])#x val
        print(cordarr[8][1])#y val
    
    #finals
    cv2.imshow("Hand Tracker", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break