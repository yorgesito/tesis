import cv2
import numpy as np
import mediapipe as mp
#import SeguimientoManos as sm  #Programa que contiene la deteccion y seguimiento de manos
import pyautogui  #Libreria que nos va a permitir manipular el mouse
import time
#---------------------------------Declaracion de variables---------------------------------------
mp_drawing= mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
#----------------------------------- Lectura de la camara----------------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


pTime= 0

color_mouse_point = (255,0,255)
wScr, hScr = pyautogui.size()
camW = 640
camH = 480
frameR= 150
suave=10

plocX,plocY= 0,0
clocX,clocy= 0,0

cap.set(3, camW)
cap.set(4, camH)
pyautogui.FAILSAFE = False

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
    
    while True:
        #----------------- Vamos a encontrar los puntos de la mano -----------------------------
        ret, frame = cap.read()
        if ret == False:
            break

        frame = cv2.cvtColor(frame, 1)
        #frame = cv2.flip(frame, 1)
        frame_rgb = cv2. cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        cv2.rectangle(frame, (frameR, frameR),(camW-frameR, camH-frameR), (255,0,255),2 )

        if results.multi_hand_landmarks is not None:
            for hands_landmarks in results.multi_hand_landmarks:
                x = int(hands_landmarks.landmark[8].x * camW)
                y = int(hands_landmarks.landmark[8].y * camH)
                #print(str(x), ' ',str(y))
                
                #cv2.circle(frame, (x,y), 10, color_mouse_point, 3 )

                #MovinMOde
                x3 = np.interp(x, (frameR,camW-frameR), (0,wScr))
                y3 = np.interp(y, (frameR,camH-frameR), (0, hScr))
                clocX = plocX + (x3 - plocX)/ suave
                clocY = plocY + (y3 - plocY)/ suave
                
                pyautogui.moveTo(int(wScr-x3),int(y3))
                print(wScr-x3, ' ' ,y3)
                cv2.circle(frame, (x,y), 10, color_mouse_point, 3 ,cv2.FILLED)
                plocX, plocY = clocX, clocY
        k = cv2.waitKey(1)
        if k == 27:
            break
        cTime= time.time()
        fps= 1/(cTime-pTime)
        pTime= cTime
        cv2.putText(frame, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN,3, (255,0,0), 3)
        cv2.imshow("Mouse", frame)
    

    cap.release()
    cv2.destroyAllWindows()
