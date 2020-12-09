from tkinter import *
from pprint import *
from classe.plateau import *
from classe.event import *
from functools import partial

def initPlateau():


    # Micellious
    # Valeur indépendantes
    fenX = 1300
    fenY = 880


    # Event history
    event_log = []


    # Event id generator
    global id
    id = 0


    # Fenetre sur laquelle on placera tous les composants
    fen = Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX) + "x" + str(fenY))


    # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
    echiquier = Canvas(fen, bg='white', width=950, height=int(fenY))
    echiquier.pack(side=LEFT)


    # Console, Canvas sur lequel placer les textes et autres commandes, lui-meme placé sur la fenêtre fen.
    console = Canvas(fen, bg='grey', width=(fenX - 950), height=int(fenY))
    console.pack(side=LEFT)
    # label_title = Label(console,text="Aloooooo")
    # label_title.pack()


    # Objet plateau qui contient les positions et infos et pions.
    # Utilisant comme repertoire un Set de pion limité
    plat = plateau()
    plat.apercu()


    # Dictionnaire de type { (x,y) : button } contenant tous les boutons (ou cases) de l'échiquier,
    # permet de faire la lisaison avec les cases du plateau.
    # En cas d'action sur un bouton on parcours ce dictionnaire pour retrouver sa matrice,
    # et ainsi pouvoir mettre à jour celle du plateau.
    # En quelque sorte ce dictionnaire est la matrice graphique, là où celle du plateau est la "base de donnée"
    dict_bouton = {}
    col_bouton = {}


    # Valeur permettant d'alterner les couleurs
    black = False


    # On parcours de gauche à droite, puis de haut en bas
    # Du bas vers le haut
    y = 1
    while y <= 8:

        # De gaughe à droite
        x = 1
        while x <= 8:

            # On récupère la photo correspondant au pion contenant à cette emplacement du plateau
            photo = plat.getCase(x, y).getImage()


            def changeCaseColorOnClick(tuple):

                global id
                newId = id

                bouton = dict_bouton[(tuple[0],tuple[1])]
                normal = col_bouton[(tuple[0],tuple[1])]
                clicked = "#aaaaaa"

                if bouton["bg"] != clicked:
                    bouton.config(bg="#aaaaaa")
                else:
                    bouton.config(bg=normal)

                newEvent = event(newId, tuple, "click")
                event_log.append(newEvent)
                id +=  1


            # On crée un bouton à cette position, avec la photo de sa case du plateau, on lui donne une couleur.
            # Et une fonction onClick()
            bouton = Button(echiquier)

            # On ajoute ce bouton au dictionnaire de boutons
            dict_bouton[(x, y)] = bouton
            col_bouton[(x, y)] = "#638f6e" if black else "white"

            bouton.config(
                width=echiquier.winfo_reqwidth()//8,  #119px
                    height=echiquier.winfo_reqheight()//8,  #113px
                        bg="#638f6e" if black else "white",
                            activebackground="#46634d" if black else "#bbbfbc",
                                image=photo,
                                    command=partial(changeCaseColorOnClick, (x, y)))

            # bouton.bind("<Button-3>", partial(rightClick, ((x, y))))

            # Et pour finir on place le bouton sur le canvas pour l'afficher
            bouton.place(x=(x-1)*echiquier.winfo_reqwidth()/8, y=(y-1)*echiquier.winfo_reqheight()/8)

            # On passe à la colonne suivante et change de couleur
            x += 1 ; black = not black

        # On passe à la Ligne suivante et change de couleur
        y += 1 ; black = not black


    # Actions de fermeture
    def on_closing():
        print("\n--- Fermeture ---")
        for event in event_log:
            event.apercu()
        fen.destroy()

    # Protocol Handler
    fen.protocol("WM_DELETE_WINDOW", on_closing)

    # Stay alive
    fen.mainloop()




def temp(case2):

    piece1 = matrice[case1]

    matrice[case2].setState(False)
    matrice[case2].setAssociation(False)
    matrice[case2] = piece1
    matrice[case1] = self.setDeJeu.getFreePion("empty","")


if __name__ == '__main__':

    initPlateau()

