from tkinter import *
from pprint import *
from classe.plateau import *
# from .classe.pion import *


def initPlateau():

    # Micellious
    fenX = 1300
    fenY = 880

    # Fenetre
    fen = Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX) + "x" + str(fenY))

    echiquier = Canvas(fen, bg='white', width=950, height=int(fenY))
    echiquier.pack(side=LEFT)
    console = Canvas(fen, bg='grey', width=(fenX - 950), height=int(fenY))
    console.pack(side=LEFT)

    plat = plateau()

    y = 0
    black = True
    dict_bouton = {}

    while y <= 8:
        x = 0
        while x <= 8:

            a = y+1 if y+1 < 9 else 8
            b = x+1 if x+1 < 9 else 8
            photo = plat.getCase(a, b).getImage()

            bouton = Button(echiquier,
                            width=echiquier.winfo_reqwidth()//8, #119px
                            height=echiquier.winfo_reqheight()//8, #113px
                            bg="#638f6e" if black else "white",
                            activebackground="#46634d" if black else "#bbbfbc",
                            image=photo)

            dict_bouton[(x,y)] = bouton

            bouton.place(x=x*echiquier.winfo_reqwidth()/8,y=y*echiquier.winfo_reqheight()/8)

            x += 1
            black = not black

        y += 1

    fen.mainloop()

    fen.destroy()



if __name__ == '__main__':

    initPlateau()


