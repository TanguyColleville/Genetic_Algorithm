from tkinter import *
from tkinter.filedialog import * ## pour l'explorateur de fichier
import tkinter.ttk as ttk
from PIL import Image,ImageTk
import os 
import Main as Princ

main = Tk()
main.title("Algorithme génétique")

# Permet de gérer le blocage et déblocage des boutons si le fichier est chargé ou non 
def switchButtonState():
    Button_calculus['state']="normal"
    Button_init['state']="normal"

# Affichage du logo de notre projet
ch=r"logo_ei.PNG"
render = ImageTk.PhotoImage(Image.open(os.path.join(ch)))
Label(image=render).grid(columnspan=3)


nombre_generation=StringVar(main,value="100")
nombre_indiv=StringVar(main,value="500")

Label(main, text= "Nombre de génération").grid(row = 1, column = 0)
Entry(main,textvariable=nombre_generation).grid(row=1,column=1)

Label(main, text= "Nombre d'individus dans la population").grid(row = 2, column = 0)
Entry(main,textvariable=nombre_indiv).grid(row=2,column=1)

# Permet de récupérer le fichier fasta à étudier
filename = StringVar()
Label(main,text="Cliquez sur ouvrir").grid(row=3,column=0)
Entry(main, textvariable=filename,state='disabled').grid(row=3,column=1)
Button_open=Button(main,text='Ouvrir',command=lambda:[filename.set(askopenfilename(filetypes=[("Fasta file", "*.fasta*")])),switchButtonState()])
Button_open.grid(row=3,column=2)

# Entrées des différents paramètres de notre outil 
Methode= StringVar(main)
Label(main, text= "Sélection de la méthode").grid(row = 5, column = 0)

Combo=ttk.Combobox(main,values=["Tournoi","Elitisme"],textvariable=Methode)
Combo.current(0)
Combo.grid(row=5,column=1)


Scalvar=StringVar(main,value=False)
Checkbutton(main,text="Scaling",variable=Scalvar,onvalue=True,offvalue=False).grid(row=6,column=0)

Luckvar=StringVar(main,value=0)
Label(main,text="Entrer une valeur de probabilité (float)").grid(row=7,column=0)
Entry(main, textvariable=Luckvar,state='normal').grid(row=7,column=1)

Puissvar=StringVar(main,value=2)
Label(main,text="Entrer une valeur de puissance (int)").grid(row=8,column=0)
Entry(main, textvariable=Puissvar,state='normal').grid(row=8,column=1)

# Permet de lancer les calculs d'optimisation d'angles
Button_calculus=Button(main,text="Lancer les calculs",command=lambda : Princ.test_draw_traited(filename.get(),bool(Scalvar.get()),Methode.get(),int(nombre_generation.get()),int(nombre_indiv.get()),float(Luckvar.get()),int(Puissvar.get())),state='disabled' )
Button_calculus.grid(row=10, column= 1)

# Permet de tracer la molécule à partir de la table initiale
Button_init=Button(main,text="Tracer la trajectoire 3D de la molécule initiale",command=lambda : Princ.test_draw_initial_seq(filename.get()),state='disabled')
Button_init.grid(row=10,column=0)

Button(main,text="Quitter",command=main.destroy).grid(row=12, columnspan=3)###création d'un boutton qui entraine la destruction (fermerture) de l'interface

main.mainloop()
