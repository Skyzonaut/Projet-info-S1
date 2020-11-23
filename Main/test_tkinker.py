from tkinter import *
from random import randrange

def drawline():

    global x1, y1, x2, y2, coul
    plateau.create_line(x1, y1, x2, y2, width=2, fill=coul)

    y2, y1 = y2 + 10, y1 - 10

def drawline2():

    global x3, y3, x4, y4, x5, y5, x6, y6, coul2
    plateau.create_line(x3, y3, x4, y4, width=2, fill=coul2)
    plateau.create_line(x5, y5, x6, y6, width=2, fill=coul2)

def changecolor():

    global coul
    pal=['purple', 'cyan', 'maroon', 'green', 'red', 'blue', 'orange', 'yellow']
    c = randrange(8)
    coul = pal[c]


if __name__ == '__main__':

    # Micellious
    coul='white'
    coul2='red'
    fenX = 1300
    fenY = 850

    # Fenetre
    fen=Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX)+"x"+str(fenY))

    plateau = Canvas(fen, bg='white', width=950, height=int(fenY))
    console = Canvas(fen, bg='white', width=(fenX-950), height=int(fenY))
    plateau.pack(side=LEFT)

    pos = 0
    while pos <= plateau.winfo_reqwidth() / 8:
        print(plateau.winfo_reqwidth())
        plateau.create_line(pos, 0, pos, plateau.winfo_reqheight(), width=2, fill=coul2)
        pos += plateau.winfo_reqwidth() / 8
    fen.mainloop()

    fen.destroy()