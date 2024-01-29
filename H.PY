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



def iniciarP():
    global vid, shape_predictor, detector, predictor
    
    shape_predictor = "shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)
    vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    
    
    visualizar()


def finalizarP():
    global vid
    # Haz un poco de limpieza
    vid.release()
    cv2.destroyAllWindows()


def visualizar():
    global vid ,framee, ret, shape_predictor, detector, predictor

    if vid is not None:
        
        ret, framee = vid.read()
        
        
        if ret == True:
            framee = cv2.flip(framee, 1)
            framee = imutils.resize(framee, width=640, height=480)
            #framee = cv2.cvtColor(framee, cv2.COLOR_BGR2RGB) 

            'Yorge'
            wW = 2120 
            hH = 1180 

            frame_rgb= cv2.cvtColor(framee, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)
            '----'

            '//////////////////////////////////'
            '//////////////////////////////////'
            mp_face_mesh= mp.solutions.face_mesh
            mp_drawing=mp.solutions.drawing_utils
            


            
            'YORGE'
            with mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5) as face_mesh:
            #------------------------
                        
                if results.multi_face_landmarks is not None:
                    for face_landmarks in results.multi_face_landmarks:
                        xX = int(face_landmarks.landmark[4].x * wW *1.11)
                        yY = int(face_landmarks.landmark[4].y * hH *1.11)
                        #cv2.circle(vid, (x, y), 2, (255,0,255), 2)
                                
                        mp_drawing.draw_landmarks(framee, face_landmarks,
                            mp_face_mesh.FACE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                            mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                                
                        pag.moveTo(xX,yY)
                        print(str(xX), ' ', str(yY))



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


pantalla.mainloop()