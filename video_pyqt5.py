# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2


#Maikol Rodriguez
#Yorge Arteaga

#Importamos todas las librerias de Inteligencia Artificial
from imutils import face_utils
from utils import *
import numpy as np
import pyautogui as pag
import imutils
import dlib
from tkinter import*

from PIL import Image, ImageTk
import mediapipe as mp

import tensorflow as tf

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setMinimumSize(QtCore.QSize(900, 700))
        MainWindow.setMaximumSize(QtCore.QSize(900, 700))
        MainWindow.setStyleSheet("QWidget#centralwidget{background-color: rgb(85, 170, 127);}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 70, 320, 240))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 340, 231, 41))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(232, 58, 58);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 340, 231, 41))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(85, 255, 127);\n"
"\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 420, 91, 20))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("border-radius:5px;\n"
"background-color: rgb(85, 170, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 341, 31))
        self.label_2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.cancel)
        self.pushButton_2.clicked.connect(self.start_video)
        self.pushButton_3.clicked.connect(self.salir)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_video(self):
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.label.clear()
        self.Work.stop()

    def salir(self):
        sys.exit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Stop"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton_3.setText(_translate("MainWindow", "Exit"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Video stream con PyQt5 y Python</p></body></html>"))

class Work(QThread):
    Imageupd = pyqtSignal(QImage)
    def run(self):
        self.hilo_corriendo = True
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.hilo_corriendo:
            ret, frame = cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(Image, 1)
                gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY) #Bien
               
                
                
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
                cv2.drawContours(Image, [mouthHull], -1, YELLOW_COLOR, 1)
                cv2.drawContours(Image, [leftEyeHull], -1, YELLOW_COLOR, 1)
                cv2.drawContours(Image, [rightEyeHull], -1, YELLOW_COLOR, 1)

                for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
                    cv2.circle(Image, (x, y), 2, GREEN_COLOR, -1)

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
                    cv2.putText(Image, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
                    x, y = ANCHOR_POINT
                    nx, ny = nose_point
                    w, h = 60, 35
                    multiple = 1
                    #print(x, y, w, h)
                    cv2.rectangle(Image, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
                    cv2.line(Image, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)
                    
                    dir = direction(nose_point, ANCHOR_POINT, w, h)
                    cv2.putText(Image, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

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
                    cv2.putText(Image, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                pic = convertir_QT.scaled(320, 240, Qt.KeepAspectRatio)
                self.Imageupd.emit(pic)
            else:
                cap.release()
    def stop(self):
        self.hilo_corriendo = False
        self.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
