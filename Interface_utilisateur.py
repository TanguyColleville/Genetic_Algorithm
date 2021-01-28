from tkinter import *
from tkinter.filedialog import * ## pour l'explorateur de fichier
import tkinter.ttk as ttk
from PIL import Image,ImageTk
import os 
import Main as Princ

main = Tk()###création d'une fenêtre vide qui s'appelle main 
main.title("Algorithme génétique")### titre de la fenêtre

ch=r"logo_ei.PNG"
render = ImageTk.PhotoImage(Image.open(os.path.join(ch)))
Label(image=render).grid(columnspan=3)


nombre_generation=StringVar()
nombre_indiv=StringVar()

Label(main, text= "Nombre de génération").grid(row = 1, column = 0)
Entry(main,textvariable=nombre_generation).grid(row=1,column=1)

Label(main, text= "Nombre d'individus dans la population").grid(row = 2, column = 0)
Entry(main,textvariable=nombre_indiv).grid(row=2,column=1)

 
filename = StringVar()
Label(main,text="Cliquez sur ouvrir").grid(row=3,column=0)
Entry(main, textvariable=filename,state='disabled').grid(row=3,column=1)
Button(main,text='Ouvrir',command=lambda:filename.set(askopenfilename())).grid(row=3,column=2)

Methode= StringVar(main)
Label(main, text= "Sélection de la méthode").grid(row = 5, column = 0)

ttk.Combobox(main,values=["Tournoi","Elitisme"],textvariable=Methode).grid(row=5,column=1)

######Attention ici changer Command None en lancement des claculs de main.py 
Button(main,text="Lancer les calculs",command=lambda : Princ.test_draw_traited(filename.get(),Methode.get(),int(nombre_generation.get()),int(nombre_indiv.get())) ).grid(row=6, column= 1)

Button(main,text="Tracer la trajectoire 3D de la molécule initiale",command=lambda : Princ.test_draw_initial_seq(filename.get())).grid(row=7,column=0)

Button(main,text="Quitter",command=main.destroy).grid(row=8, column= 2)###création d'un boutton qui entraine la destruction (fermerture) de l'interface
main.mainloop()
