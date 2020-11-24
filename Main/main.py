from tkinter import *

from project.classe.plateau import *
from project.classe.pion import *

if __name__ == '__main__':

    # Micellious
    fenX = 1300
    fenY = 850

    # Fenetre
    fen=Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX)+"x"+str(fenY))

    echi = Canvas(fen, bg='white', width=950, height=int(fenY))
    echi.pack(side=LEFT)
    console = Canvas(fen, bg='grey', width=(fenX-950), height=int(fenY))
    console.pack(side=LEFT)
    # console.create_text(60,10,text="TA mère la chienne")
    # consolePrint("ta mère")

    plat = plateau()
    plat.apercu()
    pi = pion()
    pi.apercu()

    pos = 0
    while pos <= echi.winfo_reqwidth():
        echi.create_line(pos, 0, pos, echi.winfo_reqheight(), width=2, fill="black")
        echi.create_line(0, pos, echi.winfo_reqwidth(), pos, width=2, fill="black")
        pos += echi.winfo_reqwidth() / 8

    fen.mainloop()
    fen.destroy()


