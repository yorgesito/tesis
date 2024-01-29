#import tensorflow as tf

#tf.config.set_visible_devices([], 'GPU')

#tf.debugging.set_log_device_placement(True)

#print(tf.config.list_physical_devices())
# Place tensors on the CPU
'''
while True:
   with tf.device('/CPU:0'):
    a=1
    b=2
    print(a+b)
'''
'''
while True:
    a=1
    b=2
    print(a+b)
'''

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
#import tensorflow as tf
from PIL import Image, ImageTk
import mediapipe as mp



def iniciarP():
    global vid
    ''' 
    #Yorge
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
    '''

     
    # Video capture
    vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    '''
    resolution_w = 1366
    resolution_h = 768
    cam_w = 640
    cam_h = 480
    unit_w = resolution_w / cam_w
    unit_h = resolution_h / cam_h

    #Yorge
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5) as face_mesh:
    #------------------------

        while True:
            #Tome el fotograma de la secuencia del archivo de vídeo encadenado y cambie el tamaño
            # y convertirlo a escala de grises
            # canales)
            _, frame = vid.read()
            frame = cv2.flip(frame, 1)
            #frame = imutils.resize(frame, width=cam_w, height=cam_h)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            'Yorge'
            wW = 2120 
            hH = 1180 
        
            frame_rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)
            '----'

            # Detectar rostros en el marco de escala de grises
            rects = detector(gray, 0)

            # Recorre las detecciones de rostros
            if len(rects) > 0:
                rect = rects[0]
            else:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                continue

            # Determine los puntos de referencia faciales para la región de la cara, luego
            # convertir las coordenadas del punto de referencia facial (x, y) a NumPy
            # matriz
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
                x, y = ANCHOR_POINT
                nx, ny = nose_point
                w, h = 60, 35
                multiple = 1
                print(x, y, w, h)
                cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
                cv2.line(frame, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)

                
                
                dir = direction(nose_point, ANCHOR_POINT, w, h)
                cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
                
                #YORGE
                
                if results.multi_face_landmarks is not None:
                    for face_landmarks in results.multi_face_landmarks:
                        xX = int(face_landmarks.landmark[4].x * wW *1.11)
                        yY = int(face_landmarks.landmark[4].y * hH *1.11)
                        #cv2.circle(vid, (x, y), 2, (255,0,255), 2)
                        
                        mp_drawing.draw_landmarks(frame, face_landmarks,
                            mp_face_mesh.FACE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                            mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                        
                        pag.moveTo(xX,yY)
                        print(str(xX), ' ', str(yY))
                
                    
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
                
            if SCROLL_MODE:
                cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

            # cv2.putText(frame, "MAR: {:.2f}".format(mar), (500, 30),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
            # cv2.putText(frame, "Right EAR: {:.2f}".format(rightEAR), (460, 80),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
            # cv2.putText(frame, "Left EAR: {:.2f}".format(leftEAR), (460, 130),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
            # cv2.putText(frame, "Diff EAR: {:.2f}".format(np.abs(leftEAR - rightEAR)), (460, 80),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Mostrar el marco
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # Si se presionó la tecla `Esc`, salir del bucle
            if key == 27:
                break
'''
    visualizar()


def finalizarP():
    global vid
    # Haz un poco de limpieza
    vid.release()
    cv2.destroyAllWindows()


def visualizar():
    global vid ,frame, ret
    if vid is not None:

        ret, frame = vid.read()
        if ret == True:
            #frame = imutils.resize(frame, width=640)
            #frame = cv2.flip(frame, 1)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            #im = Image.fromarray(frame)

            #img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            #lblVideo.configure(image=img)
            #lblVideo.image = img
            #lblVideo.after(10, visualizar)

            '//////////////////////////////////'
            'Yorge'
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

            # Video capture
            '//////////////////////////////////'
            resolution_w = 1366
            resolution_h = 768
            cam_w = 640
            cam_h = 480
            unit_w = resolution_w / cam_w
            unit_h = resolution_h / cam_h

            'YORGE'
            with mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5) as face_mesh:
            #------------------------

                while True:
                    #Tome el fotograma de la secuencia del archivo de vídeo encadenado y cambie el tamaño
                    # y convertirlo a escala de grises
                    # canales)
                    
                    _, frame = vid.read() #Bien
                    frame = cv2.flip(frame, 1) #Bien
                    frame = imutils.resize(frame, width=cam_w, height=cam_h)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Bien

                    'Yorge'#--------------------
                    wW = 2120 
                    hH = 1180 
                    #_--------------------------

                    frame_rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(frame_rgb)
                    '----'

                    # Detectar rostros en el marco de escala de grises
                    rects = detector(gray, 0)

                    # Recorre las detecciones de rostros
                    if len(rects) > 0:
                        rect = rects[0]
                    else:
                        cv2.imshow("Frame", frame)
                        key = cv2.waitKey(1) & 0xFF
                        continue

                    # Determine los puntos de referencia faciales para la región de la cara, luego
                    # convertir las coordenadas del punto de referencia facial (x, y) a NumPy
                    # matriz
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
                        x, y = ANCHOR_POINT
                        nx, ny = nose_point
                        w, h = 60, 35
                        multiple = 1
                        #print(x, y, w, h)
                        cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
                        cv2.line(frame, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)

                        
                        
                        dir = direction(nose_point, ANCHOR_POINT, w, h)
                        cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
                        
                        '''YORGE'''
                        '''
                        if results.multi_face_landmarks is not None:
                            for face_landmarks in results.multi_face_landmarks:
                                xX = int(face_landmarks.landmark[4].x * wW *1.11)
                                yY = int(face_landmarks.landmark[4].y * hH *1.11)
                                #cv2.circle(vid, (x, y), 2, (255,0,255), 2)
                                
                                mp_drawing.draw_landmarks(frame, face_landmarks,
                                    mp_face_mesh.FACE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                                
                                pag.moveTo(xX,yY)
                                print(str(xX), ' ', str(yY))
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
                        
                    if SCROLL_MODE:
                        cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

                    # cv2.putText(frame, "MAR: {:.2f}".format(mar), (500, 30),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
                    # cv2.putText(frame, "Right EAR: {:.2f}".format(rightEAR), (460, 80),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
                    # cv2.putText(frame, "Left EAR: {:.2f}".format(leftEAR), (460, 130),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, YELLOW_COLOR, 2)
                    # cv2.putText(frame, "Diff EAR: {:.2f}".format(np.abs(leftEAR - rightEAR)), (460, 80),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # Mostrar el marco
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF

                    # Si se presionó la tecla `Esc`, salir del bucle
                    if key == 27:
                        break
            '//////////////////////////////////'

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
#imagenF = PhotoImage(file='gray.jpg')
#bg = Label(image = imagenF, text='Fondo')
#bg.place(x=0,y=0, relwidth=1,relheight=1)

# Botones
btn = Button(pantalla, text="Iniciar", command=iniciarP)
#btn = Button(pantalla, text="Iniciar")
btn.config(height=2, width=10)
#btn.config(bg='green')
btn.place(x=100, y=250)

btna = Button(pantalla, text="Finalizar", command=finalizarP)
btna.config(height=2, width=10)
#btna.config(bg='red')
btna.place(x=100, y=400)

# Video
lblVideo = Label(pantalla)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(pantalla)
lblVideo2.place(x = 470, y = 500)

pantalla.mainloop()