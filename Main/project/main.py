from tkinter import *
from pprint import *
from classe.plateau import *
from classe.event import *
from functools import partial
from time import *
from datetime import *
from threading import *

# TODO: Dossier présentation du code
# Test

class initPlateau(Frame):
        def __init__(self, parent):

            Frame.__init__(self, parent)

            print("intitialization")

            self.parent = parent

            parent.resizable(False, False)

            # Valeur indépendantes
            self.fenX = 1300
            self.fenY = 880

            # Event id generator
            self.id = 1
            print(self.id)
            # Nombre du tour
            self.tour = 1

            # Event history
            initEvent = event("0", (0,0), "place")
            self.event_log = [initEvent]

            # Objet plateau qui contient les positions et infos et pions.
            # Utilisant comme repertoire un Set de pion limité
            self.plat = Plateau()

            # Dictionnaire de type { (x,y) : button } contenant tous les boutons (ou cases) de l'échiquier,
            # permet de faire la lisaison avec les cases du plateau.
            # En cas d'action sur un bouton on parcours ce dictionnaire pour retrouver sa matrice,
            # et ainsi pouvoir mettre à jour celle du plateau.
            # En quelque sorte ce dictionnaire est la matrice graphique, là où celle du plateau est la "base de donnée"
            self.dict_bouton = {}
            self.coul_bouton = {}

            # Valeur permettant d'alterner les couleurs
            self.black = False

            # Echec ou non, permet de bloquer le jeu si il y a un echec
            self.echec = False

            # Valeur contenant le tour actuel
            self.tourWhite = True
            self.textTourStringVar = StringVar()
            self.textTourStringVar.set("AU TOUR DES BLANCS")
            print(self.textTourStringVar.get())
            # Valeur contenant le panneau d'affichage d'état du jeu
            self.textAffichage = StringVar()
            self.textAffichage.set("")

            # Valeur contenant le numéro du tour
            self.textNbTour = StringVar()
            self.textNbTour.set(str(self.tour))

            # # Protocol Handler
            # parent.protocol("WM_DELETE_WINDOW", on_closing)

            self.initiateUI()

        def initiateUI(self):

            print("InitiateUI")

            # Fenetre sur laquelle on placera tous les composants
            self.parent.geometry(str(self.fenX) + "x" + str(self.fenY))

            # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
            self.echiquier = Canvas(self.parent, bg='white', width=950, height=int(self.fenY))
            self.echiquier.pack(side=LEFT)

            # Console, Canvas sur lequel placer les textes et autres commandes, lui-meme placé sur la fenêtre fen.
            self.console = Canvas(self.parent, bg="grey", width=(self.fenX - 950), height=int(self.fenY))
            self.console.pack(side=LEFT)

            self.nbTour = Label(self.console, width=45, height=2)
            self.nbTour['textvariable'] = self.textNbTour
            self.nbTour['fg'] = "black"
            self.nbTour['bg'] = "#3BCB38"
            self.nbTour.place(x=self.console.winfo_x()+11, y=8)

            self.tourLabel = Label(self.console, width=45, height=12)
            self.tourLabel['textvariable'] = self.textTourStringVar
            self.tourLabel['fg'] = "black"
            self.tourLabel['bg'] = "white"
            self.tourLabel.place(x=self.console.winfo_x()+11, y=55)

            self.affichage = Label(self.console, width=45, height=12)
            self.affichage['textvariable'] = self.textAffichage
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#789FDE"
            self.affichage.place(x=self.console.winfo_x()+12, y=520)

            self.restartButton = Button(self.console, text="RESTART GAME", width=45, height=4, command=self.restart)
            self.restartButton['borderwidth'] = 3
            self.restartButton['fg'] = "black"
            self.restartButton['bg'] = "grey"
            self.restartButton.place(x=self.console.winfo_x()+11, y=720)

            self.quitButton = Button(self.console, text="QUIT", width=45, height=4, command=self.on_closing)
            self.quitButton['borderwidth'] = 3
            self.quitButton['fg'] = "white"
            self.quitButton['bg'] = "#A02B2B"
            self.quitButton.place(x=self.console.winfo_x()+11, y=800)

            # self.cons_text = Text(self.console, bg="black", fg="white", width=(self.fenX - 950), height=int(self.fenY))
            # self.cons_text.place(x=self.console.winfo_x(), y=self.console.winfo_y())

            self.create_grid()

        def create_grid(self):

            print("Create Grid")
            # On parcours de gauche à droite, puis de haut en bas
            # Du bas vers le haut
            self.y = 1
            while self.y <= 8:

                # De gaughe à droite
                self.x = 1
                while self.x <= 8:

                    # On récupère la photo correspondant au pion contenant à cette emplacement du plateau
                    self.photo = self.plat.getCase(self.x, self.y).getImage()

                    # On crée un bouton à cette position, avec la photo de sa case du plateau, on lui donne une couleur.
                    # Et une fonction onClick()
                    self.bouton = Button(self.echiquier)

                    # On ajoute ce bouton au dictionnaire de boutons
                    self.dict_bouton[(self.x, self.y)] = self.bouton
                    self.coul_bouton[(self.x, self.y)] = "#638f6e" if self.black else "white"

                    self.bouton.config(
                        width=self.echiquier.winfo_reqwidth()//8,  #119px
                            height=self.echiquier.winfo_reqheight()//8,  #113px
                                bg="#638f6e" if self.black else "white",
                                    activebackground="#46634d" if self.black else "#bbbfbc",
                                        image=self.photo,
                                            command=partial(self.move, (self.x, self.y)))

                    # Et pour finir on place le bouton sur le canvas pour l'afficher
                    self.bouton.place(x=(self.x-1)*self.echiquier.winfo_reqwidth()/8, y=(self.y-1)*self.echiquier.winfo_reqheight()/8)

                    # On passe à la colonne suivante et change de couleur
                    self.x += 1 ; self.black = not self.black

                # On passe à la Ligne suivante et change de couleur
                self.y += 1 ; self.black = not self.black


        def move(self, tuple):

            self.newId = self.id

            self.bouton = self.dict_bouton[(tuple[0], tuple[1])]

            self.couleurPion = ""

            # Print piece on the console if enable
            # self.cons_text.insert(1.0, str(self.plat.getCase(tuple[0], tuple[1]).getApercu()))

            # if not self.echec or self.echec:

            if self.event_log[-1].getAction() != "click":

                if self.tourCouleurVerificateur(self.plat.getCase(tuple[0], tuple[1]).getCouleur(), self.tourWhite):

                    # On crée un nouvel évènement de click simple
                    self.newEvent = event(str(self.newId), tuple, "click")

                    # Comme c'est un click et non un place, ça signifie que ce bouton est
                    # l'origine du mouvement, donc contient le pion à bouger
                    if self.plat.getCase(tuple[0], tuple[1]):

                        self.newEvent.setCache(self.plat.getCase(tuple[0], tuple[1]).getImage())

                    # Colorie la case en gris pour indiquer l'origine du mouvement
                    self.bouton.config(bg="#aaaaaa")

                    self.possibleMoves = self.plat.getPath(tuple)

                    for case in self.possibleMoves:

                        self.dict_bouton[case].config(bg="#CD4C4C")

                    self.newEvent.setTrace(self.possibleMoves)

                    # On récupère la couleur du pion à jouer
                    self.couleurPion = self.plat.getCase(tuple[0], tuple[1]).getCouleur()

                else:
                    
                    print("C'est aux", "blanc" if self.tourWhite else "noirs", "de jouer")

            else:

                # On crée un nouvel évènement de placement.
                self.newEvent = event(str(self.newId), tuple, "place")

                # L'évènement est un event de placement, donc l'évènement juste avant
                # est un évènement d'origine (de click) donc on va chercher l'image
                # contenu en cache dans cet évènement pour l'utiliser ici
                self.image = self.event_log[-1].getCache()

                # On récupère les coordonnées de la case cliquée à l'évènement précédant
                self.former_case = self.event_log[-1].getOrigin()

                # On récupère sa couleur de base (originelle)
                self.former_button_normal_color = self.coul_bouton[self.former_case]

                # Et on lui remet sa couleur de base. Puisque
                self.dict_bouton[self.former_case].config(bg=self.former_button_normal_color)

                # On récupère la couleur du pion qui a été sélectionné
                self.couleurPion = self.plat.getCase(self.former_case[0], self.former_case[1]).getCouleur()

                for traceCase in self.event_log[-1].getTrace():

                    self.dict_bouton[traceCase].config(bg=self.coul_bouton[traceCase])

                if self.image:

                    if tuple in self.plat.getPath(self.former_case):

                        # Retire l'image du bouton de l'ancienne case
                        self.dict_bouton[self.former_case].config(image="")

                        # On met l'ancien pion dans la nouvelle case
                        # plat.setCase(tuple[0],tuple[1], plat.getCase(former_case[0], former_case[1]))

                        self.plat.move(self.former_case, tuple)

                        # On vide l'ancienne case
                        # plat.empty(former_case[0], former_case[1])

                        # Place l'image de l'ancienne case sur la nouvelle
                        self.bouton.config(image=self.image)

                        self.tourWhite = not self.tourWhite
                        self.textTourStringVar.set("AU TOUR DES BLANCS" if self.tourWhite else "AU TOUR DES NOIRS")
                        self.tourLabel['fg'] = "black" if self.tourWhite else "white"
                        self.tourLabel['bg'] = "white" if self.tourWhite else "black"

                        self.tour += 1
                        self.textNbTour.set(str(self.tour))

                    else:

                        print("Impossible move")


            self.newEvent.apercu()

            # On rajoute l'evènement à la liste des évènements
            self.event_log.append(self.newEvent)

            print("@@@@@@", self.plat.checkMate("blanc"))
            print("@@@@@@", self.plat.checkMate("noir"))

            self.listPionEchec = self.plat.checkEchec(self.couleurPion)

            if self.listPionEchec:

                self.dict_bouton[self.plat.getRoi(self.couleurPion)].config(bg="#CD4C4C")

                # self.newEchecEvent = event(str(self.newId) + "_echec", tuple, "echec")
                # self.newEchecEvent.setTrace(self.listPionEchec)
                # self.newEchecEvent.apercu()
                # self.event_log.append(self.newEchecEvent)

                for pionEchec in self.listPionEchec:
                    self.dict_bouton[pionEchec].config(bg="#e08f38")

                self.textAffichage.set("ECHEC")
                self.affichage['fg'] = "white"
                self.affichage['bg'] = "#A02B2B"
                self.echec = True

            else:
                #
                # self.original_color = self.coul_bouton[self.plat.getRoi(self.couleurPion)]
                # self.dict_bouton[self.plat.getRoi(self.couleurPion)].config(bg=self.original_color)

                self.textAffichage.set("")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#789FDE"

            if self.plat.checkMate("blanc") == "mat":

                self.textAffichage.set("ECHEC ET MAT\nLes Noirs l'emportent")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#A02B2B"

                winPopUp = Tk(className=" ECHECS")

            if self.plat.checkMate("noir") == "mat":

                self.textAffichage.set("ECHEC ET MAT\nLes Blancs l'emportent")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#A02B2B"

            # On incrémente la chaine qui sert à créer le nom/id des évènements pour le prochain
            # évènement. Toujours de x + 1
            self.id += 1


        def tourCouleurVerificateur(self, couleur, boolean):

            if (couleur == "blanc" or couleur == None) and boolean:

                return True

            elif (couleur == "noir" or couleur == None) and not boolean:

                return True

            else:

                return False


        def game(self):
            pass
            # gamePlaying = True
            # oldTime = datetime.now().strftime("%H:%M:%S")
            # while gamePlaying:
            #     now = datetime.now().strftime("%H:%M:%S")
            #     if oldTime != now:
            #         print(now)
            #         oldTime = now

        def restart(self):
            print("restart")
            self.__init__(self.parent)
            # self.plat.__init__()
            # self.initiateUI()
            # self.plat.apercu()
            # self.on_closing()

        # Actions de fermeture
        def on_closing(self):
            print("\n--- Fermeture ---")
            # for event in event_log:
            #     event.apercu()
            # self.plat.apercu()
            # self.plat.apercuSet()
            self.parent.destroy()

        # # Stay alive
        # fen.mainloop()

if __name__ == '__main__':

    root = Tk(className=" Jeu d'échecs")

    # def run():
    #     gamePlaying = True
    #     oldTime = datetime.now().strftime("%H:%M:%S")
    #     while gamePlaying:
    #         now = datetime.now().strftime("%H:%M:%S")
    #         if oldTime != now:
    #             print(now)
    #             oldTime = now


    # control_thread = Thread(target=run, daemon=True)
    game = initPlateau(root)
    # control_thread.start()
    root.mainloop()