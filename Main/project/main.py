from tkinter import *
from pprint import *
from classe.plateau import *
from classe.event import *
from functools import partial
# import sys
# sys.path.append("./classe")

def initPlateau():


    # Micellious
    # Valeur indépendantes
    fenX = 1300
    fenY = 880


    # Event history
    initEvent = event(0, (0,0), "place")
    event_log = [initEvent]


    # Event id generator
    global id
    id = 1


    # Fenetre sur laquelle on placera tous les composants
    fen = Tk(className="Jeu d'Echec")
    fen.geometry(str(fenX) + "x" + str(fenY))


    # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
    echiquier = Canvas(fen, bg='white', width=950, height=int(fenY))
    echiquier.pack(side=LEFT)


    # Console, Canvas sur lequel placer les textes et autres commandes, lui-meme placé sur la fenêtre fen.
    console = Canvas(fen, bg='grey', width=(fenX - 950), height=int(fenY))
    console.pack(side=LEFT)


    # Text box for debugging

    # scrollbar = Scrollbar(console)
    # scrollbar.pack(side=RIGHT, fill=Y)

    cons_text = Text(console, bg="black", fg="white", width=(fenX - 950), height=int(fenY))
    cons_text.place(x=console.winfo_x(), y=console.winfo_y())
    #
    # cons_text.config(yscrollcommand=scrollbar.set)
    # scrollbar.config(command=cons_text.yview)

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
    coul_bouton = {}


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


            def move(tuple):

                global id
                newId = id

                bouton = dict_bouton[(tuple[0],tuple[1])]
                # if bouton["bg"] != clicked:
                #     bouton.config(bg="#aaaaaa")
                # else:
                #     bouton.config(bg=normal)

                cons_text.insert(1.0, str(plat.getCase(tuple[0],tuple[1]).getApercu()))

                if event_log[-1].getAction() == "place":

                    # On crée un nouvel évènement de click simple
                    newEvent = event(newId, tuple, "click")

                    # Comme c'est un click et non un place, ça signifie que ce bouton est
                    # l'origine du mouvement, donc contient le pion à bouger
                    if plat.getCase(tuple[0],tuple[1]):
                        newEvent.setCache(plat.getCase(tuple[0],tuple[1]).getImage())

                    # Colorie la case en gris pour indiquer l'origine du mouvement
                    bouton.config(bg="#aaaaaa")

                else:

                    # On crée un nouvel évènement de placement.
                    newEvent = event(newId, tuple, "place")

                    # L'évènement est un event de placement, donc l'évènement juste avant
                    # est un évènement d'origine (de click) donc on va chercher l'image
                    # contenu en cache dans cet évènement pour l'utiliser ici
                    image = event_log[-1].getCache()

                    # On récupère les coordonnées de la case cliquée à l'évènement précédant
                    former_case = event_log[-1].getOrigin()

                    # On récupère sa couleur de base (originelle)
                    former_button_normal_color = coul_bouton[(former_case[0], former_case[1])]

                    # Et on lui remet sa couleur de base. Puisque
                    dict_bouton[former_case].config(bg=former_button_normal_color)

                    if image:

                        print("@@@ IMAGE")

                        # Retire l'image du bouton de l'ancienne case
                        dict_bouton[former_case].config(image="")

                        # On met l'ancien pion dans la nouvelle case
                        # plat.setCase(tuple[0],tuple[1], plat.getCase(former_case[0], former_case[1]))

                        plat.move((former_case[0], former_case[1]), (tuple[0],tuple[1]))

                        # On vide l'ancienne case
                        # plat.empty(former_case[0], former_case[1])

                        # Place l'image de l'ancienne case sur la nouvelle
                        bouton.config(image=image)

                        plat.apercu()


                # newEvent.apercu()

                # On rajoute l'evènement à la liste des évènements
                event_log.append(newEvent)

                # On incrémente la chaine qui sert à créer le nom/id des évènements pour le prochain
                # évènement. Toujours de x + 1
                id +=  1


            # On crée un bouton à cette position, avec la photo de sa case du plateau, on lui donne une couleur.
            # Et une fonction onClick()
            bouton = Button(echiquier)

            # On ajoute ce bouton au dictionnaire de boutons
            dict_bouton[(x, y)] = bouton
            coul_bouton[(x, y)] = "#638f6e" if black else "white"

            bouton.config(
                width=echiquier.winfo_reqwidth()//8,  #119px
                    height=echiquier.winfo_reqheight()//8,  #113px
                        bg="#638f6e" if black else "white",
                            activebackground="#46634d" if black else "#bbbfbc",
                                image=photo,
                                    command=partial(move, (x, y)))

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
        # for event in event_log:
        #     event.apercu()
        # plat.apercu()
        plat.apercuSet()
        fen.destroy()

    # Protocol Handler
    fen.protocol("WM_DELETE_WINDOW", on_closing)

    # Stay alive
    fen.mainloop()



if __name__ == '__main__':

    initPlateau()

