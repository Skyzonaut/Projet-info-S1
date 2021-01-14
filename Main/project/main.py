from tkinter import *
from pprint import *
from classe.plateau import *
from classe.event import *
from functools import partial
from time import *
from datetime import *
from threading import *

# TODO: Dossier présentation du code
# TODO: IA
# TODO: Voir pour cacher les mouvements normaux d'un pion quand il doit sauver son roi
# TODO: Implementer simulation
# TODO: Implémenter starts différents
# TODO: Implémenter coups spéciaux

running = True

class initPlateau(Frame):

        def __init__(self, parent):

            Frame.__init__(self, parent)

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
            self.whiteEnEchec = False
            self.blackEnEchec = False
            self.pionWhitePlayEchec = []
            self.pionBlackPlayEchec = []

            # Valeur contenant le tour actuel
            self.tourColorDisplay = True
            self.textTourStringVar = StringVar()
            self.textTourStringVar.set("AU TOUR DES BLANCS")

            # Valeur contenant le panneau d'affichage d'état du jeu
            self.textAffichage = StringVar()
            self.textAffichage.set("")

            # Valeur contenant le numéro du tour
            self.textNbTour = StringVar()
            self.textNbTour.set(str(self.tour))

            # Protocol Handler
            parent.protocol("WM_DELETE_WINDOW", self.on_closing)

            self.initiateUI()

        def initiateUI(self):

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

            self.tourLabel = Label(self.console, width=45, height=9)
            self.tourLabel['textvariable'] = self.textTourStringVar
            self.tourLabel['fg'] = "black"
            self.tourLabel['bg'] = "white"
            self.tourLabel.place(x=self.console.winfo_x()+11, y=55)

            self.historiquePanneau = Text(self.console, width=34, height=22)
            # self.historiquePanneau['textvariable'] = self.textTourStringVar
            self.historiquePanneau['fg'] = "black"
            self.historiquePanneau['bg'] = "#babfbb"
            self.historiquePanneau['cursor'] = "arrow"
            self.historiquePanneau['padx'] = "5px"
            self.historiquePanneau['pady'] = "5px"
            self.historiquePanneau['relief'] = "solid"
            self.historiquePanneau['borderwidth'] = "1px"
            self.historiquePanneau['state'] = "disabled"
            self.historiquePanneau['wrap'] = "word"
            self.historiquePanneau['font'] = ("Courier", 11, "bold")
            self.historiquePanneau.place(x=self.console.winfo_x()+11, y=205)

            self.affichage = Label(self.console, width=45, height=7)
            self.affichage['textvariable'] = self.textAffichage
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#789FDE"
            self.affichage.place(x=self.console.winfo_x()+12, y=600)

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

            if self.event_log[-1].getAction() != "click":

                if self.tourCouleurVerificateur(self.plat.getCase(tuple[0], tuple[1]).getCouleur(), self.tourColorDisplay):

                    # On crée un nouvel évènement de click simple
                    self.newEvent = event(str(self.newId), tuple, "click")

                    # On récupère la couleur du pion à jouer
                    self.couleurPion = self.plat.getCase(tuple[0], tuple[1]).getCouleur()

                    # Comme c'est un click et non un place, ça signifie que ce bouton est
                    # l'origine du mouvement, donc contient le pion à bouger
                    if self.plat.getCase(tuple[0], tuple[1]):

                        self.newEvent.setCache(self.plat.getCase(tuple[0], tuple[1]).getImage())

                    # Colorie la case en gris pour indiquer l'origine du mouvement
                    self.bouton.config(bg="#aaaaaa")

                    self.possibleMoves = self.plat.getPath(tuple)

                    couleurEnnemie = "blanc" if self.couleurPion == "noir" else "noir"

                    pieceEnnemies = self.plat.getMatriceByCouleur(couleurEnnemie)

                    pieceAllie = self.plat.getMatriceByCouleur(self.couleurPion)

                    # Empeche le roi de se déplacer dans une case qui le mettrait en situation d'échec
                    if self.plat.getCaseTuple(tuple).getType() == "roi":

                        zoneEnEchec = []

                        for piece in pieceEnnemies:

                            # zoneEnEchec += self.plat.getPath(piece, pion=True)
                            zoneEnEchec += self.plat.getPath(piece, pion=True)

                        for move in zoneEnEchec:

                            if move in self.possibleMoves:

                                self.possibleMoves.remove(move)

                    else:

                        # Empeche une piece de bouger si cela met son roi en echec
                        pieceAttaque = []
                        roi = self.plat.getRoi(self.couleurPion)

                        for piece in pieceEnnemies:

                            allieSurLeChemin = []

                            for allie in pieceAllie:

                                if allie in self.plat.getCasePathFinding(roi, piece, True):

                                    allieSurLeChemin.append(allie)

                            if len(allieSurLeChemin) <=  2:

                                if roi in self.plat.getCasePathFinding(roi, piece, True):

                                    if tuple in self.plat.getPath(piece):

                                        if tuple in self.plat.getCasePathFinding(roi, piece, True):

                                            self.possibleMoves.clear()
                                            break

                    for case in self.possibleMoves:

                        self.dict_bouton[case].config(bg="#CD4C4C")

                    self.newEvent.setTrace(self.possibleMoves)

                else:
                    
                    print("C'est aux", "blanc" if self.tourColorDisplay else "noirs", "de jouer")

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

                # Et on lui remet sa couleur de base.
                self.dict_bouton[self.former_case].config(bg=self.former_button_normal_color)

                # On récupère la couleur du pion qui a été sélectionné
                self.couleurPion = self.plat.getCase(self.former_case[0], self.former_case[1]).getCouleur()

                for traceCase in self.event_log[-1].getTrace():

                    self.dict_bouton[traceCase].config(bg=self.coul_bouton[traceCase])

                if self.image:

                    # possibleMove = self.plat.getPath(self.former_case)
                    possibleMove = self.event_log[-1].getTrace()

                    if tuple in possibleMove:

                        # Retire l'image du bouton de l'ancienne case
                        self.dict_bouton[self.former_case].config(image="")

                        if "empty" in self.plat.getCaseTuple(tuple).getName():
                            self.printPanneau(self.former_case, tuple, "move")
                        else:
                            self.printPanneau(self.former_case, tuple, "take")

                        self.plat.move(self.former_case, tuple)



                        # Place l'image de l'ancienne case sur la nouvelle
                        self.bouton.config(image=self.image)

                        self.tourColorDisplay = not self.tourColorDisplay
                        self.textTourStringVar.set("AU TOUR DES BLANCS" if self.tourColorDisplay else "AU TOUR DES NOIRS")
                        self.tourLabel['fg'] = "black" if self.tourColorDisplay else "white"
                        self.tourLabel['bg'] = "white" if self.tourColorDisplay else "black"

                        self.tour += 1
                        self.textNbTour.set(str(self.tour))

                    else:

                        print("Impossible move")

            self.listPionBlackPlayEchec = self.plat.checkEchec("blanc")
            self.listPionWhitePlayEchec = self.plat.checkEchec("noir")

            self.echecTrace = {"whitePlayEchec" : [], "blackPlayEchec" : []}

            if self.listPionBlackPlayEchec:

                self.dict_bouton[self.plat.getRoi("blanc")].config(bg="#CD4C4C")

                for pionEchec in self.listPionBlackPlayEchec:

                    self.dict_bouton[pionEchec].config(bg="#e08f38")

                self.echecTrace["blackPlayEchec"] = self.listPionBlackPlayEchec

                self.textAffichage.set("ECHEC")
                self.affichage['fg'] = "white"
                self.affichage['bg'] = "#A02B2B"
                self.whiteEnEchec = True


            else:

                self.original_color = self.coul_bouton[self.plat.getRoi("blanc")]
                self.dict_bouton[self.plat.getRoi("blanc")].config(bg=self.original_color)

                self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

                if self.echecTraceToEmpty:

                    for pionEchec in self.echecTraceToEmpty["blackPlayEchec"]:

                        # On récupère sa couleur de base (originelle)
                        self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

                        # Et on lui remet sa couleur de base.
                        self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

                self.textAffichage.set("")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#789FDE"

            if self.listPionWhitePlayEchec:

                self.dict_bouton[self.plat.getRoi("noir")].config(bg="#CD4C4C")

                for pionEchec in self.listPionWhitePlayEchec:

                    self.dict_bouton[pionEchec].config(bg="#e08f38")

                self.echecTrace["whitePlayEchec"] = self.listPionWhitePlayEchec

                self.textAffichage.set("ECHEC")
                self.affichage['fg'] = "white"
                self.affichage['bg'] = "#A02B2B"
                self.blackEnEchec = True

            else:

                self.original_color = self.coul_bouton[self.plat.getRoi("noir")]
                self.dict_bouton[self.plat.getRoi("noir")].config(bg=self.original_color)

                self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

                if self.echecTraceToEmpty:

                    for pionEchec in self.echecTraceToEmpty["whitePlayEchec"]:

                        # On récupère sa couleur de base (originelle)
                        self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

                        # Et on lui remet sa couleur de base.
                        self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

                self.textAffichage.set("")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#789FDE"

            checkMateWhiteTestResult = self.plat.checkMate("blanc")
            checkMateBlackTestResult = self.plat.checkMate("noir")
            print("@@@@@@@@@@@@@@@",checkMateWhiteTestResult)
            print("@@@@@@@@@@@@@@@",checkMateBlackTestResult)

            # =============================================================================================
            # Check echec et mats
            # =============================================================================================

            self.newEventSauveteur = {
                "whiteSaver" : [],
                "blackSaver" : [],
                "whiteSaverTrace" : [],
                "blackSaverTrace" : []
            }

            # White Test Echec ----------------------------------------------------------------------------

            if checkMateWhiteTestResult == "mat":

                self.textAffichage.set("ECHEC ET MAT\nLes Noirs l'emportent")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#A02B2B"

                self.freezeGrid()

            elif type(checkMateWhiteTestResult) == list:

                listeSauveteurWhite = []
                listeSauveteurWhiteTrace = []

                listeMoveRoiSave = checkMateWhiteTestResult

                for el in listeMoveRoiSave:

                    if self.plat.getCaseTuple(el[0]).getType() != 'roi':

                        self.dict_bouton[el[0]].config(bg="#5fb1cf")

                        listeSauveteurWhite.append(el[0])

                        for move in el[1]:

                            self.dict_bouton[el[1]].config(bg="#31cc55")

                            listeSauveteurWhiteTrace.append(el[1])

                self.newEventSauveteur["whiteSaver"] = listeSauveteurWhite
                self.newEventSauveteur["whiteSaverTrace"] = listeSauveteurWhiteTrace

                listButtonNotToDisable = listeSauveteurWhite + listeSauveteurWhiteTrace
                roiBlanc = self.plat.getRoi("blanc")
                listButtonNotToDisable.append(roiBlanc)
                listButtonNotToDisable += self.plat.getPath(roiBlanc)

                self.newEvent.setEnabledButton(listButtonNotToDisable)

                self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)


            elif checkMateWhiteTestResult == "no-echec":

                self.whiteSaverToEmpty = self.event_log[-1].getSauveteur()

                if self.whiteSaverToEmpty:

                    for saver in self.whiteSaverToEmpty["whiteSaver"]:
                        # On récupère sa couleur de base (originelle)
                        self.pionEchecOriginalColor = self.coul_bouton[saver]

                        # Et on lui remet sa couleur de base.
                        self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

                    for saverMove in self.whiteSaverToEmpty["whiteSaverTrace"]:

                        # On récupère sa couleur de base (originelle)
                        self.pionEchecOriginalColor = self.coul_bouton[saverMove]

                        # Et on lui remet sa couleur de base.
                        self.dict_bouton[saverMove].config(bg=self.pionEchecOriginalColor)

                self.enableAllButtons()

            # Black Test Echec ----------------------------------------------------------------------------

            if checkMateBlackTestResult == "mat":

                self.textAffichage.set("ECHEC ET MAT\nLes Blancs l'emportent")
                self.affichage['fg'] = "black"
                self.affichage['bg'] = "#A02B2B"

                self.freezeGrid()

            elif type(checkMateBlackTestResult) == list:

                listeSauveteurBlack = []
                listeSauveteurBlackTrace = []

                listeMoveRoiSave = checkMateBlackTestResult

                for el in listeMoveRoiSave:

                    if self.plat.getCaseTuple(el[0]).getType() != 'roi':

                        self.dict_bouton[el[0]].config(bg="#5fb1cf")

                        listeSauveteurBlack.append(el[0])

                        for move in el[1]:

                            self.dict_bouton[el[1]].config(bg="#31cc55")
                            listeSauveteurBlackTrace.append(el[1])

                self.newEventSauveteur["blackSaver"] = listeSauveteurBlack
                self.newEventSauveteur["blackSaverTrace"] = listeSauveteurBlackTrace

                listButtonNotToDisable = listeSauveteurBlack + listeSauveteurBlackTrace
                roiNoir = self.plat.getRoi("noir")
                listButtonNotToDisable.append(roiNoir)
                listButtonNotToDisable += self.plat.getPath(roiNoir)

                self.newEvent.setEnabledButton(listButtonNotToDisable)

                self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)

            elif checkMateBlackTestResult == "no-echec":

                self.blackSaverToEmpty = self.event_log[-1].getSauveteur()

                if self.blackSaverToEmpty:

                    for saver in self.blackSaverToEmpty["blackSaver"]:
                        # On récupère sa couleur de base (originelle)
                        self.pionEchecOriginalColor = self.coul_bouton[saver]

                        # Et on lui remet sa couleur de base.
                        self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

                    for saverMove in self.blackSaverToEmpty["blackSaverTrace"]:
                        # On récupère sa couleur de base (originelle)
                        self.pionEchecOriginalColor = self.coul_bouton[saverMove]

                        # Et on lui remet sa couleur de base.
                        self.dict_bouton[saverMove].config(bg=self.pionEchecOriginalColor)

                self.enableAllButtons()


            self.newEvent.setSauveteur(self.newEventSauveteur)
            self.newEvent.setEchecTrace(self.echecTrace)
            self.newEvent.apercu()

            # On rajoute l'evènement à la liste des évènements
            self.event_log.append(self.newEvent)

            # On incrémente la chaine qui sert à créer le nom/id des évènements pour le prochain
            # évènement. Toujours de x + 1
            self.id += 1

            # self.plat.apercu()

        def printPanneau(self, origin, target, type):

            self.historiquePanneau["state"] = "normal"

            pionOrigin = self.plat.getCaseTuple(origin)
            pionTarget = self.plat.getCaseTuple(target)

            txt = f"Tour : {self.tour} - {pionOrigin.getCouleur().upper()}\n"

            if type == "take":
                txt += f"{pionOrigin.getType()} {pionOrigin.getCouleur()} en {origin} prends "
                txt += f"{pionTarget.getType()} {pionTarget.getCouleur()} en {target}\n"

            elif type == "move":
                txt += f"{pionOrigin.getType()} {pionOrigin.getCouleur()} en {origin} va en {target}\n\n"

            # Pour de futures évolutions
            elif type == "echec":
                pass

            elif type == "mat":
                pass

            self.historiquePanneau.insert(END, txt)
            self.historiquePanneau["state"] = "disabled"
            self.historiquePanneau.see("end")

        def tourCouleurVerificateur(self, couleur, boolean):

            if (couleur == "blanc" or couleur == None) and boolean:

                return True

            elif (couleur == "noir" or couleur == None) and not boolean:

                return True

            else:

                return False

        # def disableButton(self, buttonToDisableList):
        #     for button in buttonToDisableList:
        #          button['command'] = DISABLE
        #
        # def enableButton(self, buttonToDisableList):
        #     for button in buttonToEnableList:
        #         button['state'] = ENABlE

        def disableButtonInCaseOfEchec(self, allButtonDict, buttonNotToDisableList):

            for coords, button in allButtonDict.items():

                if coords not in buttonNotToDisableList:

                    button['state'] = DISABLED

        def enableAllButtons(self):

            for coords, button in self.dict_bouton.items():

                button['state'] = NORMAL

        def freezeGrid(self):

            for coords, button in self.dict_bouton.items():

                button['command'] = self.freezeButton

        def freezeButton(self):
            # pass volontaire, permet de rajouter une commande null aux boutons
            # pour que l'on puisse les freeze
            pass

        def restart(self):
            print("restart")
            self.on_closing()
            self.parent.quit()

        def on_closing(self):
            print("\n--- Fermeture ---")
            self.parent.destroy()

class initGame(Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent)

        self.parent = parent

        parent.resizable(False, False)

        # Valeur indépendantes
        self.size = 600

        # Protocol Handler
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Fenetre sur laquelle on placera tous les composants
        self.parent.geometry(str(self.size) + "x" + str(self.size))

        self.createIntroGui()

    def createIntroGui(self):
        self.background_image = PhotoImage(file='../res/intro_background.png')

        # # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
        self.mainCanvas = Canvas(self.parent, width=self.size, height=self.size)
        self.mainCanvas.pack(side=LEFT)
        self.mainCanvas.create_image(0, 0, image=self.background_image, anchor='nw')

        # self.startPVPGameButton = Button(self.mainCanvas, text="START A PVP GAME", width=20, height=3)
        self.startPVPGameButton = Button(self.mainCanvas, text="START A PVP GAME", width=20, height=3, command=self.startPVPGame)
        self.startPVPGameButton['fg'] = "white"
        self.startPVPGameButton['bg'] = "#000000"
        self.startPVPGameButton['borderwidth'] = "2"
        self.startPVPGameButton['relief'] = "raised"
        self.startPVPGameButton.place(x=230, y=330)

        self.startPVEGameButton = Button(self.mainCanvas, text="START A GAME VS AN IA", width=20, height=3)
        self.startPVEGameButton['borderwidth'] = 3
        self.startPVEGameButton['fg'] = "white"
        self.startPVEGameButton['bg'] = "#000000"
        self.startPVEGameButton['borderwidth'] = "2"
        self.startPVEGameButton['relief'] = "raised"
        self.startPVEGameButton.place(x=230, y=400)

    def startPVPGame(self):
        while running:
            print(running)
            newWindow = Toplevel(rootGame)
            game = initPlateau(newWindow)
            game.mainloop()

    def on_closing(self):
        print("\n--- Fermeture ---")
        self.parent.destroy()

if __name__ == '__main__':

    rootGame = Tk(className=" Echec The VideoGame by Hideo Kojima")
    intro = initGame(rootGame)
    intro.mainloop()

    # while running:
    #
    #     print(running)
    #     # rootGame = Tk(className=" Jeu d'échecs")
    #     newWindow = Toplevel(rootGame)
    #     game = initPlateau(newWindow)
    #     game.mainloop()

    # def run():
    #     gamePlaying = True
    #     oldTime = datetime.now().strftime("%H:%M:%S")
    #     while gamePlaying:
    #         now = datetime.now().strftime("%H:%M:%S")
    #         if oldTime != now:
    #             print(now)
    #             oldTime = now
    #
    #
    # control_thread = Thread(target=run, daemon=True)

    # control_thread.start()