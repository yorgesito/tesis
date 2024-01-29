from tkinter import *
import mouse_curso_control

principal = mouse_curso_control


#Crea la ventana principal para añadir los Widgets
#ventana = Tk()
'Tk()'
raiz= Tk()


raiz.title("Face Pointer")
raiz.geometry('800x480')

#Bloque de Texto
'Label(maestro, text='')'
lbl = Label(raiz, text="Hellouda")
'Pack ubica los WIDGETS o los llama a la'
'interfaz'
lbl.pack()

def miFuncion():
    principal.main


cuadro = Frame(raiz, width=700,height=300, bg='#FFFFCD')
cuadro.place(x=450, y=200)

'command=Accion()'
btn = Button(raiz, text='Boton', command=miFuncion)
btn.pack()
 
raiz.mainloop()