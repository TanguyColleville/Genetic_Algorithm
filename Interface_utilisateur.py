from tkinter import *
from tkinter.filedialog import * ## pour l'explorateur de fichier
import tkinter.ttk as ttk
from PIL import Image,ImageTk
import os 

main = Tk()###création d'une fenêtre vide qui s'appelle main 
main.title("Algorithme génétique")### titre de la fenêtre
ch=r"‪C:/Users/Tanguy/Desktop/logo_ei.PNG"
ch=r"D:\AM 1A\Informatique\Projet POO\Programme\logo_ei.PNG"
render = ImageTk.PhotoImage(Image.open(os.path.join(ch)))
Label(image=render).grid(sticky="n")


nombre_generation=StringVar()

Label(main, text= "Nombre de génération").grid(row = 1, column = 0)
Entry(main,textvariable=nombre_generation).grid(row=1,column=1)

 
filename = StringVar()
Label(main,text="Clic on Open to select a file").grid(row=2,column=0)
Entry(main, textvariable=filename,state='disabled').grid(row=2,column=1)
Button(main,text='Open',command=lambda:filename.set(askopenfilename())).grid(row=2,column=2)

Methode= StringVar(main)
Label(main, text= "Selection de la méthode").grid(row = 4, column = 0)
ttk.Combobox(main,values=["Tournois","Elitisme"],textvariable=Methode).grid(row=4,column=1)

######Attention ici changer Command None en lancement des claculs de main.py 
Button(main,text="Lancer les calculs",command=None).grid(row=5, column= 1)

Button(main,text="Tracer la trajectoire 3D de la molécule initiale",command=None).grid(row=6,column=0)


Button(main,text="Quitter",command=main.destroy).grid(row=6, column= 2)###création d'un boutton qui entraine la destruction (fermerture) de l'interface
main.mainloop()

generation_max=int(nombre_generation.get())
chemin=filename.get()
meth=str(Methode.get())
