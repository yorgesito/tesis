#------------------------------ Importamos las librerias ----------------------------------------
import cv2
import math
import mediapipe as mp
import numpy as np
import time

#import autopy  #Libreria que nos va a permitir manipular el mouse
class detectormanos():

    def __init__(self, mode=False, maxManos=2, Confdeteccion=0.5, Consegui=0.5):
        self.mode=mode
        self.maxManos=maxManos
        self.Confdeteccion = Confdeteccion
        self.Consegui= Consegui

        self.mpmanos= mp.solutions.hands
        self.manos=  self.mpmanos.Hands(self.mode, self.maxManos, self.Confdeteccion, self.Consegui)
        self.dibujo = mp.solutions.mp_drawing_utils
        self.tip= [4,8,12,16,20]

    def encontrarmanos(self,frame, dibujar=True):
        imgColor= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados= self.manos.process(imgColor)

        if resultados.multi_hand_landmarks:
            for mano in resultados.multi_hand_landmarks:
                if dibujar:
                    self.maxManosdibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)
            return frame

    def encontrarposicion(self,frame, ManoNum=0, dibujar=True):
        xLista=[]
        yLista=[]
        bbox= []
        self.lista= []
        if self.resultados.multi_hand_landmarks:
            miMano= self.resultados.multi_hand_landmarks[ManoNum]
            for id, lm in enumerate(miMano.landmark):
                alto, ancho, c = frame.shape
                cx, cy = int(lm.x * ancho), int(lm.y * alto)
                xLista.append(cx)
                yLista.append(cy)
                self.lista.append([id, cx, cy])
                if dibujar:
                    cv2.circle(frame (cx, cy), 5, (0,0,0), cv2.FILLED)
            
            xmin, xmax = min(xLista), max(xLista)
            ymin, ymax = min(yLista), max(yLista)
            bbox = xmin, ymin, xmax, ymax
            if dibujar:
                cv2.rectangle(frame, (xmin-20, ymin-20), (xmax+20, ymax+20), (0,255,0), 2)
        return self.lista, bbox

    def dedosArriba(self):
        dedos = []
        if self.lista[self.tip[0]][1]> self.lista[self.tip[0]-1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range(1, 5):
            if self.lista[self.tip[id]][2]> self.lista[self.tip[id]-2][2]:
                dedos.append(1)
            else:
                dedos(0)
        return dedos

    def distancia(self,p1,p2,frame,dibujar=True, r=15, t=3):
        x1, y1 = self.lista[p1][1:]
        x2, y2 = self.lista[p2][1:]
        cx, cy = (x1+x2)//2,(y1+y2)//2
        if dibujar:
            cv2.line(frame, (x1,x2), (x2,y2), (0,0,255),t)
            cv2.circle(frame, (x1,y1), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (x2,y2), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (cx,cy), r, (0,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]
    
def main():
    pTiempo=0
    cTiempo=0

    cap = cv2.VideoCapture(0)

    detector= detectormanos()

    while True:
        #----------------- Vamos a encontrar los puntos de la mano -----------------------------
        ret, frame = cap.read()
        frame = detector.encontrarmanos(frame)  #Encontramos las manos
        lista, bbox = detector.encontrarposicion(frame) #Mostramos las posiciones

        #-----------------Obtener la punta del dedo indice y corazon----------------------------
        if len(lista) != 0:
            #x1, y1 = lista[8][1:]                  #Extraemos las coordenadas del dedo indice
            #x2, y2 = lista[12][1:]                 #Extraemos las coordenadas del dedo corazon
            print(lista[4])

            cTiempo = time.time()
            fps = 1/(cTiempo-pTiempo)
            pTiempo = cTiempo
            #----------------- Comprobar que dedos estan arriba --------------------------------
            dedos = detector.dedosarriba() #Contamos con 5 posiciones nos indica si levanta cualquier dedo
            #print(dedos)
            cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)  # Generamos cuadro
            cv2.imshow('Manos', frame)
            k= cv2.waitKey(1)

            if k==27:
                break
          
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()