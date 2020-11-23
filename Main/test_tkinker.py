from tkinter import *
from random import randrange

def consolePrint(text):
    console.create_text(60,10,text=text)

if __name__ == '__main__':

    # Micellious
    fenX = 1300
    fenY = 850

    # Fenetre
    fen=Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX)+"x"+str(fenY))

    plateau = Canvas(fen, bg='white', width=950, height=int(fenY))
    plateau.pack(side=LEFT)
    console = Canvas(fen, bg='grey', width=(fenX-950), height=int(fenY))
    console.pack(side=LEFT)
    # console.create_text(60,10,text="TA mère la chienne")
    # consolePrint("ta mère")

    pos = 0
    while pos <= plateau.winfo_reqwidth():
        consolePrint(plateau.winfo_reqwidth())
        plateau.create_line(pos, 0, pos, plateau.winfo_reqheight(), width=2, fill="black")
        plateau.create_line(0, pos, plateau.winfo_reqwidth(), pos, width=2, fill="black")
        pos += plateau.winfo_reqwidth() / 8
    fen.mainloop()

    fen.destroy()
