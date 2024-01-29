#Maikol Rodriguez
#Yorge Arteaga

#Importamos todas las librerias de Inteligencia Artificial
from imutils import face_utils
from utils import *
import numpy as np
import pyautogui as pag
import imutils
import dlib
import cv2
from tkinter import*

from PIL import Image, ImageTk
import mediapipe as mp

import tensorflow as tf

#tf.config.set_visible_devices([], 'GPU')

#tf.debugging.set_log_device_placement(True)

print(tf.config.list_physical_devices())
print(tf.test.is_gpu_available())
# Place tensors on the CPU

'''Software 2.0 - Mover todos lados'''
import time
pag.FAILSAFE = False #Esto quita el error del Mouse cuando sale de la pantalla

suave=5 #Esto es una suavizante a la hora de mover el Mouse
color_mouse_point = (255,0,255) #Color del Puntero del Mouse
wScr, hScr = pag.size() #Este metodo obtiene el tamaño de la pantalla de la Computadora
camW = 640 #Ancho de la WebCam
camH = 480 #Alto de la WebCam
frameR= 150 #Tamaño del Cuadro, mientras mas grande el numero, mas se reduce el cuadro
'''--------------------------------'''


with tf.device('/CPU:0'):
    #shape_predictor = "shape_predictor_68_face_landmarks.dat"
    #detector = dlib.get_frontal_face_detector()
    #predictor = dlib.shape_predictor(shape_predictor)
    
    def iniciarP():
        global vid, shape_predictor, detector, predictor
        
        vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    
       
        visualizar()


    def finalizarP():
        global vid
        # Haz un poco de limpieza
        vid.release()
        cv2.destroyAllWindows()


    def visualizar():
        global vid ,framee, ret, shape_predictor, detector, predictor, rect

        if vid is not None:
            
            ret, framee = vid.read()  
            pTime= 0          
            if ret == True:
                #framee = cv2.flip(framee, 1)
                #framee = imutils.resize(framee, width=640, height=480)
                #framee = cv2.cvtColor(framee, cv2.COLOR_BGR2RGB) 

            

                '//////////////////////////////////'
                '//////////////////////////////////'
                mp_face_mesh= mp.solutions.face_mesh
                mp_drawing=mp.solutions.drawing_utils
                

                # Umbrales y longitud de fotograma consecutivo para activar la acción del mouse.
                MOUTH_AR_THRESH = 0.6
                MOUTH_AR_CONSECUTIVE_FRAMES = 15
                EYE_AR_THRESH = 0.19
                EYE_AR_CONSECUTIVE_FRAMES = 15
                WINK_AR_DIFF_THRESH = 0.04
                WINK_AR_CLOSE_THRESH = 0.8
                WINK_CONSECUTIVE_FRAMES = 10

                # Inicialice los contadores de fotogramas para cada acción, así como
                # booleanos utilizados para indicar si la acción se realiza o no
                MOUTH_COUNTER = 0
                EYE_COUNTER = 0
                WINK_COUNTER = 0
                INPUT_MODE = False
                EYE_CLICK = False
                LEFT_WINK = False
                RIGHT_WINK = False
                SCROLL_MODE = False
                ANCHOR_POINT = (0, 0)
                WHITE_COLOR = (255, 255, 255)
                YELLOW_COLOR = (0, 255, 255)
                RED_COLOR = (0, 0, 255)
                GREEN_COLOR = (0, 255, 0)
                BLUE_COLOR = (255, 0, 0)
                BLACK_COLOR = (0, 0, 0)
                # Inicialice el detector de rostros de Dlib (basado en HOG) y luego cree
                # el predictor de puntos de referencia facial
                
                shape_predictor = "shape_predictor_68_face_landmarks.dat"
                detector = dlib.get_frontal_face_detector()
                predictor = dlib.shape_predictor(shape_predictor)

                # Tome los índices de los puntos de referencia faciales para la izquierda y
                # ojo derecho, nariz y boca respectivamente
                (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
                (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
                (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
                (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

                '''Software 2.0 - Mover todos lados'''
                plocX,plocY= 0,0 #Ancho de la WebCam
                clocX,clocy= 0,0 #Ancho de la WebCam

                vid.set(3, camW) #Insertar Ancho del la WebCam
                vid.set(4, camH) #Insertar Alto de la WebCam
                '''---------------------------------'''
                       
                _, frame = vid.read() #Bien
                #frame = cv2.flip(frame, 1) #Bien
                #frame = imutils.resize(frame, width=cam_w, height=cam_h)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Bien
                    

                frame_rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #results = face_mesh.process(frame_rgb)
                '----'
                    
                # Detectar rostros en el marco de escala de grises
                rects = detector(gray, 0)
                # Recorre las detecciones de rostros
                if len(rects) > 0:
                    rect = rects[0]
                    #print(rect)
                #else:
                    #cv2.imshow("LOCO", framee)
                    #key = cv2.waitKey(1) & 0xFF
                    #continue

                # Determine los puntos de referencia faciales para la región de la cara, luego
                # convertir las coordenadas del punto de referencia facial (x, y) a NumPy
                # matriz

                #print(rect)
                    
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # Extraiga las coordenadas del ojo izquierdo y derecho, luego use el
                # coordenadas para calcular la relación de aspecto de ambos ojos
                mouth = shape[mStart:mEnd]
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                nose = shape[nStart:nEnd]

                # Debido a que volteé el marco, la izquierda es la derecha y la derecha es la izquierda.
                temp = leftEye
                leftEye = rightEye
                rightEye = temp

                # Average the mouth aspect ratio together for both eyes
                mar = mouth_aspect_ratio(mouth)
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                diff_ear = np.abs(leftEAR - rightEAR)

                nose_point = (nose[3, 0], nose[3, 1])


                # Calcule el casco convexo para el ojo izquierdo y derecho, luego
                # visualizar cada uno de los ojos
                mouthHull = cv2.convexHull(mouth)
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
                cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
                cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)

                for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
                    cv2.circle(frame, (x, y), 2, GREEN_COLOR, -1)

                '''Software 2.0 - Mover todos lados'''
                #Dibujar El RECTANGULO en la WebCam
                cv2.rectangle(frame, (frameR, frameR),(camW-frameR, camH-frameR), (255,0,255),2 ) 
                '''-----------------------------------'''

                #if results.multi_face_landmarks is not None:    
                '''Software 2.0 - Mover todos lados'''

                for rect in rects:
                        
                    shapee= predictor(gray, rect) #Lee los puntos del Rostro
                    x1=shapee.part(33).x #Obtienes Coordenada en X 
                    y1=shapee.part(33).y #Obtienes Coordenada en Y
                    #print(x1,' ', y1)

                        #x = int(x1 * camW)
                        #y = int(y1 * camH)
                        #print(str(x), ' ',str(y))
                            
                        #cv2.circle(frame, (x,y), 10, color_mouse_point, 3 )  
                        #cv2.putText=(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        #            (255,0,0), 3 )
                                
                        #Conversor de Coordenadas del Rectangulo a la Pantalla de la Computadora
                    x3 = np.interp(x1, (frameR,camW-frameR), (0,wScr))
                    y3 = np.interp(y1, (frameR,camH-frameR), (0,hScr))
                    clocX = plocX + (x3 - plocX)/ suave
                    clocY = plocY + (y3 - plocY)/ suave
                                
                    pag.moveTo(int(wScr-x3),int(y3)) #Mover el Mouse
                    #print(int(wScr-x3), ' ' ,int(y3))

                    cv2.circle(frame, (x1,y1), 10, color_mouse_point, 3 ,cv2.FILLED) #Dibujar Punto Rosado del Mouse en la Nariz
                    plocX, plocY = clocX, clocY
                    '''-----------------------------------'''   

                # Verifique si la relación de aspecto del ojo está por debajo del parpadeo
                    # umbral y, de ser así, incrementar el contador de fotogramas de parpadeo.
                if diff_ear > WINK_AR_DIFF_THRESH:
                    if leftEAR < rightEAR:
                        if leftEAR < EYE_AR_THRESH:
                            WINK_COUNTER += 1

                            if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                                pag.click(button='left')

                                WINK_COUNTER = 0

                    elif leftEAR > rightEAR:
                        if rightEAR < EYE_AR_THRESH:
                            WINK_COUNTER += 1

                            if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                                pag.click(button='right')

                                WINK_COUNTER = 0
                    else:
                        WINK_COUNTER = 0
                    
                else:
                    if ear <= EYE_AR_THRESH:
                        EYE_COUNTER += 1

                        if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
                            SCROLL_MODE = not SCROLL_MODE
                            # INPUT_MODE = not INPUT_MODE
                            EYE_COUNTER = 0

                            # punto de la nariz para dibujar un cuadro delimitador a su alrededor
                    else:
                        EYE_COUNTER = 0
                        WINK_COUNTER = 0
                if mar > MOUTH_AR_THRESH:
                    MOUTH_COUNTER += 1

                    if MOUTH_COUNTER >= MOUTH_AR_CONSECUTIVE_FRAMES:
                        # si la alarma no está encendida, enciéndela
                        INPUT_MODE = not INPUT_MODE
                        # SCROLL_MODE = not SCROLL_MODE
                        MOUTH_COUNTER = 0
                        ANCHOR_POINT = nose_point
                else:
                    MOUTH_COUNTER = 0


                if INPUT_MODE:
                    cv2.putText(frame, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
                    #x, y = ANCHOR_POINT
                    #nx, ny = nose_point
                    #w, h = 60, 35
                    #multiple = 1
                    #print(x, y, w, h)
                    #cv2.rectangle(framee, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
                    #cv2.line(framee, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)
                    
                    #dir = direction(nose_point, ANCHOR_POINT, w, h)
                    #cv2.putText(framee, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
                    '''Software 2.0 - Mover todos lados'''
                    #Dibujar El RECTANGULO en la WebCam
                    cv2.rectangle(frame, (frameR, frameR),(camW-frameR, camH-frameR), (255,0,255),2 ) 
                    '''-----------------------------------'''

                    #if results.multi_face_landmarks is not None:    
                    '''Software 2.0 - Mover todos lados'''

                    for rect in rects:
                        
                        shapee= predictor(gray, rect) #Lee los puntos del Rostro
                        x1=shapee.part(33).x #Obtienes Coordenada en X 
                        y1=shapee.part(33).y #Obtienes Coordenada en Y
                        #print(x1,' ', y1)

                        #x = int(x1 * camW)
                        #y = int(y1 * camH)
                        #print(str(x), ' ',str(y))
                            
                        #cv2.circle(frame, (x,y), 10, color_mouse_point, 3 )  
                        #cv2.putText=(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        #            (255,0,0), 3 )
                                
                        #Conversor de Coordenadas del Rectangulo a la Pantalla de la Computadora
                        x3 = np.interp(x1, (frameR,camW-frameR), (0,wScr))
                        y3 = np.interp(y1, (frameR,camH-frameR), (0,hScr))
                        clocX = plocX + (x3 - plocX)/ suave
                        clocY = plocY + (y3 - plocY)/ suave
                                
                        pag.moveTo(int(wScr-x3),int(y3)) #Mover el Mouse
                        #print(int(wScr-x3), ' ' ,int(y3))

                        cv2.circle(frame, (x1,y1), 10, color_mouse_point, 3 ,cv2.FILLED) #Dibujar Punto Rosado del Mouse en la Nariz
                        plocX, plocY = clocX, clocY
                    '''-----------------------------------'''   
                    
                    

                    '''
                    drag = 18
                    if dir == 'right':
                        pag.moveRel(drag, 0)
                    elif dir == 'left':
                        pag.moveRel(-drag, 0)
                    elif dir == 'up':
                        if SCROLL_MODE:
                            pag.scroll(40)
                        else:
                            pag.moveRel(0, -drag)
                    elif dir == 'down':
                        if SCROLL_MODE:
                            pag.scroll(-40)
                        else:
                            pag.moveRel(0, drag)  
                    '''

                if SCROLL_MODE:
                    cv2.putText(framee, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
                
                '''Software 2.0 - Mover todos lados'''
                #Todo esto es para los FPS
                cTime= time.time()
                fps= 1/(cTime-pTime)
                pTime= cTime
                cv2.putText(frame, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN,3, (255,0,0), 3)
                '''-----------------------------------'''

                framee = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                im = Image.fromarray(framee)
                img = ImageTk.PhotoImage(image=im)

                # Mostramos en el GUI
                lblVideo.configure(image=img)
                lblVideo.image = img
                lblVideo.after(10, visualizar) 
            else:
                lblVideo.image = ""
                vid.release()
    vid = None
    #Ventana Principal
    #Pantalla
    pantalla = Tk()
    pantalla.title("FaceMovement")
    pantalla.geometry('1280x720')

    # Fondo
    #imagenF = PhotoImage(file='ujaplogo.png')
    #bg = pantalla.Label(image = imagenF, height="40", width="200",)
    #bg.place(x=5,y=5)
    #grayb = Button(pantalla, text="RGB", image= imagenBG, height="40", width="200", command=grayf)
    #grayb.place(x = 980, y = 250)
    #bg.pack()

  
   # Botones
    btn = Button(pantalla, text="Iniciar Cara", command=iniciarP)
    #btn = Button(pantalla, text="Iniciar")
    btn.config(height=1, width=11)
    btn.config(bg='#D4D4D4')
    btn.place(x=30, y=200)

    btna = Button(pantalla, text="Terminar Cara", command=finalizarP)
    btna.config(height=1, width=13)
    btna.config(bg='#D4D4D4')
    btna.place(x=160, y=200)

    btnM = Button(pantalla, text="Iniciar Manos", command=iniciarP)
    #btn = Button(pantalla, text="Iniciar")
    btnM.config(height=1, width=11)
    btnM.config(bg='#D4D4D4')
    btnM.place(x=30, y=275)

    btnM = Button(pantalla, text="Terminar Manos", command=finalizarP)
    btnM.config(height=1, width=13)
    btnM.config(bg='#D4D4D4')
    btnM.place(x=160, y=275)

    btnM = Button(pantalla, text="Teclado")
    btnM.config(height=1, width=10)
    btnM.config(bg='#D4D4D4')
    btnM.place(x=92, y=340)

    # Video
    lblVideo = Label(pantalla)
    lblVideo.place(x = 320, y = 50)


    pantalla.mainloop()