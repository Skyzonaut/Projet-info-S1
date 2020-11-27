from tkinter import *
from pprint import *
from classe.plateau import *
# from .classe.pion import *
from functools import partial

def initPlateau():

    # Micellious
    # Valeur indépendantes
    fenX = 1300
    fenY = 880


    # Fenetre sur laquelle on placera tous les composants
    fen = Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX) + "x" + str(fenY))


    # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
    echiquier = Canvas(fen, bg='white', width=950, height=int(fenY))
    echiquier.pack(side=LEFT)


    # Console, Canvas sur lequel placer les textes et autres commandes, lui-meme placé sur la fenêtre fen.
    console = Canvas(fen, bg='grey', width=(fenX - 950), height=int(fenY))
    console.pack(side=LEFT)


    # Ojbet plateau qui contient les positions et infos et pions.
    # Utilisant comme repertoire un Set de pion limité
    plat = plateau()
    plat.apercu()


    # Dictionnaire de type { (x,y) : button } contenant tous les boutons (ou cases) de l'échiquier,
    # permet de faire la lisaison avec les cases du plateau.
    # En cas d'action sur un bouton on parcours ce dictionnaire pour retrouver sa matrice,
    # et ainsi pouvoir mettre à jour celle du plateau.
    # En quelque sorte ce dictionnaire est la matrice graphique, là où celle du plateau est la "base de donnée"
    dict_bouton = {}


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



            def movePionTo(x, y):
               dict_bouton[(x,y)].config(bg="#aaaaaa")
               print(x, y)

            # On crée un bouton à cette position, avec la photo de sa case du plateau, on lui donne une couleur.
            # Et une fonction onClick()
            bouton = Button(echiquier)

            # On ajoute ce bouton au dictionnaire de boutons
            dict_bouton[(x, y)] = bouton

            bouton.config(
                width=echiquier.winfo_reqwidth()//8,  #119px
                    height=echiquier.winfo_reqheight()//8,  #113px
                        bg="#638f6e" if black else "white",
                            activebackground="#46634d" if black else "#bbbfbc",
                                image=photo,
                                    command=partial(movePionTo, x, y))

            # Et pour finir on place le bouton sur le canvas pour l'afficher
            bouton.place(x=(x-1)*echiquier.winfo_reqwidth()/8, y=(y-1)*echiquier.winfo_reqheight()/8)

            # On passe à la colonne suivante et change de couleur
            x += 1 ; black = not black

        # On passe à la Ligne suivante et change de couleur
        y += 1 ; black = not black


    # Actions de fermeture
    def on_closing():
        print("\n--- Fermeture ---")
        fen.destroy()

    # Protocol Handler
    fen.protocol("WM_DELETE_WINDOW", on_closing)

    # Stay alive
    fen.mainloop()




def movePionTo(case2):

    piece1 = matrice[case1]

    matrice[case2].setState(False)
    matrice[case2].setAssociation(False)
    matrice[case2] = piece1
    matrice[case1] = self.setDeJeu.getFreePion("empty","")


if __name__ == '__main__':

    initPlateau()


