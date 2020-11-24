from tkinter import *
from pprint import *
from project.classe.plateau import *
from project.classe.pion import *


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
    plat.apercu()
    pi = pion()
    pi.apercu()
    # photo = PhotoImage(file=r"../res/noir/cavalier_noir.png")
    # bouton = Button(echiquier, # 113px
    #                 image=photo)
    # bouton.place(x=0, y=0)

    y = 0
    black = True
    photo = PhotoImage(file = r"../res/noir/cavalier_noir.png")
    photoblanc = PhotoImage(file = r"../res/blanc/cavalier_blanc.png")
    dict_bouton = {}
    while y <= 8:
        x = 0
        while x <= 8:
            bouton = Button(echiquier,
                            width=echiquier.winfo_reqwidth()//8, #119px
                            height=echiquier.winfo_reqheight()//8, #113px
                            bg="#638f6e" if black else "white",
                            activebackground="#46634d" if black else "#bbbfbc")
            dict_bouton[(x,y)] = bouton
            bouton.place(x=x*echiquier.winfo_reqwidth()/8,y=y*echiquier.winfo_reqheight()/8)
            x += 1
            black = not black
        y += 1



    # bouton = Button(echiquier,
    #                         width=echiquier.winfo_reqwidth()//8, #119px
    #                         height=echiquier.winfo_reqheight()//8, #113px
    #                         bg="#638f6e" if black else "white",
    #                         activebackground="#46634d" if black else "#bbbfbc",
    #                         image=PhotoImage(file = "../res/noir/cavalier_noir.png"))


    # pos = 0
    # while pos <= echiquier.winfo_reqwidth():
    #     echiquier.create_line(pos, 0, pos, echiquier.winfo_reqheight(), width=2, fill="black")
    #     echiquier.create_line(0, pos, echiquier.winfo_reqwidth(), pos, width=2, fill="black")
    #     pos += echiquier.winfo_reqwidth() / 8

    fen.mainloop()

    fen.destroy()



if __name__ == '__main__':

    initPlateau()


